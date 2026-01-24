# Workout Templates Reference

The v2.0 plan format uses workout templates to dramatically reduce verbosity. Instead of specifying full workout objects with structure, paces, and descriptions, you reference templates that expand automatically.

## How Templates Work

### Basic Syntax

```yaml
# Template reference syntax
workouts:
  Mon: rest # No parameters
  Tue: easy(40) # Single parameter
  Wed: tempo(20, 10, 10) # Multiple parameters
  Thu: swim.threshold(10) # Sport-prefixed template
```

### Template Resolution

1. **Running templates** (default): Use template name directly
   - `easy(40)` → `templates/run/easy.yaml`
   - `intervals.400(6)` → `templates/run/intervals.400.yaml`

2. **Other sports**: Use sport prefix
   - `swim.threshold(10)` → `templates/swim/threshold.yaml`
   - `bike.sweetspot(60)` → `templates/bike/sweetspot.yaml`
   - `brick.olympic(90, 30)` → `templates/brick/olympic.yaml`
   - `strength.core(15)` → `templates/strength/core.yaml`

### Parameter Passing

Parameters are passed in order matching the template's `params` definition:

```yaml
# Template definition (tempo.yaml)
params:
  tempo_mins:
    type: int
    required: true
  warmup_mins:
    type: int
    default: 10
  cooldown_mins:
    type: int
    default: 10

# Usage examples
tempo(20)           # tempo_mins=20, warmup=10, cooldown=10 (defaults)
tempo(25, 15, 10)   # tempo_mins=25, warmup=15, cooldown=10
```

### Variable Interpolation

Templates use `${variable}` syntax for dynamic values:

```yaml
# In template definition
pace: "${paces.tempo}"
duration: "${duration}min"
estimatedDuration: "${warmup_mins + tempo_mins + cooldown_mins}"

# Athlete's paces are injected from the plan
paces:
  tempo: "8:15/mi"
```

---

## Complete Template Reference

### Running Templates

Located in `templates/run/`

| Template                     | File                | Required Params   | Optional Params            | Description                  |
| ---------------------------- | ------------------- | ----------------- | -------------------------- | ---------------------------- |
| `rest`                       | rest.yaml           | -                 | -                          | Complete rest day            |
| `easy(duration)`             | easy.yaml           | duration (mins)   | -                          | Zone 2 easy run              |
| `recovery(duration)`         | recovery.yaml       | duration (mins)   | -                          | Zone 1 recovery run          |
| `long(duration)`             | long.yaml           | duration (mins)   | -                          | Long run, progressive finish |
| `tempo(tempo_mins)`          | tempo.yaml          | tempo_mins        | warmup_mins, cooldown_mins | Continuous tempo at T pace   |
| `threshold(threshold_mins)`  | threshold.yaml      | threshold_mins    | warmup_mins, cooldown_mins | Threshold-pace running       |
| `intervals.400(reps)`        | intervals.400.yaml  | reps              | recovery                   | 400m repeats at R pace       |
| `intervals.800(reps)`        | intervals.800.yaml  | reps              | recovery                   | 800m repeats at I pace       |
| `intervals.1k(reps)`         | intervals.1k.yaml   | reps              | recovery                   | 1K repeats at I pace         |
| `intervals.mile(reps)`       | intervals.mile.yaml | reps              | recovery                   | Mile repeats at T pace       |
| `fartlek(duration)`          | fartlek.yaml        | duration (mins)   | -                          | Unstructured speed play      |
| `progression(duration)`      | progression.yaml    | duration (mins)   | -                          | Easy → tempo progression     |
| `strides(duration, strides)` | strides.yaml        | duration, strides | -                          | Easy run with strides        |
| `hills(reps)`                | hills.yaml          | reps              | -                          | Hill repeats                 |
| `race.5k`                    | race.5k.yaml        | -                 | -                          | 5K race day                  |

**Required Paces for Running:**

- `paces.easy` - Used by: easy, recovery, long, warmups/cooldowns
- `paces.tempo` - Used by: tempo
- `paces.threshold` - Used by: threshold
- `paces.long` - Used by: long
- `paces.r400` - Used by: intervals.400
- `paces.r800` - Used by: intervals.800
- `paces.r1k` - Used by: intervals.1k
- `paces.rMile` - Used by: intervals.mile

### Swimming Templates

Located in `templates/swim/`

| Template                   | File           | Required Params | Optional Params | Description              |
| -------------------------- | -------------- | --------------- | --------------- | ------------------------ |
| `swim.rest`                | rest.yaml      | -               | -               | Rest day                 |
| `swim.easy(duration)`      | easy.yaml      | duration (mins) | -               | Zone 2 continuous swim   |
| `swim.technique(duration)` | technique.yaml | duration (mins) | -               | Drill-focused session    |
| `swim.aerobic(reps)`       | aerobic.yaml   | reps (400m)     | rest_secs       | 400m @ CSS+10s repeats   |
| `swim.threshold(reps)`     | threshold.yaml | reps (100m)     | rest_secs       | 100m @ CSS repeats       |
| `swim.vo2max(reps)`        | vo2max.yaml    | reps (100m)     | rest_secs       | 100m @ CSS-5s repeats    |
| `swim.openwater(duration)` | openwater.yaml | duration (mins) | -               | Open water with sighting |

**Required Paces for Swimming:**

- `paces.css` - Critical Swim Speed (e.g., "1:45/100m")
- `paces.swim_easy` - Easy swim pace (e.g., "2:00/100m")

### Cycling Templates

Located in `templates/bike/`

| Template                   | File            | Required Params | Optional Params                  | Description            |
| -------------------------- | --------------- | --------------- | -------------------------------- | ---------------------- |
| `bike.rest`                | rest.yaml       | -               | -                                | Rest day               |
| `bike.easy(duration)`      | easy.yaml       | duration (mins) | -                                | Zone 1-2 easy spin     |
| `bike.endurance(duration)` | endurance.yaml  | duration (mins) | -                                | Zone 2 endurance       |
| `bike.tempo(tempo_mins)`   | tempo.yaml      | tempo_mins      | sets, warmup_mins, cooldown_mins | 76-90% FTP             |
| `bike.sweetspot(ss_mins)`  | sweetspot.yaml  | ss_mins         | sets, warmup_mins, cooldown_mins | 88-93% FTP             |
| `bike.threshold(reps)`     | threshold.yaml  | reps            | interval_mins, rest_mins         | 95-105% FTP intervals  |
| `bike.vo2max(reps)`        | vo2max.yaml     | reps            | interval_mins, rest_mins         | 106-120% FTP intervals |
| `bike.overunders(sets)`    | overunders.yaml | sets            | cycles_per_set                   | Threshold extension    |
| `bike.hills(reps)`         | hills.yaml      | reps            | climb_mins                       | Hill repeat climbs     |

**Required Zones for Cycling:**

- `zones.power.ftp` - Functional Threshold Power in watts

### Brick Templates

Located in `templates/brick/`

| Template                                | File             | Required Params     | Description            |
| --------------------------------------- | ---------------- | ------------------- | ---------------------- |
| `brick.sprint(bike_mins, run_mins)`     | sprint.yaml      | bike_mins, run_mins | Sprint tri simulation  |
| `brick.olympic(bike_mins, run_mins)`    | olympic.yaml     | bike_mins, run_mins | Olympic tri simulation |
| `brick.halfironman(bike_hrs, run_mins)` | halfironman.yaml | bike_hrs, run_mins  | 70.3 simulation        |
| `brick.ironman(bike_hrs, run_mins)`     | ironman.yaml     | bike_hrs, run_mins  | Ironman simulation     |

### Strength Templates

Located in `templates/strength/`

| Template                         | File             | Required Params | Description                   |
| -------------------------------- | ---------------- | --------------- | ----------------------------- |
| `strength.foundation(duration)`  | foundation.yaml  | duration (mins) | Bodyweight, base phase        |
| `strength.full(duration)`        | full.yaml        | duration (mins) | Complete session, build phase |
| `strength.maintenance(duration)` | maintenance.yaml | duration (mins) | Light, taper/race week        |
| `strength.core(duration)`        | core.yaml        | duration (mins) | Core-focused session          |

---

## Template File Structure

Each template is a YAML file with this structure:

```yaml
id: tempo # Template identifier
name: Tempo Run # Display name
sport: run # Sport type
type: tempo # Workout type
category: tempo # Workout category

params: # Configurable parameters
  tempo_mins:
    type: int
    required: true
    default: 20
    min: 10
    max: 45
    description: Duration of tempo section in minutes
  warmup_mins:
    type: int
    default: 10
    description: Warmup duration in minutes

structure: # Workout structure
  warmup:
    - type: warmup
      name: Easy warmup
      duration: "${warmup_mins}min"
      pace: "${paces.easy}"
  main:
    - type: work
      name: Tempo
      duration: "${tempo_mins}min"
      pace: "${paces.tempo}"
      intensity: Zone 3-4
  cooldown:
    - type: cooldown
      name: Easy cooldown
      duration: "${cooldown_mins}min"
      pace: "${paces.easy}"

humanReadable: | # Coach-friendly text output
  TEMPO RUN

  WARM-UP: ${warmup_mins} min easy @ ${paces.easy}

  MAIN SET:
  ${tempo_mins} min @ tempo pace (${paces.tempo})

  COOL-DOWN: ${cooldown_mins} min easy

estimatedDuration: "${warmup_mins + tempo_mins + cooldown_mins}"
targetZone: Z3-Z4
rpe: "6-7"
notes: Builds lactate threshold and race-pace feel
```

---

## Creating Custom Templates

To add a custom template:

1. Create a YAML file in the appropriate `templates/{sport}/` directory
2. Follow the structure above
3. Define params with types, defaults, and constraints
4. Use `${variable}` interpolation for dynamic values
5. Test with `npx endurance-coach templates show your-template`

**Available interpolation variables:**

- `${param_name}` - Any defined parameter
- `${paces.X}` - Athlete's pace values
- `${zones.X}` - Athlete's zone values
- Math expressions: `${warmup + main + cooldown}`

---

## CLI Commands for Templates

```bash
# List all templates
npx endurance-coach templates

# Filter by sport
npx endurance-coach templates --sport run
npx endurance-coach templates --sport swim
npx endurance-coach templates --sport bike

# Show template details
npx endurance-coach templates show intervals.400
npx endurance-coach templates show swim.threshold

# Expand a plan to see full workouts
npx endurance-coach expand plan.yaml --verbose
```
