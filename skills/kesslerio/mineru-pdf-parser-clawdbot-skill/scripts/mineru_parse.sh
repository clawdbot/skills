#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: mineru_parse.sh <input.pdf> [options]

Options:
  --outroot DIR        Root output directory (default: ./mineru-output)
  --format FMT         md | json | both (default: both)
  --tables             Extract tables (if supported)
  --images             Extract images (if supported)
  --threads N          Thread count (default: 4)
  --lang LANG          Language (default: en)
  --backend NAME       Backend (default: pipeline)
  --method NAME        Method (default: auto)
  --device NAME        Device (default: cpu)
  -h, --help           Show help

Environment overrides:
  MINERU_CMD                  MinerU CLI command (default: mineru)
  MINERU_INPUT_FLAG           Input flag (default: -p)
  MINERU_OUTPUT_FLAG          Output flag (default: -o)
  MINERU_FORMAT_FLAG          Format flag (default: --format)
  MINERU_FORMAT_VALUE_MD      Value for md (default: markdown)
  MINERU_FORMAT_VALUE_JSON    Value for json (default: json)
  MINERU_FORMAT_VALUE_BOTH    Value for both (default: markdown,json)
  MINERU_TABLES_FLAG          Tables flag (default: --tables)
  MINERU_IMAGES_FLAG          Images flag (default: --images)
  MINERU_THREADS_FLAG         Threads env var name (default: OMP_NUM_THREADS)
  MINERU_LANG_FLAG            Language flag (default: -l)
  MINERU_BACKEND_FLAG         Backend flag (default: -b)
  MINERU_METHOD_FLAG          Method flag (default: -m)
  MINERU_DEVICE_FLAG          Device flag (default: -d)
  MINERU_EXTRA_ARGS           Extra raw args appended as-is

EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

input=""
outroot="./mineru-output"
format="both"
tables=false
images=false
threads="4"
lang="en"
backend="pipeline"
method="auto"
device="cpu"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage; exit 0;;
    --outroot)
      outroot="$2"; shift 2;;
    --format)
      format="$2"; shift 2;;
    --tables)
      tables=true; shift;;
    --images)
      images=true; shift;;
    --threads)
      threads="$2"; shift 2;;
    --lang)
      lang="$2"; shift 2;;
    --backend)
      backend="$2"; shift 2;;
    --method)
      method="$2"; shift 2;;
    --device)
      device="$2"; shift 2;;
    *)
      if [[ -z "$input" ]]; then
        input="$1"; shift
      else
        echo "Unknown argument: $1" >&2
        usage
        exit 1
      fi
      ;;
  esac
 done

if [[ -z "$input" ]]; then
  echo "Missing input PDF" >&2
  usage
  exit 1
fi

if [[ ! -f "$input" ]]; then
  echo "Input not found: $input" >&2
  exit 1
fi

cmd="${MINERU_CMD:-mineru}"
if ! command -v "$cmd" >/dev/null 2>&1; then
  echo "MinerU CLI not found: $cmd" >&2
  echo "Set MINERU_CMD or install MinerU CLI." >&2
  exit 1
fi

outdir="$outroot"
mkdir -p "$outdir"

input_flag="${MINERU_INPUT_FLAG:--p}"
output_flag="${MINERU_OUTPUT_FLAG:--o}"
format_flag="${MINERU_FORMAT_FLAG:---format}"
fmt_md="${MINERU_FORMAT_VALUE_MD:-markdown}"
fmt_json="${MINERU_FORMAT_VALUE_JSON:-json}"
fmt_both="${MINERU_FORMAT_VALUE_BOTH:-markdown,json}"

tables_flag="${MINERU_TABLES_FLAG:---tables}"
images_flag="${MINERU_IMAGES_FLAG:---images}"
threads_env="${MINERU_THREADS_FLAG:-OMP_NUM_THREADS}"
lang_flag="${MINERU_LANG_FLAG:--l}"
backend_flag="${MINERU_BACKEND_FLAG:--b}"
method_flag="${MINERU_METHOD_FLAG:--m}"
device_flag="${MINERU_DEVICE_FLAG:--d}"

case "$format" in
  md) fmt_val="$fmt_md";;
  json) fmt_val="$fmt_json";;
  both) fmt_val="$fmt_both";;
  *)
    echo "Invalid format: $format (use md|json|both)" >&2
    exit 1;;
 esac

args=("$input_flag" "$input" "$output_flag" "$outdir" "$backend_flag" "$backend" \
      "$lang_flag" "$lang" "$device_flag" "$device" "$method_flag" "$method")

if $tables; then
  args+=("$tables_flag")
fi
if $images; then
  args+=("$images_flag")
fi

# Include format if flag is supported by wrapper/CLI
if [[ -n "$format_flag" ]]; then
  args+=("$format_flag" "$fmt_val")
fi

if [[ -n "${MINERU_EXTRA_ARGS:-}" ]]; then
  # shellcheck disable=SC2206
  extra=( ${MINERU_EXTRA_ARGS} )
  args+=("${extra[@]}")
fi

echo "Running: $threads_env=$threads $cmd ${args[*]}"
env "$threads_env=$threads" "$cmd" "${args[@]}"

echo "Done. Output root: $outdir"
