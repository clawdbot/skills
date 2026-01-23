# MinerU CLI Configuration

This skill assumes the MinerU wrapper described by Martin:

```bash
mineru -p <path_to_pdf> -o <output_dir> -b pipeline -l en -d cpu [-m auto]
```

## Defaults (wrapper-based)
- Input flag: `-p`
- Output flag: `-o`
- Backend flag: `-b`
- Language flag: `-l`
- Device flag: `-d` (cpu)
- Method flag: `-m` (auto)
- Threads: `OMP_NUM_THREADS=4` (set by wrapper or this script)

## Output
MinerU will create a per-document directory under the output root. Typical outputs:
- `<doc>.md`
- `<doc>_middle.json`
- `<doc>/` (images/tables)

## Format mapping
The wrapper supports `--format md|json|both` and maps to MinerU values:
- `md` → `markdown`
- `json` → `json`
- `both` → `markdown,json`

If your wrapper uses different values, override:

```bash
export MINERU_FORMAT_FLAG=--format
export MINERU_FORMAT_VALUE_MD=markdown
export MINERU_FORMAT_VALUE_JSON=json
export MINERU_FORMAT_VALUE_BOTH=markdown,json
```

## Advanced defaults
Defaults used by the wrapper:
- `backend=pipeline`
- `method=auto`
- `device=cpu`
- `threads=OMP_NUM_THREADS` (default 4)

Override flags/values via env vars as needed:

```bash
export MINERU_CMD=~/.local/bin/mineru
export MINERU_INPUT_FLAG=-p
export MINERU_OUTPUT_FLAG=-o
export MINERU_BACKEND_FLAG=-b
export MINERU_LANG_FLAG=-l
export MINERU_DEVICE_FLAG=-d
export MINERU_METHOD_FLAG=-m
export MINERU_THREADS_FLAG=OMP_NUM_THREADS
```

## Test
```bash
./scripts/mineru_parse.sh /path/to/file.pdf --format both --threads 4 --lang en --backend pipeline --method auto --device cpu
```
