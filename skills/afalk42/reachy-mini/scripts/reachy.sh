#!/usr/bin/env bash
# reachy.sh — Reachy Mini robot control CLI
# Usage: reachy.sh [--host HOST] <command> [args...]
# Requires: curl, jq
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REACHY_HOST="${REACHY_HOST:-192.168.8.17}"
REACHY_PORT="${REACHY_PORT:-8000}"
BASE=""  # set after arg parsing

usage() {
  cat <<'EOF'
Usage: reachy.sh [--host HOST] <command> [args...]

CONNECTION
  --host HOST          Override robot IP (default: $REACHY_HOST or 192.168.8.17)

STATUS & INFO
  status               Daemon status (name, state, version, IP)
  state                Full robot state (head pose, body yaw, antennas)
  motors               Motor control mode
  health               Send health-check ping

MOVEMENT
  wake-up              Wake the robot up (head rises, eyes open)
  sleep                Put the robot to sleep
  goto [options]       Move to a target pose
    --head PITCH,YAW,ROLL    Head orientation in radians (pitch,yaw,roll)
    --body YAW               Body rotation in radians
    --antennas LEFT,RIGHT    Antenna positions in radians
    --duration SECS          Movement duration (default: 1.5)
    --interp MODE            Interpolation: linear|minjerk|ease|cartoon (default: minjerk)
  set-target [options] Set target pose directly (continuous control)
    (same options as goto, except no duration/interp)
  stop-move UUID       Stop a running move by UUID
  running              List currently running moves

HEAD
  head-pose            Get current head pose (x,y,z,roll,pitch,yaw)

BODY
  body-yaw             Get current body yaw (radians)

ANTENNAS
  antennas             Get current antenna positions [left, right]

MOTORS
  motors-enable        Enable motor control
  motors-disable       Disable motor control
  motors-gravity       Set gravity compensation mode

EMOTIONS & DANCES (Recorded Moves)
  emotions             List available emotion moves
  dances               List available dance moves
  play-emotion NAME    Play a named emotion (e.g., cheerful1, curious1)
  play-dance NAME      Play a named dance (e.g., groovy_sway_and_roll)

VOLUME
  volume               Get current speaker volume
  volume-set LEVEL     Set speaker volume (0-100)
  volume-test          Play test sound
  mic-volume           Get current microphone volume
  mic-volume-set LVL   Set microphone volume (0-100)

AUDIO SENSING
  doa                  Get Direction of Arrival (microphone array)

APPS
  apps                 List all available apps
  apps-installed       List installed apps only
  app-status           Get status of currently running app
  app-start NAME       Start an app by name
  app-stop             Stop the currently running app
  app-restart          Restart the currently running app
  app-install JSON     Install an app (pass JSON body)
  app-remove NAME      Remove an installed app

CAMERA
  snap [OUTPUT]        Capture a JPEG snapshot from the camera (via WebRTC)
                       Default output: /tmp/reachy_snap.jpg
                       Requires SSH access (REACHY_SSH_PASS or ssh key)

SYSTEM
  wifi-status          Get WiFi connection status
  update-check         Check if firmware update is available
  version              Show firmware version
  reboot-daemon        Restart the robot daemon

ADVANCED
  raw METHOD PATH [BODY]   Raw API call (GET/POST, path, optional JSON body)
EOF
  exit 0
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die()  { echo "ERROR: $*" >&2; exit 1; }

api_get() {
  local path="$1"; shift
  local query="${1:-}"
  local url="${BASE}${path}"
  [[ -n "$query" ]] && url="${url}?${query}"
  curl -sf --max-time 10 "$url" 2>/dev/null || die "Request failed: GET $path"
}

api_post() {
  local path="$1"; shift
  local body="${1:-}"
  local query="${2:-}"
  local url="${BASE}${path}"
  [[ -n "$query" ]] && url="${url}?${query}"
  if [[ -n "$body" ]]; then
    curl -sf --max-time 15 -X POST -H "Content-Type: application/json" -d "$body" "$url" 2>/dev/null \
      || die "Request failed: POST $path"
  else
    curl -sf --max-time 15 -X POST "$url" 2>/dev/null \
      || die "Request failed: POST $path"
  fi
}

# Pretty-print JSON if jq is available
pp() {
  if command -v jq &>/dev/null; then
    jq .
  else
    cat
  fi
}

# SSH into the robot
REACHY_SSH_USER="${REACHY_SSH_USER:-pollen}"
REACHY_SSH_PASS="${REACHY_SSH_PASS:-root}"

ssh_cmd() {
  if command -v sshpass &>/dev/null && [[ -n "$REACHY_SSH_PASS" ]]; then
    sshpass -p "$REACHY_SSH_PASS" ssh -F /dev/null -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${REACHY_SSH_USER}@${REACHY_HOST}" "$@"
  else
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${REACHY_SSH_USER}@${REACHY_HOST}" "$@"
  fi
}

scp_from() {
  local remote="$1" local="$2"
  if command -v sshpass &>/dev/null && [[ -n "$REACHY_SSH_PASS" ]]; then
    sshpass -p "$REACHY_SSH_PASS" scp -F /dev/null -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${REACHY_SSH_USER}@${REACHY_HOST}:${remote}" "${local}"
  else
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${REACHY_SSH_USER}@${REACHY_HOST}:${remote}" "${local}"
  fi
}

scp_to() {
  local localfile="$1" remote="$2"
  if command -v sshpass &>/dev/null && [[ -n "$REACHY_SSH_PASS" ]]; then
    sshpass -p "$REACHY_SSH_PASS" scp -F /dev/null -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${localfile}" "${REACHY_SSH_USER}@${REACHY_HOST}:${remote}"
  else
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 \
      "${localfile}" "${REACHY_SSH_USER}@${REACHY_HOST}:${remote}"
  fi
}

# ---------------------------------------------------------------------------
# Parse global flags
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) REACHY_HOST="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) break ;;
  esac
done

BASE="http://${REACHY_HOST}:${REACHY_PORT}"
CMD="${1:-help}"
shift || true

# ---------------------------------------------------------------------------
# Command dispatch
# ---------------------------------------------------------------------------
case "$CMD" in

  # --- STATUS & INFO ---
  status)
    api_get "/api/daemon/status" | pp
    ;;
  state)
    api_get "/api/state/full" | pp
    ;;
  motors)
    api_get "/api/motors/status" | pp
    ;;
  health)
    api_post "/health-check" | pp
    ;;
  version)
    api_get "/api/daemon/status" | jq -r '.version // "unknown"'
    ;;

  # --- MOVEMENT ---
  wake-up|wakeup)
    api_post "/api/move/play/wake_up" | pp
    ;;
  sleep|goto-sleep)
    api_post "/api/move/play/goto_sleep" | pp
    ;;
  goto)
    # Parse goto sub-options
    head="" body="" ant="" dur="1.5" interp="minjerk"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --head)     head="$2"; shift 2 ;;
        --body)     body="$2"; shift 2 ;;
        --antennas) ant="$2"; shift 2 ;;
        --duration) dur="$2"; shift 2 ;;
        --interp)   interp="$2"; shift 2 ;;
        *) die "Unknown goto option: $1" ;;
      esac
    done
    # Build JSON
    json="{\"duration\":${dur},\"interpolation\":\"${interp}\""
    if [[ -n "$head" ]]; then
      IFS=',' read -r p y r <<< "$head"
      json+=",\"head_pose\":{\"x\":0,\"y\":0,\"z\":0,\"pitch\":${p},\"yaw\":${y},\"roll\":${r}}"
    fi
    if [[ -n "$body" ]]; then
      json+=",\"body_yaw\":${body}"
    fi
    if [[ -n "$ant" ]]; then
      IFS=',' read -r l ri <<< "$ant"
      json+=",\"antennas\":[${l},${ri}]"
    fi
    json+="}"
    api_post "/api/move/goto" "$json" | pp
    ;;
  set-target)
    head="" body="" ant=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --head)     head="$2"; shift 2 ;;
        --body)     body="$2"; shift 2 ;;
        --antennas) ant="$2"; shift 2 ;;
        *) die "Unknown set-target option: $1" ;;
      esac
    done
    json="{"
    first=true
    if [[ -n "$head" ]]; then
      IFS=',' read -r p y r <<< "$head"
      json+="\"target_head_pose\":{\"x\":0,\"y\":0,\"z\":0,\"pitch\":${p},\"yaw\":${y},\"roll\":${r}}"
      first=false
    fi
    if [[ -n "$body" ]]; then
      $first || json+=","
      json+="\"target_body_yaw\":${body}"
      first=false
    fi
    if [[ -n "$ant" ]]; then
      $first || json+=","
      IFS=',' read -r l ri <<< "$ant"
      json+="\"target_antennas\":[${l},${ri}]"
    fi
    json+="}"
    api_post "/api/move/set_target" "$json" | pp
    ;;
  stop-move)
    [[ $# -ge 1 ]] || die "Usage: stop-move UUID"
    api_post "/api/move/stop" "{\"uuid\":\"$1\"}" | pp
    ;;
  running)
    api_get "/api/move/running" | pp
    ;;

  # --- HEAD / BODY / ANTENNAS ---
  head-pose|head)
    api_get "/api/state/present_head_pose" | pp
    ;;
  body-yaw|body)
    api_get "/api/state/present_body_yaw"
    echo  # newline after bare number
    ;;
  antennas)
    api_get "/api/state/present_antenna_joint_positions" | pp
    ;;

  # --- MOTOR MODES ---
  motors-enable)
    api_post "/api/motors/set_mode/enabled" | pp
    ;;
  motors-disable)
    api_post "/api/motors/set_mode/disabled" | pp
    ;;
  motors-gravity)
    api_post "/api/motors/set_mode/gravity_compensation" | pp
    ;;

  # --- EMOTIONS & DANCES ---
  emotions)
    api_get "/api/move/recorded-move-datasets/list/pollen-robotics/reachy-mini-emotions-library" | pp
    ;;
  dances)
    api_get "/api/move/recorded-move-datasets/list/pollen-robotics/reachy-mini-dances-library" | pp
    ;;
  play-emotion)
    [[ $# -ge 1 ]] || die "Usage: play-emotion NAME"
    api_post "/api/move/play/recorded-move-dataset/pollen-robotics/reachy-mini-emotions-library/$1" | pp
    ;;
  play-dance)
    [[ $# -ge 1 ]] || die "Usage: play-dance NAME"
    api_post "/api/move/play/recorded-move-dataset/pollen-robotics/reachy-mini-dances-library/$1" | pp
    ;;

  # --- VOLUME ---
  volume)
    api_get "/api/volume/current" | pp
    ;;
  volume-set)
    [[ $# -ge 1 ]] || die "Usage: volume-set LEVEL (0-100)"
    api_post "/api/volume/set" "{\"volume\":$1}" | pp
    ;;
  volume-test)
    api_post "/api/volume/test-sound" | pp
    ;;
  mic-volume)
    api_get "/api/volume/microphone/current" | pp
    ;;
  mic-volume-set)
    [[ $# -ge 1 ]] || die "Usage: mic-volume-set LEVEL (0-100)"
    api_post "/api/volume/microphone/set" "{\"volume\":$1}" | pp
    ;;

  # --- AUDIO SENSING ---
  doa)
    api_get "/api/state/doa" | pp
    ;;

  # --- APPS ---
  apps)
    api_get "/api/apps/list-available" | jq '[.[] | {name, source_kind, description}]'
    ;;
  apps-installed)
    api_get "/api/apps/list-available/installed" | jq '[.[] | {name, description}]'
    ;;
  app-status)
    api_get "/api/apps/current-app-status" | pp
    ;;
  app-start)
    [[ $# -ge 1 ]] || die "Usage: app-start NAME"
    api_post "/api/apps/start-app/$1" | pp
    ;;
  app-stop)
    api_post "/api/apps/stop-current-app" | pp
    ;;
  app-restart)
    api_post "/api/apps/restart-current-app" | pp
    ;;
  app-install)
    [[ $# -ge 1 ]] || die "Usage: app-install JSON"
    api_post "/api/apps/install" "$1" | pp
    ;;
  app-remove)
    [[ $# -ge 1 ]] || die "Usage: app-remove NAME"
    api_post "/api/apps/remove/$1" | pp
    ;;

  # --- CAMERA ---
  snap|snapshot|photo|camera)
    OUTPUT="${1:-/tmp/reachy_snap.jpg}"
    REMOTE_SNAP="/tmp/reachy_snap_$$.jpg"
    REMOTE_SCRIPT="/tmp/reachy_gst_snap.py"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Deploy snapshot script if not present or outdated
    ssh_cmd "test -f ${REMOTE_SCRIPT}" 2>/dev/null || {
      echo "Deploying snapshot script..." >&2
      scp_to "${SCRIPT_DIR}/reachy-gst-snap.py" "${REMOTE_SCRIPT}" 2>/dev/null \
        || die "Failed to deploy snapshot script via SCP"
    }

    # Run capture on the robot
    ssh_cmd "
      export GST_PLUGIN_PATH=/opt/gst-plugins-rs/lib/aarch64-linux-gnu/gstreamer-1.0

      # Get producer ID from WebRTC signalling server
      PRODUCER=\$(/venvs/apps_venv/bin/python3 -c \"
import asyncio, json, websockets
async def p():
    async with websockets.connect('ws://127.0.0.1:8443') as ws:
        await ws.recv()
        await ws.send(json.dumps({'type': 'setPeerStatus', 'roles': ['listener'], 'meta': {}}))
        await ws.recv()
        await ws.send(json.dumps({'type': 'list'}))
        listing = json.loads(await ws.recv())
        if listing.get('producers'): print(listing['producers'][0]['id'])
asyncio.run(p())
\" 2>/dev/null)

      if [ -z \"\$PRODUCER\" ]; then
        echo 'ERROR: No WebRTC producer found. Is the daemon running?' >&2
        exit 1
      fi

      rm -f ${REMOTE_SNAP}
      timeout 20 /venvs/apps_venv/bin/python3 ${REMOTE_SCRIPT} ${REMOTE_SNAP} \"\$PRODUCER\" 2>&1 \
        | grep -v 'BUS ERROR\|Signalling error\|receiver is gone'
    " || die "Capture failed on robot"

    # Pull the image back
    scp_from "${REMOTE_SNAP}" "${OUTPUT}" 2>/dev/null \
      || die "Failed to copy snapshot from robot"

    # Cleanup remote temp file
    ssh_cmd "rm -f ${REMOTE_SNAP}" 2>/dev/null

    SIZE=$(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT" 2>/dev/null)
    echo "Snapshot saved: ${OUTPUT} (${SIZE} bytes)"
    ;;

  # --- SYSTEM ---
  wifi-status|wifi)
    api_get "/wifi/status" | pp
    ;;
  update-check)
    api_get "/update/available" | pp
    ;;
  reboot-daemon|restart)
    api_post "/api/daemon/restart" | pp
    ;;

  # --- RAW ---
  raw)
    [[ $# -ge 2 ]] || die "Usage: raw METHOD PATH [BODY]"
    method="$1"; path="$2"; body="${3:-}"
    case "${method^^}" in
      GET)  api_get "$path" ;;
      POST) api_post "$path" "$body" ;;
      *)    die "Unsupported method: $method (use GET or POST)" ;;
    esac | pp
    ;;

  help|-h|--help) usage ;;
  *) die "Unknown command: $CMD (run with --help for usage)" ;;
esac
