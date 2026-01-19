const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 18795;
const FRAME_PATH = '/tmp/clawdbot-screen-latest.png';
const META_PATH = '/tmp/clawdbot-screen-latest.json';

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.url === '/screen-share' || req.url === '/screen-share.html') {
        const htmlPath = path.join(__dirname, '../web/screen-share.html');
        fs.readFile(htmlPath, 'utf8', (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Not found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
        });
        return;
    }

    if (req.url === '/api/screen-frame' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const { frame, timestamp, width, height } = JSON.parse(body);
                const buffer = Buffer.from(frame, 'base64');
                fs.writeFileSync(FRAME_PATH, buffer);
                fs.writeFileSync(META_PATH, JSON.stringify({
                    timestamp, width, height, active: true,
                    updated: new Date().toISOString()
                }));
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok' }));
            } catch (err) {
                res.writeHead(400);
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    if (req.url === '/api/screen-status') {
        if (fs.existsSync(META_PATH)) {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(fs.readFileSync(META_PATH, 'utf8'));
        } else {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ active: false }));
        }
        return;
    }

    res.writeHead(404);
    res.end('Not found');
});

server.listen(PORT, () => {
    console.log('Screen share server: http://localhost:' + PORT + '/screen-share');
});
