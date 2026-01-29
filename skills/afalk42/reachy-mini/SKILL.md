---
name: reachy-mini
description: Control a Reachy Mini robot (by Pollen Robotics / Hugging Face) via its REST API and SSH. Use for any request involving the Reachy Mini robot — moving the head, body, or antennas; playing emotions or dances; capturing camera snapshots; adjusting volume; managing apps; checking robot status; or any physical robot interaction. The robot has a 6-DoF head, 360° body rotation, two animated antennas, a wide-angle camera (with non-disruptive WebRTC snapshot), 4-mic array, and speaker.
---

# Reachy Mini Robot Control

## Quick Start

Use the CLI script or `curl` to control the robot. The script lives at:
```
~/clawd/skills/reachy-mini/scripts/reachy.sh
```

Set the robot IP via `REACHY_HOST` env var or `--host` flag. Default: `192.168.8.17`.

### Common Commands
```bash
reachy.sh status                    # Daemon status, version, IP
reachy.sh state                     # Full robot state
reachy.sh wake-up                   # Wake the robot
reachy.sh sleep                     # Put to sleep
reachy.sh snap                      # Camera snapshot → /tmp/reachy_snap.jpg
reachy.sh snap /path/to/photo.jpg   # Snapshot to custom path
reachy.sh play-emotion cheerful1    # Play an emotion
reachy.sh play-dance groovy_sway_and_roll  # Play a dance
reachy.sh goto --head 0.2,0,0 --duration 1.5  # Nod down
reachy.sh volume-set 70             # Set speaker volume
reachy.sh emotions                  # List all emotions
reachy.sh dances                    # List all dances
```

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `REACHY_HOST` | `192.168.8.17` | Robot IP address |
| `REACHY_PORT` | `8000` | REST API port |
| `REACHY_SSH_USER` | `pollen` | SSH username (for `snap` command) |
| `REACHY_SSH_PASS` | `root` | SSH password (for `snap` command, uses `sshpass`) |

## Movement Guide

### Head Control (6 DoF)
The head accepts pitch, yaw, roll in **radians**:
- **Pitch** (look up/down): -0.5 (up) to 0.5 (down)
- **Yaw** (look left/right): -0.8 (right) to 0.8 (left)
- **Roll** (tilt sideways): -0.5 to 0.5

```bash
# Look up
reachy.sh goto --head -0.3,0,0 --duration 1.0

# Look left
reachy.sh goto --head 0,0.4,0 --duration 1.0

# Tilt head right, look slightly up
reachy.sh goto --head -0.1,0,-0.3 --duration 1.5

# Return to neutral
reachy.sh goto --head 0,0,0 --duration 1.0
```

### Body Rotation (360°)
Body yaw in radians. 0 = forward, positive = left, negative = right.
```bash
reachy.sh goto --body 1.57 --duration 2.0   # Turn 90° left
reachy.sh goto --body -1.57 --duration 2.0  # Turn 90° right
reachy.sh goto --body 0 --duration 2.0      # Face forward
```

### Antennas
Two antennas [left, right] in radians. Range ~-0.5 to 0.5.
```bash
reachy.sh goto --antennas 0.4,0.4 --duration 0.5    # Both up
reachy.sh goto --antennas -0.3,-0.3 --duration 0.5   # Both down
reachy.sh goto --antennas 0.4,-0.4 --duration 0.5    # Asymmetric
```

### Combined Movements
```bash
# Look left and turn body left with antennas up
reachy.sh goto --head 0,0.3,0 --body 0.5 --antennas 0.4,0.4 --duration 2.0
```

### Interpolation Modes
Use `--interp` with goto:
- `minjerk` — Smooth, natural (default)
- `linear` — Constant speed
- `ease` — Ease in/out
- `cartoon` — Bouncy, exaggerated

## Emotions & Dances

### Playing Emotions
80+ pre-recorded expressive animations. Select contextually appropriate ones:
```bash
reachy.sh play-emotion curious1       # Curious look
reachy.sh play-emotion cheerful1      # Happy expression
reachy.sh play-emotion surprised1     # Surprise reaction
reachy.sh play-emotion thoughtful1    # Thinking pose
reachy.sh play-emotion welcoming1     # Greeting gesture
reachy.sh play-emotion yes1           # Nodding yes
reachy.sh play-emotion no1            # Shaking no
```

### Playing Dances
19 dance moves, great for fun or celebration:
```bash
reachy.sh play-dance groovy_sway_and_roll
reachy.sh play-dance chicken_peck
reachy.sh play-dance dizzy_spin
```

### Full Lists
Run `reachy.sh emotions` or `reachy.sh dances` to see all available moves.

## Motor Modes

Before movement, motors must be `enabled`. Check with `reachy.sh motors`.

```bash
reachy.sh motors-enable     # Enable (needed for movement commands)
reachy.sh motors-disable    # Disable (robot goes limp)
reachy.sh motors-gravity    # Gravity compensation (manually pose the robot)
```

## Volume Control
```bash
reachy.sh volume            # Current speaker volume
reachy.sh volume-set 50     # Set speaker to 50%
reachy.sh volume-test       # Play test sound
reachy.sh mic-volume        # Microphone level
reachy.sh mic-volume-set 80 # Set microphone to 80%
```

## App Management

Reachy Mini runs HuggingFace Space apps. Manage them via:
```bash
reachy.sh apps              # List all available apps
reachy.sh apps-installed    # Installed apps only
reachy.sh app-status        # What's running now
reachy.sh app-start NAME    # Start an app
reachy.sh app-stop          # Stop current app
```

**Important**: Only one app runs at a time. Starting a new app stops the current one. Apps may take exclusive control of the robot — stop the running app before sending manual movement commands if the robot doesn't respond.

## Camera Snapshots

Capture JPEG photos from the robot's camera (IMX708 wide-angle) via WebRTC — **non-disruptive** to the running daemon.

```bash
reachy.sh snap                        # Save to /tmp/reachy_snap.jpg
reachy.sh snap /path/to/output.jpg    # Custom output path
```

**Requirements**: SSH access to the robot (uses `sshpass` + `REACHY_SSH_PASS` env var, default: `root`).

**How it works**: Connects to the daemon's WebRTC signalling server (port 8443) using GStreamer's `webrtcsrc` plugin on the robot, captures one H264-decoded frame, and saves as JPEG. No daemon restart, no motor disruption.

**Note**: The robot must be **awake** (head up) for a useful image. If asleep, the camera faces into the body. Run `reachy.sh wake-up` first.

## Audio Sensing
```bash
reachy.sh doa               # Direction of Arrival from mic array
```
Returns angle in radians (0=left, π/2=front, π=right) and speech detection boolean.

## Contextual Reactions (Clawdbot Integration)

Use `reachy-react.sh` to trigger contextual robot behaviors from heartbeats, cron jobs, or session responses.

```
~/clawd/skills/reachy-mini/scripts/reachy-react.sh
```

### Reactions
```bash
reachy-react.sh ack           # Nod acknowledgment (received a request)
reachy-react.sh success       # Cheerful emotion (task done)
reachy-react.sh alert         # Surprised + antennas up (urgent email, alert)
reachy-react.sh remind        # Welcoming/curious (meeting reminder, to-do)
reachy-react.sh idle          # Subtle animation (heartbeat presence)
reachy-react.sh morning       # Wake up + greeting (morning briefing)
reachy-react.sh goodnight     # Sleepy emotion + sleep (night mode)
reachy-react.sh patrol        # Camera snapshot, prints image path
reachy-react.sh doa-track     # Turn head toward detected sound source
reachy-react.sh celebrate     # Random dance (fun moments)
```

Pass `--bg` to run in background (non-blocking).

### Built-in Behaviors
- **Quiet hours** (22:00–06:29 ET): All reactions except `morning`, `goodnight`, and `patrol` are silently skipped.
- **Auto-wake**: Reactions ensure the robot is awake before acting (starts daemon + wakes if needed).
- **Fault-tolerant**: If robot is unreachable, reactions exit cleanly without errors.

### Integration Points

| Trigger | Reaction | Notes |
|---------|----------|-------|
| Morning briefing cron (6:30 AM) | `morning` | Robot wakes up and greets |
| Goodnight cron (10:00 PM) | `goodnight` | Robot plays sleepy emotion, goes to sleep |
| Heartbeat (periodic) | `idle` | Subtle head tilt, antenna wave, or look-around |
| Heartbeat (~1 in 4) | `doa-track` | Checks for nearby speech, turns toward it |
| Heartbeat (~1 in 6) | `patrol` | Camera snapshot for room awareness |
| Important unread email | `alert` | Antennas up + surprised emotion |
| Meeting <2h away | `remind` | Welcoming/curious emotion |
| Request from Alexander | `ack` | Quick head nod |
| Task completed | `success` | Random cheerful/happy emotion |
| Good news or celebration | `celebrate` | Random dance move |

### DOA (Direction of Arrival) Tracking

The `doa-track` reaction uses the robot's 4-mic array to detect speech direction and turn the head toward the speaker. The DOA angle (0=left, π/2=front, π=right) is mapped to head yaw. Only triggers when speech is actively detected.

### Camera Patrol

The `patrol` reaction captures a snapshot and prints the image path. Use this during heartbeats to check the room periodically. Combine with image analysis to detect activity or changes.

## Direct API Access

For anything not covered by the CLI, use `curl` or the `raw` command:
```bash
# Via raw command
reachy.sh raw GET /api/state/full
reachy.sh raw POST /api/move/goto '{"duration":1.0,"head_pose":{"pitch":0.2,"yaw":0,"roll":0}}'

# Via curl directly
curl -s http://192.168.8.17:8000/api/state/full | jq
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"duration":1.5,"head_pose":{"pitch":0,"yaw":0.3,"roll":0}}' \
  http://192.168.8.17:8000/api/move/goto
```

## Reference

For the complete API endpoint list, schemas (GotoModelRequest, FullBodyTarget, XYZRPYPose), and full emotion/dance catalogs, see [references/api-reference.md](references/api-reference.md).

## Troubleshooting

- **Robot doesn't move**: Check `reachy.sh motors` — must be `enabled`. Run `reachy.sh motors-enable`.
- **No response**: Check `reachy.sh status`. State should be `running`. If not, run `reachy.sh reboot-daemon`.
- **Movements ignored**: An app may have exclusive control. Run `reachy.sh app-stop` first.
- **Network unreachable**: Verify the robot IP with `ping $REACHY_HOST`. Check `reachy.sh wifi-status`.
- **Snap shows black image**: Robot is likely asleep (head down). Run `reachy.sh wake-up` first.
- **Snap fails with SSH error**: Ensure `sshpass` is installed and `REACHY_SSH_PASS` is set correctly.
