# Reachy Mini REST API Reference

Base URL: `http://<REACHY_HOST>:8000`

## Robot Anatomy & Coordinate System

Reachy Mini is a desktop robot (28cm tall, 1.5kg) with:
- **Head**: 6 DoF movement (x, y, z translation in meters; roll, pitch, yaw rotation in radians)
- **Body**: 360° rotation around vertical axis (yaw in radians)
- **Antennas**: 2 independently animated antennas (position in radians, ~-0.5 to 0.5 range)
- **Camera**: Wide-angle camera (in the head/eyes)
- **Microphones**: 4-mic array with Direction of Arrival detection
- **Speaker**: 5W speaker

### Head Pose (XYZRPYPose)
All values in radians unless noted. Typical useful ranges:
- `pitch`: -0.5 to 0.5 (negative = look up, positive = look down)
- `yaw`: -0.8 to 0.8 (negative = look right, positive = look left)
- `roll`: -0.5 to 0.5 (tilt head sideways)
- `x`, `y`, `z`: Translation in meters (small adjustments, typically ±0.02)

### Body Yaw
- Range: approximately -3.14 to 3.14 (full 360°)
- 0 = forward, positive = turn left, negative = turn right

### Antenna Positions
- Tuple of [left, right] in radians
- Typical range: -0.5 to 0.5
- 0 = neutral, negative/positive = different angles

## Interpolation Modes
Used in goto commands:
- `linear` — Constant speed
- `minjerk` — Smooth acceleration/deceleration (most natural, default)
- `ease` — Ease-in/ease-out
- `cartoon` — Exaggerated, bouncy motion

## Motor Control Modes
- `enabled` — Motors actively holding position and accepting commands
- `disabled` — Motors off, robot limp
- `gravity_compensation` — Motors compensate for gravity but allow manual manipulation

## Recorded Move Datasets

### Emotions (pollen-robotics/reachy-mini-emotions-library)
80+ expressive animations. Key emotions:
- **Positive**: cheerful1, enthusiastic1/2, loving1, grateful1, proud1/2/3, success1/2, relief1/2, serenity1
- **Negative**: sad1/2, angry (rage1, furious1), fear1, scared1, anxiety1, frustrated1, lonely1, exhausted1
- **Social**: welcoming1/2, attentive1/2, helpful1/2, understanding1/2, calming1, inquiring1/2/3
- **Reactive**: surprised1/2, amazed1, confused1, curious1, thoughtful1/2, uncertain1
- **Playful**: laughing1/2, oops1/2, dance1/2/3, electric1
- **Dismissive**: boredom1/2, contempt1, indifferent1, go_away1, irritated1/2, displeased1/2
- **Communication**: yes1, yes_sad1, no1, no_excited1, no_sad1, come1, reprimand1/2/3
- **States**: sleep1, tired1, dying1, shy1, lost1, uncomfortable1, resigned1, downcast1

### Dances (pollen-robotics/reachy-mini-dances-library)
19 dance moves:
side_glance_flick, jackson_square, side_peekaboo, groovy_sway_and_roll, chin_lead,
side_to_side_sway, neck_recoil, head_tilt_roll, simple_nod, uh_huh_tilt,
interwoven_spirals, pendulum_swing, chicken_peck, yeah_nod, stumble_and_recover,
dizzy_spin, grid_snap, polyrhythm_combo, sharp_side_tilt

## API Endpoints

### Daemon
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/daemon/status` | Robot name, state, version, IP, backend status |
| POST | `/api/daemon/start?wake_up=BOOL` | Start daemon |
| POST | `/api/daemon/stop?goto_sleep=BOOL` | Stop daemon |
| POST | `/api/daemon/restart` | Restart daemon |

### State
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/state/full` | Full state (head pose, body yaw, antennas, control mode) |
| GET | `/api/state/present_head_pose` | Current head pose (XYZRPYPose) |
| GET | `/api/state/present_body_yaw` | Current body yaw (radians) |
| GET | `/api/state/present_antenna_joint_positions` | Antenna positions [left, right] |
| GET | `/api/state/doa` | Direction of Arrival from mic array |

### Motors
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/motors/status` | Current motor mode |
| POST | `/api/motors/set_mode/{mode}` | Set mode: enabled, disabled, gravity_compensation |

### Movement
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/move/goto` | Animated move to target (body: GotoModelRequest) |
| POST | `/api/move/set_target` | Set target directly (body: FullBodyTarget) |
| POST | `/api/move/play/wake_up` | Wake up animation |
| POST | `/api/move/play/goto_sleep` | Sleep animation |
| POST | `/api/move/play/recorded-move-dataset/{dataset}/{move}` | Play recorded move |
| GET | `/api/move/recorded-move-datasets/list/{dataset}` | List moves in dataset |
| GET | `/api/move/running` | List running move tasks |
| POST | `/api/move/stop` | Stop a move (body: {"uuid": "..."}) |

#### GotoModelRequest Body
```json
{
  "head_pose": {"x": 0, "y": 0, "z": 0, "pitch": 0.0, "yaw": 0.0, "roll": 0.0},
  "body_yaw": 0.0,
  "antennas": [0.0, 0.0],
  "duration": 1.5,
  "interpolation": "minjerk"
}
```
All fields except `duration` are optional. Omitted fields keep current position.

#### FullBodyTarget Body
```json
{
  "target_head_pose": {"x": 0, "y": 0, "z": 0, "pitch": 0.0, "yaw": 0.0, "roll": 0.0},
  "target_body_yaw": 0.0,
  "target_antennas": [0.0, 0.0]
}
```

### Volume
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/volume/current` | Speaker volume (0-100) |
| POST | `/api/volume/set` | Set volume (body: {"volume": N}) |
| POST | `/api/volume/test-sound` | Play test sound |
| GET | `/api/volume/microphone/current` | Microphone volume |
| POST | `/api/volume/microphone/set` | Set mic volume (body: {"volume": N}) |

### Apps
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/apps/list-available` | All available apps |
| GET | `/api/apps/list-available/{source}` | Apps by source: hf_space, installed, local |
| POST | `/api/apps/install` | Install app (body: AppInfo JSON) |
| POST | `/api/apps/remove/{name}` | Remove installed app |
| POST | `/api/apps/start-app/{name}` | Start app by name |
| POST | `/api/apps/stop-current-app` | Stop running app |
| POST | `/api/apps/restart-current-app` | Restart running app |
| GET | `/api/apps/current-app-status` | Status of running app |
| GET | `/api/apps/job-status/{job_id}` | Install/remove job progress |

### WiFi
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/wifi/status` | Mode, connected network, known networks |
| POST | `/api/wifi/connect?ssid=X&password=Y` | Connect to network |
| POST | `/api/wifi/scan_and_list` | Scan available networks |
| POST | `/api/wifi/forget?ssid=X` | Forget a network |

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/update/available` | Check for firmware updates |
| POST | `/update/start` | Start firmware update |
| POST | `/health-check` | Health check ping |
| GET | `/api/kinematics/info` | Kinematics engine info |
| GET | `/api/kinematics/urdf` | URDF model of the robot |
