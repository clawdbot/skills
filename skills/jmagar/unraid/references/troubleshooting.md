# Unraid API Troubleshooting Guide

Common issues and solutions when working with the Unraid GraphQL API.

## "Cannot query field" error
Field name doesn't exist in your Unraid version. Use introspection to find valid fields:
```bash
./scripts/unraid-query.sh -q "{ __type(name: \"TypeName\") { fields { name } } }"
```

## "API key validation failed"
- Check API key is correct and not truncated
- Verify key has appropriate permissions (use "Viewer" role)
- Ensure URL includes `/graphql` endpoint (e.g. `http://host/graphql`)

## Empty results
Many queries return empty arrays when no data exists:
- `docker.containers` - No containers running
- `vms` - No VMs configured (or VM service disabled)
- `notifications` - No active alerts
- `plugins` - No plugins installed

This is normal behavior, not an error. Ensure your scripts handle empty arrays gracefully.

## "VMs are not available" (GraphQL Error)
If the VM manager is disabled in Unraid settings, querying `{ vms { ... } }` will return a GraphQL error.
**Solution:** Check if VM service is enabled before querying, or use error handling (like `IGNORE_ERRORS=true` in dashboard scripts) to process partial data.

## URL connection issues
- Use HTTPS (not HTTP) for remote access if configured
- For local access: `http://unraid-server-ip/graphql`
- For Unraid Connect: Use provided URL with token in hostname
- Use `-k` (insecure) with curl if using self-signed certs on local HTTPS
- Use `-L` (follow redirects) if Unraid redirects HTTP to HTTPS
