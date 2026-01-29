# Task Chunking for ADHD Brains

## The Problem

- Large tasks feel overwhelming → procrastination
- ADHD brains need quick wins for dopamine
- Unclear scope → analysis paralysis

## The Solution: Micro-tasks with Immediate Feedback

```yaml
# Task Chunking Protocol

Bad Task (too vague):
  "Implement user authentication system"

  Problems:
    - No clear starting point
    - Feels overwhelming
    - Success undefined

Good Task Breakdown:
  1. [15 min] Research auth libraries (Devise vs custom JWT)
  2. [30 min] Set up User model with password_digest
  3. [45 min] Create login/logout routes
  4. [30 min] Add session management
  5. [20 min] Write tests for auth flow
  6. [DOPAMINE HIT] Deploy to staging and test manually

  Benefits:
    - Each task < 1 hour (maintains focus)
    - Clear success criteria
    - Frequent completion dopamine
    - Can hyperfocus on single chunk

Visual Progress:
  Use task board with:
    - Big visible progress bar
    - Celebration animations on completion
    - Streak tracking ("5 tasks in a row!")
    - Level-up system (gamification)
```

## Implementation: ADHD Task Chunker

```python
class ADHDTaskChunker:
    MAX_CHUNK_DURATION = 60  # minutes
    MIN_CHUNK_DURATION = 10  # minutes

    @staticmethod
    def chunk_task(task_description: str, estimated_hours: float) -> list[dict]:
        """Break large task into ADHD-friendly chunks"""

        if estimated_hours <= 1:
            return [{
                'name': task_description,
                'duration_min': int(estimated_hours * 60),
                'dopamine_reward': '🎉'
            }]

        # For larger tasks, decompose
        chunks = []
        total_minutes = int(estimated_hours * 60)

        # Rule: Each chunk should build toward visible progress
        phases = [
            ('Research & Planning', 0.15),  # 15% of time
            ('Setup & Scaffolding', 0.20),  # 20%
            ('Core Implementation', 0.40),  # 40%
            ('Polish & Edge Cases', 0.15),  # 15%
            ('Testing & Documentation', 0.10)  # 10%
        ]

        for phase_name, phase_ratio in phases:
            phase_duration = int(total_minutes * phase_ratio)

            # Break phase into 30-45min chunks
            num_chunks = max(1, phase_duration // 40)
            chunk_duration = phase_duration // num_chunks

            for i in range(num_chunks):
                chunks.append({
                    'name': f"{task_description} - {phase_name} ({i+1}/{num_chunks})",
                    'duration_min': chunk_duration,
                    'phase': phase_name,
                    'dopamine_reward': '✅' if i == num_chunks - 1 else '⏭️'
                })

        return chunks

    @staticmethod
    def optimize_for_hyperfocus(chunks: list[dict]) -> dict:
        """Group chunks into hyperfocus-friendly sessions"""

        sessions = []
        current_session = []
        session_duration = 0

        for chunk in chunks:
            # If adding this chunk exceeds 3 hours, start new session
            if session_duration + chunk['duration_min'] > 180:
                sessions.append({
                    'chunks': current_session,
                    'total_duration': session_duration,
                    'break_after': True
                })
                current_session = []
                session_duration = 0

            current_session.append(chunk)
            session_duration += chunk['duration_min']

        # Add final session
        if current_session:
            sessions.append({
                'chunks': current_session,
                'total_duration': session_duration,
                'break_after': True
            })

        return {'sessions': sessions, 'estimated_days': len(sessions) // 2}
```

## Usage Example

```python
# Usage
task = "Build user authentication system"
chunks = ADHDTaskChunker.chunk_task(task, estimated_hours=8)
plan = ADHDTaskChunker.optimize_for_hyperfocus(chunks)

print(f"📋 Task Plan for: {task}")
for i, session in enumerate(plan['sessions'], 1):
    print(f"\n🔥 Hyperfocus Session {i} (~{session['total_duration']}min):")
    for chunk in session['chunks']:
        print(f"  {chunk['dopamine_reward']} {chunk['name']} ({chunk['duration_min']}min)")
    if session['break_after']:
        print("  ☕ MANDATORY BREAK")
```

## Output Example

```
📋 Task Plan for: Build user authentication system

🔥 Hyperfocus Session 1 (~168min):
  ⏭️ Build user authentication system - Research & Planning (1/1) (72min)
  ⏭️ Build user authentication system - Setup & Scaffolding (1/2) (48min)
  ✅ Build user authentication system - Setup & Scaffolding (2/2) (48min)
  ☕ MANDATORY BREAK

🔥 Hyperfocus Session 2 (~168min):
  ⏭️ Build user authentication system - Core Implementation (1/4) (48min)
  ⏭️ Build user authentication system - Core Implementation (2/4) (48min)
  ⏭️ Build user authentication system - Core Implementation (3/4) (48min)
  ☕ MANDATORY BREAK

🔥 Hyperfocus Session 3 (~120min):
  ✅ Build user authentication system - Core Implementation (4/4) (48min)
  ✅ Build user authentication system - Polish & Edge Cases (1/1) (72min)
  ☕ MANDATORY BREAK

🔥 Hyperfocus Session 4 (~48min):
  ✅ Build user authentication system - Testing & Documentation (1/1) (48min)
  ☕ MANDATORY BREAK
```

## Visual Progress Board

```
┌────────────────────────────────────────────────────────────┐
│ 🎯 USER AUTH SYSTEM                        Progress: 62%   │
│ ████████████████████░░░░░░░░░░░░                          │
│                                                            │
│ Session 1 ✅  Session 2 ✅  Session 3 🔄  Session 4 ⏳     │
│                                                            │
│ Current: Core Implementation (3/4)                         │
│ Time remaining: ~48min                                     │
│                                                            │
│ 🔥 Streak: 5 chunks completed!                            │
│ 💪 Energy: ████████░░ 80%                                 │
└────────────────────────────────────────────────────────────┘
```
