#!/bin/bash
# Convert video to different format
set -e

usage() {
    echo "Usage: $0 -i <input> -o <output>"
    echo "  -i <input>    Input file"
    echo "  -o <output>   Output file (extension determines format)"
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

ffmpeg -i "$INPUT" -c:v libx264 -crf 23 -c:a aac -b:a 128k -y "$OUTPUT"
echo "✅ Converted: $OUTPUT"
