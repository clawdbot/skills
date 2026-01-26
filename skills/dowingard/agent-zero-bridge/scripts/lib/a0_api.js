/**
 * Agent Zero API Client Library
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

class A0Client {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || config.a0.apiUrl;
        this.apiKey = options.apiKey || config.a0.apiKey;
        this.contextFile = options.contextFile || config.a0.contextFile;
        this.defaultTimeout = options.timeout || config.a0.defaultTimeout;
        this.lifetimeHours = options.lifetimeHours || config.a0.lifetimeHours;

        if (!this.apiKey) {
            console.warn("Warning: A0_API_KEY not set. Set it in .env or environment.");
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
                    'X-API-KEY': this.apiKey
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

    // Context management
    loadContext() {
        try {
            if (fs.existsSync(this.contextFile)) {
                return fs.readFileSync(this.contextFile, 'utf8').trim();
            }
        } catch (err) {}
        return null;
    }

    saveContext(contextId) {
        try {
            fs.writeFileSync(this.contextFile, contextId);
        } catch (err) {}
    }

    clearContext() {
        try {
            if (fs.existsSync(this.contextFile)) {
                fs.unlinkSync(this.contextFile);
            }
        } catch (err) {}
    }

    // API methods
    async sendMessage(message, options = {}) {
        const contextId = options.new ? null : (options.context || this.loadContext());
        
        const attachments = [];
        if (options.attach) {
            const files = Array.isArray(options.attach) ? options.attach : [options.attach];
            for (const filePath of files) {
                try {
                    const content = fs.readFileSync(filePath);
                    attachments.push({
                        filename: path.basename(filePath),
                        base64: content.toString('base64')
                    });
                } catch (err) {
                    console.warn(`Warning: Could not read attachment ${filePath}`);
                }
            }
        }

        const payload = {
            message,
            context_id: contextId || undefined,
            attachments: attachments.length > 0 ? attachments : undefined,
            lifetime_hours: this.lifetimeHours
        };

        const data = await this.request('/api_message', 'POST', payload, options.timeout);

        if (data.context_id) {
            this.saveContext(data.context_id);
        }

        return data.response || data.message || "No response received";
    }

    async reset(options = {}) {
        const contextId = options.context || this.loadContext();
        if (!contextId) return "No active context to reset";

        await this.request('/api_reset_chat', 'POST', { context_id: contextId });
        this.clearContext();
        return "Conversation reset successfully";
    }

    async status() {
        const data = await this.request('/health', 'GET');
        return { status: 'online', git: data.gitinfo, error: data.error };
    }

    async history(options = {}) {
        const contextId = options.context || this.loadContext();
        if (!contextId) return { error: "No active context" };

        const data = await this.request('/api_log_get', 'POST', { 
            context_id: contextId, 
            length: options.length || 50 
        });
        
        return {
            contextId: data.context_id,
            totalItems: data.log?.total_items || 0,
            items: data.log?.items || []
        };
    }

    getContext() {
        return this.loadContext();
    }

    setContext(contextId) {
        this.saveContext(contextId);
        return contextId;
    }
}

module.exports = A0Client;
