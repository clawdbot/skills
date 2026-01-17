---
name: comfy-cli
description: Install, manage, and run ComfyUI instances. Use when setting up ComfyUI, launching servers, installing/updating/debugging custom nodes, downloading models from CivitAI/HuggingFace, managing workspaces, running API workflows, or troubleshooting node conflicts with bisect.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["comfy"]},"install":[{"id":"uv","kind":"uv","package":"comfy-cli","bins":["comfy"],"label":"Install comfy-cli (uv)"}]}}
---

# comfy-cli

CLI tool for managing ComfyUI installations, custom nodes, and models.

## Quick start

```bash
comfy install                          # Install ComfyUI + ComfyUI-Manager
comfy launch                           # Start ComfyUI server
comfy node install ComfyUI-Impact-Pack # Install a custom node
comfy model download --url "https://civitai.com/api/download/models/12345"
```

## Installation

```bash
comfy install                          # Interactive GPU selection
comfy install --nvidia                 # NVIDIA GPU
comfy install --amd                    # AMD GPU (Linux ROCm)
comfy install --m-series               # Apple Silicon
comfy install --cpu                    # CPU only
comfy install --restore                # Restore deps for existing install
comfy install --pr 1234                # Install specific PR
comfy install --version latest         # Latest stable release
comfy install --version 0.2.0          # Specific version
```

GPU options: `--nvidia`, `--amd`, `--intel-arc`, `--m-series`, `--cpu`

CUDA versions (NVIDIA): `--cuda 12.9`, `--cuda 12.6`, `--cuda 12.4`, `--cuda 12.1`, `--cuda 11.8`

Other flags: `--skip-manager`, `--skip-torch-or-directml`, `--skip-requirement`, `--fast-deps`

## Launch

```bash
comfy launch                           # Foreground mode
comfy launch --background              # Background mode
comfy launch -- --listen 0.0.0.0       # Pass args to ComfyUI
comfy stop                             # Stop background instance
comfy launch --frontend-pr 1234        # Test frontend PR
```

## Workspace selection

Global flags (mutually exclusive):

```bash
comfy --workspace /path/to/ComfyUI ... # Explicit path
comfy --recent ...                     # Last used instance
comfy --here ...                       # Current directory
comfy which                            # Show selected instance
comfy set-default /path/to/ComfyUI     # Set default
```

## Custom nodes

```bash
comfy node show                        # List installed nodes
comfy node simple-show                 # Compact list
comfy node install <name>              # Install from registry
comfy node install <name> --fast-deps  # Fast dependency install
comfy node reinstall <name>            # Reinstall node
comfy node uninstall <name>            # Remove node
comfy node update all                  # Update all nodes
comfy node disable <name>              # Disable node
comfy node enable <name>               # Enable node
comfy node fix <name>                  # Fix node dependencies
```

Snapshots:
```bash
comfy node save-snapshot               # Save current state
comfy node save-snapshot --output snapshot.json
comfy node restore-snapshot snapshot.json
comfy node restore-dependencies        # Restore deps from nodes
```

Debugging:
```bash
comfy node bisect                      # Binary search for broken node
comfy node deps-in-workflow workflow.json  # Extract deps from workflow
comfy node install-deps --workflow workflow.json  # Install workflow deps
```

Publishing:
```bash
comfy node init                        # Init scaffolding
comfy node scaffold                    # Create project via cookiecutter
comfy node validate                    # Validate before publishing
comfy node pack                        # Package node
comfy node publish                     # Publish to registry
```

## Models

```bash
comfy model list                       # List available models
comfy model download --url <url>       # Download from URL
comfy model remove <name>              # Remove model
```

Sources: CivitAI, Hugging Face, direct URLs

Tokens for gated models:
- `--civitai-token` or config `civitai_api_token`
- `--hf-token` or config `hf_api_token`

## Run workflows

```bash
comfy run --workflow workflow_api.json
comfy run --workflow workflow.json --wait --verbose
comfy run --workflow workflow.json --host 192.168.1.10 --port 8188
```

Requires running ComfyUI instance.

## ComfyUI-Manager

```bash
comfy manager disable-gui              # Hide manager in UI
comfy manager enable-gui               # Show manager in UI
comfy manager clear                    # Clear startup actions
```

## Update

```bash
comfy update all                       # Update ComfyUI + nodes
comfy update comfy                     # Update ComfyUI only
```

## Other commands

```bash
comfy env                              # Show config and paths
comfy --version                        # Print CLI version
comfy pr-cache list                    # List cached PR builds
comfy pr-cache clean                   # Clear expired caches
comfy standalone                       # Create standalone Python bundle
comfy tracking enable|disable          # Manage analytics
comfy feedback                         # Submit feedback
```

## Config

Location:
- Linux: `~/.config/comfy-cli/config.ini`
- macOS: `~/Library/Application Support/comfy-cli/config.ini`
- Windows: `%APPDATA%\Local\comfy-cli\config.ini`

Keys: `default_workspace`, `default_launch_extras`, `civitai_api_token`, `hf_api_token`

## Tips

- `--skip-prompt` for non-interactive mode (CI/scripts)
- Background mode tracks PID for clean `comfy stop`
- Snapshots preserve exact node versions for reproducibility
- `comfy node bisect` binary-searches to find which node broke your setup
- PR cache avoids rebuilding frontend PRs you've tested before
