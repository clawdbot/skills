#!/bin/bash
# Generate thumbnail from video
set -e

usage() {
    echo "Usage: $0 -i <video> [-t <timestamp>] -o <output.jpg>"
    echo "  -i <video>     Input video file"
    echo "  -t <timestamp> Timestamp for frame (default: 00:00:01)"
    echo "  -o <output>    Output image file"
    exit 1
}

TIMESTAMP="00:00:01"

while getopts "i:t:o:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        t) TIMESTAMP="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$OUTPUT" ] && usage

ffmpeg -ss "$TIMESTAMP" -i "$INPUT" -vframes 1 -q:v 2 -y "$OUTPUT"
echo "✅ Thumbnail saved: $OUTPUT"
