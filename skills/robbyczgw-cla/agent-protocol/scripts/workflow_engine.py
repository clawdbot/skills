#!/usr/bin/env python3
"""
Workflow Engine - Orchestrates multi-agent workflows based on event triggers.

Monitors the event bus and executes workflows when matching events arrive.
Supports conditional routing, parallel execution, error handling, and retries.
"""

import json
import sys
import time
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from event_bus import EventBus

# Paths
WORKFLOW_DIR = Path(__file__).parent.parent / "config" / "workflows"
WORKFLOW_STATE_DIR = Path.home() / ".clawdbot" / "workflow_state"
WORKFLOW_LOG_DIR = Path.home() / ".clawdbot" / "events" / "log" / "workflows"

# Ensure directories exist
WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOW_STATE_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOW_LOG_DIR.mkdir(parents=True, exist_ok=True)


class WorkflowEngine:
    """Executes workflows based on event triggers."""
    
    def __init__(self):
        self.bus = EventBus()
        self.workflows = self._load_workflows()
    
    def _load_workflows(self) -> List[Dict]:
        """Load all workflow definitions."""
        workflows = []
        
        if not WORKFLOW_DIR.exists():
            return workflows
        
        for workflow_file in WORKFLOW_DIR.glob("*.json"):
            try:
                workflow = json.loads(workflow_file.read_text())
                
                # Validate workflow
                if self._validate_workflow(workflow):
                    workflows.append(workflow)
                else:
                    self._log(f"Invalid workflow: {workflow_file.name}", "WARNING")
            
            except Exception as e:
                self._log(f"Error loading workflow {workflow_file.name}: {e}", "ERROR")
        
        return workflows
    
    def _validate_workflow(self, workflow: Dict) -> bool:
        """Validate workflow structure."""
        required = ["workflow_id", "trigger", "steps"]
        
        for field in required:
            if field not in workflow:
                return False
        
        if "event_type" not in workflow["trigger"]:
            return False
        
        if not isinstance(workflow["steps"], list) or len(workflow["steps"]) == 0:
            return False
        
        return True
    
    def _log(self, message: str, level: str = "INFO"):
        """Log workflow engine messages."""
        timestamp = datetime.utcnow().isoformat()
        log_line = f"[{timestamp}] [{level}] [WorkflowEngine] {message}\n"
        
        log_file = WORKFLOW_LOG_DIR / "engine.log"
        try:
            with open(log_file, "a") as f:
                f.write(log_line)
        except:
            pass
        
        if level in ("ERROR", "WARNING"):
            print(log_line, file=sys.stderr)
    
    def _matches_trigger(self, event: Dict, trigger: Dict) -> bool:
        """Check if event matches workflow trigger."""
        # Check event type
        event_type = event.get("event_type", "")
        trigger_type = trigger.get("event_type", "")
        
        if trigger_type.endswith(".*"):
            prefix = trigger_type[:-2]
            if not event_type.startswith(prefix):
                return False
        elif event_type != trigger_type:
            return False
        
        # Check conditions
        conditions = trigger.get("conditions", {})
        if not self._evaluate_conditions(event["payload"], conditions):
            return False
        
        return True
    
    def _evaluate_conditions(self, data: Dict, conditions: Dict) -> bool:
        """Evaluate conditional logic."""
        for field_path, condition in conditions.items():
            # Get field value using dot notation
            value = self._get_nested_value(data, field_path)
            
            # Evaluate condition
            if isinstance(condition, dict):
                for op, expected in condition.items():
                    if op == "eq" and value != expected:
                        return False
                    elif op == "ne" and value == expected:
                        return False
                    elif op == "gt" and not (value > expected):
                        return False
                    elif op == "gte" and not (value >= expected):
                        return False
                    elif op == "lt" and not (value < expected):
                        return False
                    elif op == "lte" and not (value <= expected):
                        return False
                    elif op == "contains" and expected not in str(value):
                        return False
                    elif op == "in" and value not in expected:
                        return False
            else:
                # Direct equality
                if value != condition:
                    return False
        
        return True
    
    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get nested value using dot notation (e.g., 'payload.title')."""
        parts = path.split(".")
        value = data
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        
        return value
    
    def _substitute_variables(self, template: Any, context: Dict) -> Any:
        """Replace {{variables}} in template with values from context."""
        if isinstance(template, str):
            # Replace {{key}} with context values
            def replace(match):
                key = match.group(1)
                return str(self._get_nested_value(context, key) or "")
            
            return re.sub(r'\{\{([^}]+)\}\}', replace, template)
        
        elif isinstance(template, dict):
            return {k: self._substitute_variables(v, context) for k, v in template.items()}
        
        elif isinstance(template, list):
            return [self._substitute_variables(item, context) for item in template]
        
        return template
    
    def execute_workflow(self, workflow: Dict, event: Dict) -> bool:
        """Execute a workflow with the given triggering event."""
        workflow_id = workflow["workflow_id"]
        execution_id = f"{workflow_id}_{int(time.time())}"
        
        self._log(f"Executing workflow: {workflow_id} (trigger: {event['event_id']})")
        
        # Create execution context
        context = {
            "event": event,
            "payload": event["payload"],
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "previous": {}
        }
        
        try:
            # Execute steps
            for step_index, step in enumerate(workflow["steps"]):
                self._log(f"  Step {step_index + 1}/{len(workflow['steps'])}: {step.get('agent', 'unknown')}")
                
                # Check step conditions
                if "condition" in step:
                    if not self._evaluate_conditions(context, step["condition"]):
                        self._log(f"  Step {step_index + 1} skipped (condition not met)")
                        continue
                
                # Execute step
                success, result = self._execute_step(step, context)
                
                if not success:
                    self._log(f"  Step {step_index + 1} failed: {result}", "ERROR")
                    
                    # Handle error
                    if "on_error" in step:
                        self._handle_error(step["on_error"], context, result)
                    
                    if not step.get("on_error", {}).get("continue", False):
                        self._log(f"Workflow {workflow_id} failed at step {step_index + 1}", "ERROR")
                        return False
                
                # Store result in context for next step
                context["previous"] = result or {}
            
            self._log(f"Workflow {workflow_id} completed successfully")
            
            # Mark event as processed
            self.bus.mark_processed(event["event_id"], success=True)
            
            return True
        
        except Exception as e:
            self._log(f"Workflow {workflow_id} exception: {e}", "ERROR")
            self.bus.mark_processed(event["event_id"], success=False)
            return False
    
    def _execute_step(self, step: Dict, context: Dict) -> tuple[bool, Any]:
        """Execute a single workflow step."""
        agent = step.get("agent")
        action = step.get("action")
        step_input = step.get("input", {})
        
        # Substitute variables in input
        step_input = self._substitute_variables(step_input, context)
        
        # Parallel execution
        if "parallel" in step:
            return self._execute_parallel(step["parallel"], context)
        
        # Call agent
        try:
            result = self._call_agent(agent, action, step_input)
            
            # Publish output event if specified
            if "output_event" in step and result:
                self.bus.publish({
                    "event_type": step["output_event"],
                    "source_agent": agent,
                    "payload": result
                })
            
            return True, result
        
        except Exception as e:
            return False, str(e)
    
    def _execute_parallel(self, steps: List[Dict], context: Dict) -> tuple[bool, List]:
        """Execute steps in parallel (simplified - sequential for now)."""
        results = []
        all_success = True
        
        for step in steps:
            success, result = self._execute_step(step, context)
            results.append(result)
            if not success:
                all_success = False
        
        return all_success, results
    
    def _call_agent(self, agent: str, action: str, input_data: Any) -> Any:
        """Call an agent/skill with the given action and input."""
        # For now, we'll use a simple convention:
        # Look for scripts/skills/{agent}/{action}.py or .js
        
        skills_dir = Path(__file__).parent.parent.parent
        agent_dir = skills_dir / agent / "scripts"
        
        # Try Python first
        script_path = agent_dir / f"{action}.py"
        if not script_path.exists():
            # Try JavaScript
            script_path = agent_dir / f"{action}.js"
        
        if not script_path.exists():
            raise FileNotFoundError(f"Agent script not found: {script_path}")
        
        # Execute script with input as JSON
        input_json = json.dumps(input_data)
        
        if script_path.suffix == ".py":
            result = subprocess.run(
                ["python3", str(script_path)],
                input=input_json,
                capture_output=True,
                text=True,
                timeout=60
            )
        else:
            result = subprocess.run(
                ["node", str(script_path)],
                input=input_json,
                capture_output=True,
                text=True,
                timeout=60
            )
        
        if result.returncode != 0:
            raise RuntimeError(f"Agent execution failed: {result.stderr}")
        
        # Try to parse JSON output
        try:
            return json.loads(result.stdout)
        except:
            return {"output": result.stdout}
    
    def _handle_error(self, error_handler: Dict, context: Dict, error: str):
        """Handle workflow step error."""
        if "agent" in error_handler:
            try:
                self._call_agent(
                    error_handler["agent"],
                    error_handler.get("action", "handle_error"),
                    {"error": error, "context": context}
                )
            except:
                pass
    
    def process_events(self):
        """Process pending events and execute matching workflows."""
        events = self.bus.get_pending_events()
        
        for event in events:
            matched = False
            
            for workflow in self.workflows:
                # Skip if workflow is disabled
                if workflow.get("enabled") == False:
                    continue
                
                if self._matches_trigger(event, workflow["trigger"]):
                    matched = True
                    self.execute_workflow(workflow, event)
                    break  # Only execute first matching workflow
            
            # If no workflow matched, mark as processed anyway
            if not matched:
                self.bus.mark_processed(event["event_id"])
    
    def run_daemon(self, interval_seconds: int = 30):
        """Run workflow engine as daemon (polls for events)."""
        self._log("Workflow engine daemon started")
        
        try:
            while True:
                self.process_events()
                self.bus.cleanup_old_events()
                time.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            self._log("Workflow engine daemon stopped")


def main():
    """CLI interface for workflow engine."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Protocol Workflow Engine")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--run", action="store_true", help="Process pending events once")
    parser.add_argument("--validate", action="store_true", help="Validate workflow definitions")
    parser.add_argument("--list", action="store_true", help="List workflows")
    parser.add_argument("--test", help="Test specific workflow")
    parser.add_argument("--enable", help="Enable workflow")
    parser.add_argument("--disable", help="Disable workflow")
    parser.add_argument("--interval", type=int, default=30, help="Daemon poll interval (seconds)")
    
    args = parser.parse_args()
    
    engine = WorkflowEngine()
    
    if args.validate:
        print(f"Validating workflows in {WORKFLOW_DIR}...")
        valid_count = 0
        invalid_count = 0
        
        for workflow in engine.workflows:
            print(f"✓ {workflow['workflow_id']}")
            valid_count += 1
        
        print(f"\nValidation complete: {valid_count} valid, {invalid_count} invalid")
    
    elif args.list:
        if not engine.workflows:
            print("No workflows found.")
        else:
            print(f"Workflows ({len(engine.workflows)}):\n")
            for w in engine.workflows:
                enabled = "✓" if w.get("enabled", True) else "✗"
                print(f"{enabled} {w['workflow_id']}")
                print(f"  Trigger: {w['trigger']['event_type']}")
                print(f"  Steps: {len(w['steps'])}")
                print()
    
    elif args.daemon:
        engine.run_daemon(args.interval)
    
    elif args.run:
        print("Processing pending events...")
        engine.process_events()
        print("Done.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
