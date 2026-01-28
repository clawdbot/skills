# Troubleshooting Guide

## Authentication Issues

### Session Expired

**Problem:** Commands fail with authentication errors.

**Solution:**
```bash
nlm login
```

NotebookLM sessions typically last ~20 minutes. Re-authenticate when commands start failing.

### Chrome Not Found

**Problem:** `nlm login` fails because Chrome is not installed or not found.

**Solution:**
- Ensure Google Chrome is installed
- Check that Chrome is in your PATH
- On Linux, you may need to specify the Chrome binary path

### Cookie Extraction Failed

**Problem:** Authentication fails during cookie extraction.

**Solution:**
- Ensure Chrome is closed before running `nlm login`
- Check that Chrome is not running in headless mode
- Try logging into NotebookLM manually in Chrome first

## Network Issues

### Connection Timeout

**Problem:** Commands timeout when connecting to NotebookLM.

**Solution:**
- Check internet connection
- Verify NotebookLM is accessible (notebooklm.google.com)
- Try again in a few moments
- Check if there are firewall restrictions

### Rate Limiting

**Problem:** "Too many requests" error.

**Solution:**
- NotebookLM free tier has ~50 queries/day limit
- Wait before making more requests
- Consider batching operations

## Source Issues

### Drive Source Not Syncing

**Problem:** Google Drive sources show outdated content.

**Solution:**
```bash
nlm source stale <notebook-id>
nlm source sync <notebook-id> --confirm
```

### URL Source Fails

**Problem:** Adding URL source fails.

**Solution:**
- Verify URL is accessible
- Some websites block automated access
- Try using `--text` option instead with copied content

### YouTube Source Issues

**Problem:** YouTube video fails to add as source.

**Solution:**
- Ensure video is public
- Check if video has restrictions
- Some videos may be unavailable due to region locks

## Content Generation Issues

### Generation Timeout

**Problem:** Content generation (audio, quiz, etc.) times out.

**Solution:**
- Large notebooks take longer to process
- Reduce number of sources
- Try again with fewer sources

### Generation Fails

**Problem:** Content generation fails with error.

**Solution:**
- Check that notebook has sources
- Verify sources have been processed
- Try creating the content again
- Check studio status for existing failed artifacts

### Artifact Not Found

**Problem:** Cannot find generated artifact.

**Solution:**
```bash
nlm studio status <notebook-id>
```
List all artifacts to find the correct ID.

## Profile Issues

### Profile Not Found

**Problem:** Specified profile doesn't exist.

**Solution:**
```bash
nlm auth list
```
List all available profiles.

### Profile Conflicts

**Problem:** Unexpected behavior with multiple profiles.

**Solution:**
- Always specify `--profile` when using multiple accounts
- Use `nlm auth delete` to remove unused profiles
- Switch profiles with `nlm login --profile <name>`

## Output Format Issues

### JSON Parse Error

**Problem:** JSON output is invalid.

**Solution:**
- Check for rate limiting or auth errors
- Some commands don't support JSON output
- Try without `--json` flag

### Quiet Mode Returns Empty

**Problem:** `--quiet` mode returns no output.

**Solution:**
- Check if the underlying query succeeded
- Some resources may not exist
- Verify the resource ID is correct

## Research Issues

### Research Timeout

**Problem:** Research takes too long or times out.

**Solution:**
- Standard research takes ~30 seconds
- Deep research takes ~5 minutes
- Use `--mode deep` for comprehensive results
- Check status with `nlm research status`

### No Sources Found

**Problem:** Research returns no sources.

**Solution:**
- Try different search queries
- Use more specific terms
- Try `--source drive` for Google Drive search

## Chrome/Headless Issues

### Chrome Crashes

**Problem:** Chrome crashes during authentication.

**Solution:**
- Ensure Chrome is fully updated
- Close all Chrome processes before running
- Try restarting your system

### Headless Mode Required

**Problem:** Chrome cannot run in headless environment.

**Solution:**
- Set environment variable for headless mode
- Check Chrome flags and permissions
- Consider using a virtual display (Xvfb)

## Common Error Messages

### "Authentication required"
Run `nlm login` to authenticate.

### "Session expired"
Run `nlm login` to refresh session.

### "Notebook not found"
Verify the notebook ID is correct using `nlm notebook list`.

### "Source not found"
Verify the source ID is correct using `nlm source list <notebook-id>`.

### "Rate limit exceeded"
Wait before making more requests.

### "Chrome not found"
Ensure Google Chrome is installed and in PATH.

### "Profile not found"
Run `nlm auth list` to see available profiles.

## Debugging Tips

### Enable Verbose Output
Some commands support verbose flags. Check command help.

### Check Logs
Look for error details in command output.

### Verify Resources First
Before generating content, verify notebook has sources:
```bash
nlm notebook get <id>
nlm source list <id>
```

### Use --json for Parsing
```bash
nlm notebook list --json | jq '.'
```

## Environment-Specific Issues

### WSL (Windows Subsystem for Linux)
- Ensure Chrome is accessible from WSL
- May need to use Windows Chrome path
- Firewall may block connections

### Docker/Containers
- Chrome must be installed in container
- May need `--cap-add=SYS_ADMIN`
- DISPLAY environment variable must be set

### Remote Servers
- Headless Chrome configuration required
- Xvfb may be needed for display
- Firewall/network restrictions apply