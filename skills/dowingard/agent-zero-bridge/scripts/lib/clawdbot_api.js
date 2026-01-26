/**
 * Clawdbot API Client Library
 */

const config = require('./config');

class ClawdbotClient {
    constructor(options = {}) {
        // Use Docker URL if running inside container, otherwise regular URL
        const isDocker = process.env.DOCKER_CONTAINER === 'true';
        this.apiUrl = options.apiUrl || (isDocker ? config.clawdbot.apiUrlDocker : config.clawdbot.apiUrl);
        this.apiToken = options.apiToken || config.clawdbot.apiToken;
        this.defaultTimeout = options.timeout || config.clawdbot.defaultTimeout;

        if (!this.apiToken) {
            console.warn("Warning: CLAWDBOT_API_TOKEN not set. Set it in .env or environment.");
        }
    }

    async request(endpoint, method = 'POST', body = null, timeout = null) {
        const controller = new AbortController();
        const timeoutMs = timeout || this.defaultTimeout;
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiToken}`
                },
                signal: controller.signal
            };

            if (body) {
                options.body = JSON.stringify(body);
            }

            const response = await fetch(`${this.apiUrl}${endpoint}`, options);
            clearTimeout(timeoutId);

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`HTTP ${response.status}: ${text}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error(`Request timed out after ${timeoutMs}ms`);
            }
            throw error;
        }
    }

    // Send message via OpenAI-compatible chat completions
    async sendMessage(message, options = {}) {
        const payload = {
            model: "clawdbot:main",
            messages: [
                {
                    role: "user",
                    content: options.prefix ? `${options.prefix}\n\n${message}` : message
                }
            ],
            stream: false
        };

        const data = await this.request('/v1/chat/completions', 'POST', payload, options.timeout);
        return data.choices?.[0]?.message?.content || "No response";
    }

    // Invoke a Clawdbot tool directly
    async invokeTool(tool, args = {}, sessionKey = "main") {
        const payload = {
            tool,
            args,
            sessionKey
        };

        const data = await this.request('/tools/invoke', 'POST', payload);
        return data.result || data;
    }

    // Send notification (fire and forget via sessions_send)
    async notify(message) {
        try {
            return await this.invokeTool('sessions_send', {
                sessionKey: 'main',
                message: `[Agent Zero Notification]\n\n${message}`
            });
        } catch (error) {
            // Fallback to chat completions
            return await this.sendMessage(message, { prefix: '[Agent Zero Notification]' });
        }
    }
}

module.exports = ClawdbotClient;
