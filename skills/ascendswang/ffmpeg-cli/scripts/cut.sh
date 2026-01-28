#!/bin/bash
# Cut video segment without re-encoding (fast)
set -e

usage() {
    echo "Usage: $0 -i <input> -s <start> -e <end> -o <output>"
    echo "  -i <input>    Input video file"
    echo "  -s <start>    Start time (HH:MM:SS or seconds)"
    echo "  -e <end>      End time (HH:MM:SS or seconds)"
    echo "  -o <output>   Output file"
    exit 1
}

while getopts "i:s:e:o:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        s) START="$OPTARG" ;;
        e) END="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$START" ] || [ -z "$END" ] || [ -z "$OUTPUT" ] && usage

ffmpeg -i "$INPUT" -ss "$START" -to "$END" -c copy -y "$OUTPUT"
echo "✅ Cut complete: $OUTPUT"
