#!/usr/bin/env python3
"""
Ontology graph operations: create, query, relate, validate.

Usage:
    python ontology.py create --type Person --props '{"name":"Alice"}'
    python ontology.py get --id p_001
    python ontology.py query --type Task --where '{"status":"open"}'
    python ontology.py relate --from proj_001 --rel has_task --to task_001
    python ontology.py related --id proj_001 --rel has_task
    python ontology.py list --type Person
    python ontology.py delete --id p_001
    python ontology.py validate
"""

import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_GRAPH_PATH = "memory/ontology/graph.jsonl"
DEFAULT_SCHEMA_PATH = "memory/ontology/schema.yaml"


def generate_id(type_name: str) -> str:
    """Generate a unique ID for an entity."""
    prefix = type_name.lower()[:4]
    suffix = uuid.uuid4().hex[:8]
    return f"{prefix}_{suffix}"


def load_graph(path: str) -> tuple[dict, list]:
    """Load entities and relations from graph file."""
    entities = {}
    relations = []
    
    graph_path = Path(path)
    if not graph_path.exists():
        return entities, relations
    
    with open(graph_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            op = record.get("op")
            
            if op == "create":
                entity = record["entity"]
                entities[entity["id"]] = entity
            elif op == "update":
                entity_id = record["id"]
                if entity_id in entities:
                    entities[entity_id]["properties"].update(record.get("properties", {}))
                    entities[entity_id]["updated"] = record.get("timestamp")
            elif op == "delete":
                entity_id = record["id"]
                entities.pop(entity_id, None)
            elif op == "relate":
                relations.append({
                    "from": record["from"],
                    "rel": record["rel"],
                    "to": record["to"],
                    "properties": record.get("properties", {})
                })
            elif op == "unrelate":
                relations = [r for r in relations 
                           if not (r["from"] == record["from"] 
                                  and r["rel"] == record["rel"] 
                                  and r["to"] == record["to"])]
    
    return entities, relations


def append_op(path: str, record: dict):
    """Append an operation to the graph file."""
    graph_path = Path(path)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(graph_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def create_entity(type_name: str, properties: dict, graph_path: str, entity_id: str = None) -> dict:
    """Create a new entity."""
    entity_id = entity_id or generate_id(type_name)
    timestamp = datetime.now(timezone.utc).isoformat()
    
    entity = {
        "id": entity_id,
        "type": type_name,
        "properties": properties,
        "created": timestamp,
        "updated": timestamp
    }
    
    record = {"op": "create", "entity": entity, "timestamp": timestamp}
    append_op(graph_path, record)
    
    return entity


def get_entity(entity_id: str, graph_path: str) -> dict | None:
    """Get entity by ID."""
    entities, _ = load_graph(graph_path)
    return entities.get(entity_id)


def query_entities(type_name: str, where: dict, graph_path: str) -> list:
    """Query entities by type and properties."""
    entities, _ = load_graph(graph_path)
    results = []
    
    for entity in entities.values():
        if type_name and entity["type"] != type_name:
            continue
        
        match = True
        for key, value in where.items():
            if entity["properties"].get(key) != value:
                match = False
                break
        
        if match:
            results.append(entity)
    
    return results


def list_entities(type_name: str, graph_path: str) -> list:
    """List all entities of a type."""
    entities, _ = load_graph(graph_path)
    if type_name:
        return [e for e in entities.values() if e["type"] == type_name]
    return list(entities.values())


def update_entity(entity_id: str, properties: dict, graph_path: str) -> dict | None:
    """Update entity properties."""
    entities, _ = load_graph(graph_path)
    if entity_id not in entities:
        return None
    
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"op": "update", "id": entity_id, "properties": properties, "timestamp": timestamp}
    append_op(graph_path, record)
    
    entities[entity_id]["properties"].update(properties)
    entities[entity_id]["updated"] = timestamp
    return entities[entity_id]


def delete_entity(entity_id: str, graph_path: str) -> bool:
    """Delete an entity."""
    entities, _ = load_graph(graph_path)
    if entity_id not in entities:
        return False
    
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"op": "delete", "id": entity_id, "timestamp": timestamp}
    append_op(graph_path, record)
    return True


def create_relation(from_id: str, rel_type: str, to_id: str, properties: dict, graph_path: str):
    """Create a relation between entities."""
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "op": "relate",
        "from": from_id,
        "rel": rel_type,
        "to": to_id,
        "properties": properties,
        "timestamp": timestamp
    }
    append_op(graph_path, record)
    return record


def get_related(entity_id: str, rel_type: str, graph_path: str, direction: str = "outgoing") -> list:
    """Get related entities."""
    entities, relations = load_graph(graph_path)
    results = []
    
    for rel in relations:
        if direction == "outgoing" and rel["from"] == entity_id:
            if not rel_type or rel["rel"] == rel_type:
                if rel["to"] in entities:
                    results.append({
                        "relation": rel["rel"],
                        "entity": entities[rel["to"]]
                    })
        elif direction == "incoming" and rel["to"] == entity_id:
            if not rel_type or rel["rel"] == rel_type:
                if rel["from"] in entities:
                    results.append({
                        "relation": rel["rel"],
                        "entity": entities[rel["from"]]
                    })
        elif direction == "both":
            if rel["from"] == entity_id or rel["to"] == entity_id:
                if not rel_type or rel["rel"] == rel_type:
                    other_id = rel["to"] if rel["from"] == entity_id else rel["from"]
                    if other_id in entities:
                        results.append({
                            "relation": rel["rel"],
                            "direction": "outgoing" if rel["from"] == entity_id else "incoming",
                            "entity": entities[other_id]
                        })
    
    return results


def validate_graph(graph_path: str, schema_path: str) -> list:
    """Validate graph against schema constraints."""
    entities, relations = load_graph(graph_path)
    errors = []
    
    # Load schema if exists
    schema = {}
    schema_file = Path(schema_path)
    if schema_file.exists():
        import yaml
        with open(schema_file) as f:
            schema = yaml.safe_load(f) or {}
    
    type_schemas = schema.get("types", {})
    
    for entity_id, entity in entities.items():
        type_name = entity["type"]
        type_schema = type_schemas.get(type_name, {})
        
        # Check required properties
        required = type_schema.get("required", [])
        for prop in required:
            if prop not in entity["properties"]:
                errors.append(f"{entity_id}: missing required property '{prop}'")
        
        # Check forbidden properties
        forbidden = type_schema.get("forbidden_properties", [])
        for prop in forbidden:
            if prop in entity["properties"]:
                errors.append(f"{entity_id}: contains forbidden property '{prop}'")
        
        # Check enum values
        for prop, allowed in type_schema.items():
            if prop.endswith("_enum"):
                field = prop.replace("_enum", "")
                value = entity["properties"].get(field)
                if value and value not in allowed:
                    errors.append(f"{entity_id}: '{field}' must be one of {allowed}, got '{value}'")
    
    return errors


def main():
    parser = argparse.ArgumentParser(description="Ontology graph operations")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create
    create_p = subparsers.add_parser("create", help="Create entity")
    create_p.add_argument("--type", "-t", required=True, help="Entity type")
    create_p.add_argument("--props", "-p", default="{}", help="Properties JSON")
    create_p.add_argument("--id", help="Entity ID (auto-generated if not provided)")
    create_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Get
    get_p = subparsers.add_parser("get", help="Get entity by ID")
    get_p.add_argument("--id", required=True, help="Entity ID")
    get_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Query
    query_p = subparsers.add_parser("query", help="Query entities")
    query_p.add_argument("--type", "-t", help="Entity type")
    query_p.add_argument("--where", "-w", default="{}", help="Filter JSON")
    query_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # List
    list_p = subparsers.add_parser("list", help="List entities")
    list_p.add_argument("--type", "-t", help="Entity type")
    list_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Update
    update_p = subparsers.add_parser("update", help="Update entity")
    update_p.add_argument("--id", required=True, help="Entity ID")
    update_p.add_argument("--props", "-p", required=True, help="Properties JSON")
    update_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Delete
    delete_p = subparsers.add_parser("delete", help="Delete entity")
    delete_p.add_argument("--id", required=True, help="Entity ID")
    delete_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Relate
    relate_p = subparsers.add_parser("relate", help="Create relation")
    relate_p.add_argument("--from", dest="from_id", required=True, help="From entity ID")
    relate_p.add_argument("--rel", "-r", required=True, help="Relation type")
    relate_p.add_argument("--to", dest="to_id", required=True, help="To entity ID")
    relate_p.add_argument("--props", "-p", default="{}", help="Relation properties JSON")
    relate_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Related
    related_p = subparsers.add_parser("related", help="Get related entities")
    related_p.add_argument("--id", required=True, help="Entity ID")
    related_p.add_argument("--rel", "-r", help="Relation type filter")
    related_p.add_argument("--dir", "-d", choices=["outgoing", "incoming", "both"], default="outgoing")
    related_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # Validate
    validate_p = subparsers.add_parser("validate", help="Validate graph")
    validate_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    validate_p.add_argument("--schema", "-s", default=DEFAULT_SCHEMA_PATH)
    
    args = parser.parse_args()
    
    if args.command == "create":
        props = json.loads(args.props)
        entity = create_entity(args.type, props, args.graph, args.id)
        print(json.dumps(entity, indent=2))
    
    elif args.command == "get":
        entity = get_entity(args.id, args.graph)
        if entity:
            print(json.dumps(entity, indent=2))
        else:
            print(f"Entity not found: {args.id}")
    
    elif args.command == "query":
        where = json.loads(args.where)
        results = query_entities(args.type, where, args.graph)
        print(json.dumps(results, indent=2))
    
    elif args.command == "list":
        results = list_entities(args.type, args.graph)
        print(json.dumps(results, indent=2))
    
    elif args.command == "update":
        props = json.loads(args.props)
        entity = update_entity(args.id, props, args.graph)
        if entity:
            print(json.dumps(entity, indent=2))
        else:
            print(f"Entity not found: {args.id}")
    
    elif args.command == "delete":
        if delete_entity(args.id, args.graph):
            print(f"Deleted: {args.id}")
        else:
            print(f"Entity not found: {args.id}")
    
    elif args.command == "relate":
        props = json.loads(args.props)
        rel = create_relation(args.from_id, args.rel, args.to_id, props, args.graph)
        print(json.dumps(rel, indent=2))
    
    elif args.command == "related":
        results = get_related(args.id, args.rel, args.graph, args.dir)
        print(json.dumps(results, indent=2))
    
    elif args.command == "validate":
        errors = validate_graph(args.graph, args.schema)
        if errors:
            print("Validation errors:")
            for err in errors:
                print(f"  - {err}")
        else:
            print("Graph is valid.")


if __name__ == "__main__":
    main()
