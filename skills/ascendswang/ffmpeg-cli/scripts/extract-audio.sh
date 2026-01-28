#!/bin/bash
# Extract audio from video
set -e

usage() {
    echo "Usage: $0 -i <video> -o <output.mp3>"
    echo "  -i <video>    Input video file"
    echo "  -o <output>   Output audio file (mp3/aac)"
    exit 1
}

while getopts "i:o:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$OUTPUT" ] && usage

ffmpeg -i "$INPUT" -vn -acodec libmp3lame -q:a 2 -y "$OUTPUT"
echo "✅ Audio extracted: $OUTPUT"
