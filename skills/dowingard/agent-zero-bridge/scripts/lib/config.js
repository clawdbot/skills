/**
 * Shared Configuration
 * Reads from environment variables or .env file
 */

const path = require('path');

// Load .env file if it exists
try {
    const fs = require('fs');
    const envPath = path.join(__dirname, '..', '.env');
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        envContent.split('\n').forEach(line => {
            const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
            if (match && !process.env[match[1]]) {
                process.env[match[1]] = match[2] || '';
            }
        });
    }
} catch (err) {
    // Ignore errors loading .env
}

const config = {
    // Agent Zero
    a0: {
        apiUrl: process.env.A0_API_URL || "http://127.0.0.1:50001",
        apiKey: process.env.A0_API_KEY || "",
        contextFile: path.join(__dirname, '..', '.a0_context'),
        defaultTimeout: parseInt(process.env.A0_TIMEOUT) || 120000,
        lifetimeHours: parseInt(process.env.A0_LIFETIME_HOURS) || 24
    },
    
    // Clawdbot Gateway
    clawdbot: {
        apiUrl: process.env.CLAWDBOT_API_URL || "http://127.0.0.1:18789",
        apiUrlDocker: process.env.CLAWDBOT_API_URL_DOCKER || process.env.CLAWDBOT_API_URL || "http://127.0.0.1:18789",
        apiToken: process.env.CLAWDBOT_API_TOKEN || "",
        defaultTimeout: parseInt(process.env.CLAWDBOT_TIMEOUT) || 60000
    },
    
    // Notebook
    notebook: {
        path: process.env.NOTEBOOK_PATH || path.join(__dirname, '..', 'notebook')
    }
};

// Validation
function validateConfig() {
    const errors = [];
    
    if (!config.a0.apiKey) {
        errors.push("A0_API_KEY is not set");
    }
    if (!config.clawdbot.apiToken) {
        errors.push("CLAWDBOT_API_TOKEN is not set");
    }
    
    return errors;
}

config.validate = validateConfig;

module.exports = config;
