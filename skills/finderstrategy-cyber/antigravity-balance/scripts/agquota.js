#!/usr/bin/env node
/**
 * agquota - Check Antigravity AI model quota
 * Detects local Antigravity process and queries its API
 */

const https = require('https');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// Parse arguments
const args = process.argv.slice(2);
const jsonOutput = args.includes('--json');
const verbose = args.includes('-v') || args.includes('--verbose');
const help = args.includes('-h') || args.includes('--help');

if (help) {
    console.log(`
agquota - Check Antigravity AI model quota

Usage: agquota [OPTIONS]

Options:
  --json       Output as JSON
  -v, --verbose    Verbose output
  -h, --help   Show this help
`);
    process.exit(0);
}

const log = (msg) => {
    if (verbose) console.error(`[DEBUG] ${msg}`);
};

const error = (msg) => {
    console.error(`Error: ${msg}`);
    process.exit(1);
};

// Colors for terminal output
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    bold: '\x1b[1m',
    reset: '\x1b[0m'
};

// Detect platform and get process name
function getProcessName() {
    const platform = process.platform;
    const arch = process.arch;
    
    if (platform === 'darwin') {
        return arch === 'arm64' ? 'language_server_macos_arm' : 'language_server_macos';
    } else if (platform === 'linux') {
        return 'language_server_linux';
    } else if (platform === 'win32') {
        return 'language_server_windows_x64.exe';
    }
    error(`Unsupported platform: ${platform}`);
}

// Find Antigravity process
async function findAntigravityProcess(processName) {
    log(`Looking for process: ${processName}`);
    
    let stdout;
    if (process.platform === 'win32') {
        // Windows: use PowerShell
        const cmd = `powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'name=''${processName}''' | Select-Object ProcessId,CommandLine | ConvertTo-Json"`;
        try {
            const result = await execAsync(cmd, { timeout: 15000 });
            stdout = result.stdout;
        } catch (e) {
            error(`Failed to query processes: ${e.message}`);
        }
    } else {
        // macOS/Linux: use ps
        try {
            const result = await execAsync(`ps -ww -eo pid,args | grep "${processName}" | grep -v grep`, { timeout: 5000 });
            stdout = result.stdout;
        } catch (e) {
            if (e.code === 1) {
                error('Antigravity process not found. Is Antigravity/Windsurf running?');
            }
            error(`Failed to query processes: ${e.message}`);
        }
    }
    
    if (!stdout || !stdout.trim()) {
        error('Antigravity process not found. Is Antigravity/Windsurf running?');
    }
    
    log(`Process output:\n${stdout}`);
    
    // Find line with --app_data_dir antigravity
    const lines = stdout.split('\n').filter(l => l.trim());
    const antigravityLine = lines.find(l => /--app_data_dir\s+antigravity\b/i.test(l));
    
    if (!antigravityLine) {
        error('Found language_server but it\'s not an Antigravity instance');
    }
    
    log(`Antigravity line: ${antigravityLine}`);
    
    // Extract port and token
    const portMatch = antigravityLine.match(/--extension_server_port[= ]+(\d+)/);
    const tokenMatch = antigravityLine.match(/--csrf_token[= ]+([a-f0-9-]+)/i);
    
    if (!portMatch || !tokenMatch) {
        error('Could not extract connection info from process');
    }
    
    const extensionPort = parseInt(portMatch[1], 10);
    
    return {
        extensionPort,
        token: tokenMatch[1]
    };
}

// Find the actual API port by scanning nearby ports
async function findApiPort(extensionPort, token) {
    // The API port is typically extensionPort + 1, but scan a few ports to be safe
    const portsToTry = [
        extensionPort + 1,  // Most common
        extensionPort,
        extensionPort + 2,
        extensionPort - 1
    ];
    
    for (const port of portsToTry) {
        log(`Testing port ${port}...`);
        const works = await testPort(port, token);
        if (works) {
            log(`Found working API port: ${port}`);
            return port;
        }
    }
    
    // Fallback: scan a wider range
    log('Primary ports failed, scanning range...');
    for (let p = extensionPort - 10; p <= extensionPort + 10; p++) {
        if (portsToTry.includes(p)) continue;
        const works = await testPort(p, token);
        if (works) {
            log(`Found working API port: ${p}`);
            return p;
        }
    }
    
    error(`Could not find working API port near ${extensionPort}`);
}

// Test if a port responds to the API
function testPort(port, token) {
    return new Promise((resolve) => {
        const req = https.request({
            hostname: '127.0.0.1',
            port: port,
            path: '/exa.language_server_pb.LanguageServerService/GetUnleashData',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Connect-Protocol-Version': '1',
                'X-Codeium-Csrf-Token': token
            },
            rejectUnauthorized: false,
            timeout: 2000
        }, res => {
            resolve(res.statusCode === 200);
        });
        req.on('error', () => resolve(false));
        req.on('timeout', () => { req.destroy(); resolve(false); });
        req.write(JSON.stringify({ wrapper_data: {} }));
        req.end();
    });
}

// Make HTTPS request to local API
function queryApi(port, token, endpoint, payload) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(payload);
        
        const options = {
            hostname: '127.0.0.1',
            port: port,
            path: endpoint,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data),
                'Connect-Protocol-Version': '1',
                'X-Codeium-Csrf-Token': token
            },
            rejectUnauthorized: false,
            timeout: 10000
        };
        
        log(`Requesting: https://127.0.0.1:${port}${endpoint}`);
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                log(`Response status: ${res.statusCode}`);
                if (res.statusCode !== 200) {
                    reject(new Error(`API returned status ${res.statusCode}`));
                    return;
                }
                try {
                    resolve(JSON.parse(body));
                } catch (e) {
                    reject(new Error(`Failed to parse response: ${e.message}`));
                }
            });
        });
        
        req.on('error', (e) => reject(e));
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });
        
        req.write(data);
        req.end();
    });
}

// Format time delta
function formatDelta(ms) {
    if (ms <= 0) return 'Now';
    
    const totalMinutes = Math.ceil(ms / 60000);
    
    if (totalMinutes < 60) {
        return `${totalMinutes}m`;
    }
    
    const totalHours = Math.floor(totalMinutes / 60);
    const remainingMinutes = totalMinutes % 60;
    
    if (totalHours < 24) {
        return `${totalHours}h ${remainingMinutes}m`;
    }
    
    const days = Math.floor(totalHours / 24);
    const remainingHours = totalHours % 24;
    return `${days}d ${remainingHours}h ${remainingMinutes}m`;
}

// Create progress bar
function progressBar(percent) {
    const width = 20;
    const filled = Math.round(percent * width / 100);
    const empty = width - filled;
    return '█'.repeat(filled) + '░'.repeat(empty);
}

// Get status color
function statusColor(percent) {
    if (percent > 50) return colors.green;
    if (percent > 20) return colors.yellow;
    return colors.red;
}

// Display quota in human-readable format
function displayQuota(response) {
    const status = response.userStatus || {};
    const userName = status.name || 'Unknown';
    const userEmail = status.email || 'N/A';
    const tier = status.userTier?.name || status.planStatus?.planInfo?.teamsTier || 'N/A';
    
    console.log(`\n${colors.bold}🚀 Antigravity Quota Status${colors.reset}`);
    console.log('━'.repeat(45));
    console.log(`${colors.cyan}User:${colors.reset} ${userName} (${userEmail})`);
    console.log(`${colors.cyan}Tier:${colors.reset} ${tier}`);
    console.log();
    
    const configs = status.cascadeModelConfigData?.clientModelConfigs || [];
    const modelsWithQuota = configs.filter(m => m.quotaInfo);
    
    if (modelsWithQuota.length === 0) {
        console.log(`${colors.yellow}No model quota information available${colors.reset}`);
        return;
    }
    
    console.log(`${colors.bold}Models:${colors.reset}\n`);
    
    const now = Date.now();
    
    for (const model of modelsWithQuota) {
        const label = model.label || 'Unknown';
        const fraction = model.quotaInfo.remainingFraction || 0;
        const percent = Math.round(fraction * 100);
        const color = statusColor(percent);
        const bar = progressBar(percent);
        
        let resetDisplay = 'N/A';
        if (model.quotaInfo.resetTime) {
            const resetMs = new Date(model.quotaInfo.resetTime).getTime();
            const delta = resetMs - now;
            resetDisplay = formatDelta(delta);
        }
        
        console.log(`  ${colors.bold}${label.padEnd(30)}${colors.reset} ${color}${String(percent).padStart(3)}%${colors.reset} ${bar}  ⏱️  ${resetDisplay}`);
    }
    
    console.log();
}

// Display quota as JSON
function displayJson(response) {
    const status = response.userStatus || {};
    const configs = status.cascadeModelConfigData?.clientModelConfigs || [];
    
    const output = {
        user: {
            name: status.name,
            email: status.email,
            tier: status.userTier?.name || status.planStatus?.planInfo?.teamsTier || 'N/A'
        },
        models: configs
            .filter(m => m.quotaInfo)
            .map(m => ({
                label: m.label,
                modelId: m.modelOrAlias?.model || 'unknown',
                remainingPercent: (m.quotaInfo.remainingFraction || 0) * 100,
                isExhausted: (m.quotaInfo.remainingFraction || 0) <= 0,
                resetTime: m.quotaInfo.resetTime
            })),
        timestamp: new Date().toISOString()
    };
    
    console.log(JSON.stringify(output, null, 2));
}

// Main
async function main() {
    try {
        const processName = getProcessName();
        log(`Target process: ${processName}`);
        
        const { extensionPort, token } = await findAntigravityProcess(processName);
        log(`Found: extensionPort=${extensionPort}, token=${token.substring(0, 8)}...`);
        
        // Find the actual API port
        const apiPort = await findApiPort(extensionPort, token);
        log(`API port: ${apiPort}`);
        
        const response = await queryApi(
            apiPort,
            token,
            '/exa.language_server_pb.LanguageServerService/GetUserStatus',
            {
                metadata: {
                    ideName: 'antigravity',
                    extensionName: 'antigravity',
                    locale: 'en'
                }
            }
        );
        
        if (jsonOutput) {
            displayJson(response);
        } else {
            displayQuota(response);
        }
    } catch (e) {
        error(e.message);
    }
}

main();

