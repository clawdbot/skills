# ai-docker-compose

Scans your project and generates a docker-compose.yml that actually makes sense.

## Install

```bash
npm install -g ai-docker-compose
```

## Usage

```bash
npx ai-docker-compose                          # scan and generate
npx ai-docker-compose --preview                # print to stdout
npx ai-docker-compose -a "redis,postgres"      # add extra services
```

## Options

- `-d, --dir <path>` - Project directory (default: current)
- `-o, --output <file>` - Output file (default: docker-compose.yml)
- `--preview` - Print to stdout
- `-a, --add <services>` - Extra services to include

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## License

MIT
