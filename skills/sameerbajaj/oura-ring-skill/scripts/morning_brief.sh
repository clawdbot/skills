#!/bin/bash
# Oura Morning Readiness Brief - Maximum Insights

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$DIR")"
VENV_PATH="$SKILL_DIR/.venv"
ENV_FILE="$SKILL_DIR/.env"

if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

PYTHON_CLI="$SKILL_DIR/cli.py"

# Fetch data in JSON
SLEEP_JSON=$(python3 "$PYTHON_CLI" --env-file "$ENV_FILE" --format json sleep)
READINESS_JSON=$(python3 "$PYTHON_CLI" --env-file "$ENV_FILE" --format json readiness)
TRENDS_JSON=$(python3 "$PYTHON_CLI" --env-file "$ENV_FILE" --format json trends)

python3 - <<EOF
import json
from datetime import datetime

def fmt_dur(sec):
    h = sec // 3600
    m = (sec % 3600) // 60
    return f"{h}h {m}m"

sleep_data = json.loads('''$SLEEP_JSON''')
readiness_data = json.loads('''$READINESS_JSON''')
trends_data = json.loads('''$TRENDS_JSON''')

s_item = sleep_data.get('item', {})
s_detail = sleep_data.get('detail', {})
r_item = readiness_data.get('item', {})
trend_items = trends_data.get('items', [])
trend_sessions = trends_data.get('sessions', [])

print(f"OURA INSIGHT BRIEF — {datetime.now().strftime('%a %b %d, %Y')}\n")

# 1. LAST NIGHT ANALYSIS
print("*LAST NIGHT DATA* 💤")
dur = s_detail.get('total_sleep_duration', 0)
deep = s_detail.get('deep_sleep_duration', 0)
rem = s_detail.get('rem_sleep_duration', 0)
awake = s_detail.get('awake_time', 0)

print(f"Total Sleep: *{fmt_dur(dur)}* (Score: *{s_item.get('score', 0)}*)")
print(f"- Deep Sleep: *{fmt_dur(deep)}*")
print(f"- REM Sleep: *{fmt_dur(rem)}*")
print(f"- Time Awake: *{fmt_dur(awake)}*")
print(f"Efficiency: *{s_detail.get('efficiency', 0)}%*")
print(f"Lowest RHR: *{s_detail.get('lowest_heart_rate', 0)} bpm*")
print(f"Avg HRV: *{s_detail.get('average_hrv', 0)} ms*\n")

# 2. TODAY'S STRATEGY
print("*TODAY'S STRATEGY* 🔋")
score = r_item.get('score', 0)
if score >= 85:
    msg = "🚀 *Peak performance.* You're in an optimal state for deep work and high-intensity output."
elif score >= 70:
    msg = "⚖️ *Steady state.* Good capacity for work, but keep a balanced pace."
else:
    msg = "🛌 *Recovery mode.* Focus on low-energy tasks and active recovery."

print(f"Readiness: *{score}*")
print(f"Insight: {msg}\n")

# 3. DETAILED TRENDS (24h Delta)
print("*24-HOUR TRENDS* 📈")
if len(trend_sessions) >= 2:
    cur = trend_sessions[-1]
    prev = trend_sessions[-2]
    
    # RHR
    r_diff = cur.get('lowest_heart_rate', 0) - prev.get('lowest_heart_rate', 0)
    r_msg = f"*{abs(r_diff)} bpm higher*" if r_diff > 0 else f"*{abs(r_diff)} bpm lower*"
    r_status = "⚠️" if r_diff > 1 else "✅"
    print(f"{r_status} RHR: {r_msg} than yesterday.")
    
    # HRV
    h_diff = cur.get('average_hrv', 0) - prev.get('average_hrv', 0)
    h_msg = f"*{abs(h_diff)} ms higher*" if h_diff > 0 else f"*{abs(h_diff)} ms lower*"
    h_status = "✅" if h_diff > 0 else "⚠️"
    print(f"{h_status} HRV: {h_msg} than yesterday.")
    
    # Sleep
    d_diff = cur.get('total_sleep_duration', 0) - prev.get('total_sleep_duration', 0)
    d_msg = f"*{fmt_dur(abs(d_diff))} more*" if d_diff > 0 else f"*{fmt_dur(abs(d_diff))} less*"
    print(f"📅 Sleep: {d_msg} than yesterday.")
    
    if r_diff > 1 and h_diff < 0:
        print("\n*Note*: The combo of higher RHR and lower HRV suggests your body is still processing stress or a late meal. Prioritize hydration and an early bedtime.")

EOF
