# Troubleshooting

## rr doctor fails to connect

- Ensure Beeper Desktop is running.
- Confirm the base URL (default is http://localhost:23373).
- If you changed the port, set `BEEPER_URL` or pass `--base-url`.

## Token errors

- If you see "no token configured", run `rr auth set <token>`.
- `BEEPER_TOKEN` overrides the config file.
- Use `rr auth status --check` to validate the token.

## Non-interactive failures

- Destructive commands require confirmation.
- In CI or scripts, pass `--force` explicitly.
- `--no-input`/`BEEPER_NO_INPUT` disables prompts and will fail without `--force`.
