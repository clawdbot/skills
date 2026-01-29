#!/usr/bin/env bash
# reachy-react.sh — Contextual robot reactions for Clawdbot integration
# Usage: reachy-react.sh <reaction> [--bg]
# Reactions run in foreground by default. Pass --bg to background them.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REACHY="${SCRIPT_DIR}/reachy.sh"
REACHY_HOST="${REACHY_HOST:-192.168.8.17}"

# Quiet hours: robot sleeps, no reactions (22:00 - 06:29 ET)
QUIET_START=22
QUIET_END=7

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
die()  { echo "ERROR: $*" >&2; exit 1; }

current_hour() {
  TZ="America/New_York" date +%H | sed 's/^0//'
}

is_quiet_hours() {
  local h
  h=$(current_hour)
  [[ $h -ge $QUIET_START || $h -lt $QUIET_END ]]
}

# Quick connectivity check (200ms timeout)
is_reachable() {
  curl -sf --max-time 1 "http://${REACHY_HOST}:8000/" >/dev/null 2>&1
}

# Get robot state (not_initialized, starting, running, etc.)
robot_state() {
  curl -sf --max-time 3 "http://${REACHY_HOST}:8000/api/daemon/status" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('state','unknown'))" 2>/dev/null \
    || echo "unreachable"
}

# Ensure robot is awake. Returns 0 if awake, 1 if can't wake.
ensure_awake() {
  local state
  state=$(robot_state)
  case "$state" in
    running) return 0 ;;
    not_initialized)
      # Start daemon + wake up
      curl -sf --max-time 5 -X POST "http://${REACHY_HOST}:8000/api/daemon/start?wake_up=true" >/dev/null 2>&1
      sleep 5
      "$REACHY" wake-up >/dev/null 2>&1 || true
      sleep 3
      return 0
      ;;
    starting)
      sleep 5
      "$REACHY" wake-up >/dev/null 2>&1 || true
      sleep 3
      return 0
      ;;
    unreachable) return 1 ;;
    *) return 0 ;;  # try anyway
  esac
}

# Fire-and-forget emotion (ignore errors)
play() {
  "$REACHY" play-emotion "$1" >/dev/null 2>&1 || true
}

# Fire-and-forget move
move() {
  "$REACHY" goto "$@" >/dev/null 2>&1 || true
}

# Pick a random item from arguments
pick_random() {
  local arr=("$@")
  echo "${arr[$((RANDOM % ${#arr[@]}))]}"
}

usage() {
  cat <<'EOF'
Usage: reachy-react.sh <reaction> [--bg]

REACTIONS
  ack           Nod acknowledgment (received a request)
  success       Cheerful completion (task done)
  alert         Surprised/important (urgent email, alert)
  remind        Welcoming/helpful (meeting reminder, to-do)
  idle          Subtle heartbeat animation (head tilt or antenna wave)
  morning       Wake up + greeting (morning briefing)
  goodnight     Put robot to sleep (night mode)
  patrol        Camera snapshot + return image path
  doa-track     Check DOA and turn head toward sound source
  celebrate     Random dance (fun moments)

OPTIONS
  --bg          Run in background (non-blocking)

ENVIRONMENT
  REACHY_HOST   Robot IP (default: 192.168.8.17)
EOF
  exit 0
}

# ---------------------------------------------------------------------------
# Reactions
# ---------------------------------------------------------------------------
do_ack() {
  # Quick nod: head down then back up
  move --head 0.25,0,0 --duration 0.4
  sleep 0.5
  move --head 0,0,0 --duration 0.4
}

do_success() {
  local emotion
  emotion=$(pick_random cheerful1 cheerful2 cheerful3 happy1 happy2 yes1)
  play "$emotion"
}

do_alert() {
  # Antennas up + surprised look
  move --antennas 0.4,0.4 --duration 0.3
  sleep 0.3
  local emotion
  emotion=$(pick_random surprised1 surprised2 surprised3)
  play "$emotion"
}

do_remind() {
  local emotion
  emotion=$(pick_random welcoming1 welcoming2 curious1 curious2 attentive1)
  play "$emotion"
}

do_idle() {
  # Subtle random animation: head tilt, antenna wave, or small look-around
  local choice
  choice=$((RANDOM % 4))
  case $choice in
    0)
      # Gentle head tilt right then back
      move --head 0,0,-0.15 --duration 1.0
      sleep 1.5
      move --head 0,0,0 --duration 1.0
      ;;
    1)
      # Gentle head tilt left then back
      move --head 0,0,0.15 --duration 1.0
      sleep 1.5
      move --head 0,0,0 --duration 1.0
      ;;
    2)
      # Antenna wave: alternating up/down
      move --antennas 0.3,-0.2 --duration 0.6
      sleep 0.8
      move --antennas -0.2,0.3 --duration 0.6
      sleep 0.8
      move --antennas 0,0 --duration 0.6
      ;;
    3)
      # Small look around (glance left then right then center)
      move --head 0,0.2,0 --duration 0.8
      sleep 1.0
      move --head 0,-0.2,0 --duration 0.8
      sleep 1.0
      move --head 0,0,0 --duration 0.8
      ;;
  esac
}

do_morning() {
  # Wake up the robot and greet
  "$REACHY" wake-up >/dev/null 2>&1 || true
  sleep 3
  local emotion
  emotion=$(pick_random welcoming1 welcoming2 welcoming3 cheerful1)
  play "$emotion"
}

do_goodnight() {
  # Play a sleepy emotion then sleep
  play sleepy1 2>/dev/null || true
  sleep 2
  "$REACHY" sleep >/dev/null 2>&1 || true
}

do_patrol() {
  # Camera snapshot — prints the output path
  local output="${1:-/tmp/reachy_patrol.jpg}"
  "$REACHY" snap "$output" 2>/dev/null
  echo "$output"
}

do_doa_track() {
  # Get Direction of Arrival and turn head toward sound
  local doa_json
  doa_json=$("$REACHY" doa 2>/dev/null) || return 1

  local angle speech
  angle=$(echo "$doa_json" | python3 -c "
import sys, json, math
d = json.load(sys.stdin)
# DOA angle: 0=left, pi/2=front, pi=right
# Convert to head yaw: positive=look left, negative=look right
# Map: 0 -> +0.6, pi/2 -> 0, pi -> -0.6
angle = d.get('angle', 1.5708)  # default to front
yaw = (1.5708 - angle) / 1.5708 * 0.6
print(f'{yaw:.3f}')
" 2>/dev/null) || return 1

  speech=$(echo "$doa_json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('true' if d.get('is_speech', False) else 'false')
" 2>/dev/null) || return 1

  if [[ "$speech" == "true" ]]; then
    # Turn toward the speaker
    move --head 0,"${angle}",0 --duration 0.8
    echo "Speech detected at yaw=${angle}, turning head"
  else
    echo "No speech detected"
  fi
}

do_celebrate() {
  local dance
  dance=$(pick_random groovy_sway_and_roll chicken_peck dizzy_spin head_bop wiggle_and_groove funky_shimmy robot_wave sassy_strut)
  "$REACHY" play-dance "$dance" >/dev/null 2>&1 || true
  echo "Dancing: $dance"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
[[ $# -ge 1 ]] || usage

REACTION="$1"; shift
BG=false
for arg in "$@"; do
  [[ "$arg" == "--bg" ]] && BG=true
done

# Skip if unreachable (except for status-only commands)
if ! is_reachable; then
  echo "Robot unreachable at ${REACHY_HOST}" >&2
  exit 1
fi

# Quiet hours guard (except morning/goodnight/patrol which are intentional)
if is_quiet_hours && [[ "$REACTION" != "morning" && "$REACTION" != "goodnight" && "$REACTION" != "patrol" ]]; then
  echo "Quiet hours — skipping reaction: $REACTION"
  exit 0
fi

# Ensure awake for active reactions (not goodnight)
if [[ "$REACTION" != "goodnight" && "$REACTION" != "patrol" ]]; then
  ensure_awake || { echo "Cannot wake robot" >&2; exit 1; }
fi

# Dispatch
run_reaction() {
  case "$REACTION" in
    ack)        do_ack ;;
    success)    do_success ;;
    alert)      do_alert ;;
    remind)     do_remind ;;
    idle)       do_idle ;;
    morning)    do_morning ;;
    goodnight)  do_goodnight ;;
    patrol)     do_patrol "$@" ;;
    doa-track|doa)  do_doa_track ;;
    celebrate|dance) do_celebrate ;;
    *)          die "Unknown reaction: $REACTION" ;;
  esac
}

if $BG; then
  run_reaction "$@" &
  disown
  echo "Reaction '$REACTION' running in background"
else
  run_reaction "$@"
fi
