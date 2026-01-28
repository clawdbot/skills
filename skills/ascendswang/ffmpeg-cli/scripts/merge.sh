#!/bin/bash
# Merge multiple video files
set -e

usage() {
    echo "Usage: $0 -o <output> <file1> <file2> ..."
    echo "  -o <output>   Output file"
    echo "  <files...>    Input video files"
    exit 1
}

OUTPUT=""

while getopts "o:h" opt; do
    case $opt in
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

shift $((OPTIND-1))

[ -z "$OUTPUT" ] && usage
[ $# -eq 0 ] && usage

# Create file list for ffmpeg concat
TEMP_LIST=$(mktemp /tmp/ffmpeg_merge_XXXXXX.txt)
for f in "$@"; do
    echo "file '$f'" >> "$TEMP_LIST"
done

ffmpeg -f concat -safe 0 -i "$TEMP_LIST" -c copy -y "$OUTPUT"
rm -f "$TEMP_LIST"

echo "✅ Merge complete: $OUTPUT"
