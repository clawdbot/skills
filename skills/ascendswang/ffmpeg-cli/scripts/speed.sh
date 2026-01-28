#!/bin/bash
# Change video playback speed
set -e

usage() {
    echo "Usage: $0 -i <input> -r <rate> -o <output>"
    echo "  -i <input>    Input video file"
    echo "  -r <rate>     Speed rate (0.5 = half speed, 2.0 = double speed)"
    echo "  -o <output>   Output file"
    exit 1
}

RATE=1.0

while getopts "i:r:o:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        r) RATE="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$RATE" ] || [ -z "$OUTPUT" ] && usage

# Use atempo for 0.5-2.0 range, chain for beyond
if (( $(echo "$RATE > 2.0" | bc -l) )); then
    FILTERS="atempo=2.0,atempo=$(echo "$RATE/2" | bc -l)"
elif (( $(echo "$RATE < 0.5" | bc -l) )); then
    FILTERS="atempo=0.5,atempo=$(echo "$RATE*2" | bc -l)"
else
    FILTERS="atempo=$RATE"
fi

ffmpeg -i "$INPUT" -filter:a "$FILTERS" -filter:v "setpts=${RATE}*PTS" -c:v libx264 -crf 23 -c:a aac -y "$OUTPUT"
echo "✅ Speed adjusted ($RATEx): $OUTPUT"
