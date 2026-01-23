# Unraid API Endpoints Reference

Complete list of available GraphQL read-only endpoints in Unraid 7.2+.

## System & Metrics (8)
1. **`info`** - Hardware specs (CPU, OS, motherboard)
2. **`metrics`** - Real-time CPU/memory usage
3. **`online`** - Server online status
4. **`isInitialSetup`** - Setup completion status
5. **`config`** - System configuration
6. **`vars`** - System variables
7. **`settings`** - System settings
8. **`logFiles`** - List all log files

## Storage (4)
9. **`array`** - Array status, disks, parity
10. **`disks`** - All physical disks (array + cache + USB)
11. **`shares`** - Network shares
12. **`logFile`** - Read log content

## Virtualization (2)
13. **`docker`** - Docker containers
14. **`vms`** - Virtual machines

## Monitoring (2)
15. **`notifications`** - System alerts
16. **`upsDevices`** - UPS battery status

## User & Auth (4)
17. **`me`** - Current user info
18. **`owner`** - Server owner
19. **`isSSOEnabled`** - SSO status
20. **`oidcProviders`** - OIDC providers

## API Management (2)
21. **`apiKeys`** - List API keys

## Customization (3)
22. **`customization`** - UI theme & settings
23. **`publicTheme`** - Public theme
24. **`publicPartnerInfo`** - Partner branding

## Server Management (3)
25. **`registration`** - License info
26. **`server`** - Server metadata
27. **`servers`** - Multi-server management

## Bonus (1)
28. **`plugins`** - Installed plugins (returns empty array if none)
