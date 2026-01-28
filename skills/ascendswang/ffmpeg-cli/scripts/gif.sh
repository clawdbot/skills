#!/bin/bash
# Convert video to GIF
set -e

usage() {
    echo "Usage: $0 -i <video> -s <start> -e <end> -o <output.gif>"
    echo "  -i <video>    Input video file"
    echo "  -s <start>    Start time (HH:MM:SS or seconds)"
    echo "  -e <end>      End time (HH:MM:SS or seconds)"
    echo "  -o <output>   Output GIF file"
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

# Scale to reasonable size for GIF
ffmpeg -ss "$START" -to "$END" -i "$INPUT" -vf "fps=10,scale=480:-1:flags=lanczos" -c:v gif -y "$OUTPUT"
echo "✅ GIF created: $OUTPUT"
