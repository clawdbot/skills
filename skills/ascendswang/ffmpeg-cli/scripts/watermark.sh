#!/bin/bash
# Add watermark to video
set -e

usage() {
    echo "Usage: $0 -i <video> -w <watermark> -o <output>"
    echo "  -i <video>      Input video file"
    echo "  -w <watermark>  Watermark image file"
    echo "  -o <output>     Output file"
    exit 1
}

POS="10:10"  # Default: top-left

while getopts "i:w:o:p:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        w) WATERMARK="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        p) POS="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] || [ -z "$WATERMARK" ] || [ -z "$OUTPUT" ] && usage

ffmpeg -i "$INPUT" -i "$WATERMARK" -filter_complex "[0:v][1:v] overlay=$POS" -c:a copy -y "$OUTPUT"
echo "✅ Watermark added: $OUTPUT"
