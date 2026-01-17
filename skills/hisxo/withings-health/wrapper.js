const https = require('https');
const fs = require('fs');
const path = require('path');
const querystring = require('querystring');

// CONFIGURATION
// Load from local .env file if present
try {
    const envPath = path.join(__dirname, '.env');
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        envContent.split('\n').forEach(line => {
            const [key, value] = line.split('=');
            if (key && value) process.env[key.trim()] = value.trim().replace(/['"]/g, '');
        });
    }
} catch (e) {}

const CLIENT_ID = process.env.WITHINGS_CLIENT_ID;
const CLIENT_SECRET = process.env.WITHINGS_CLIENT_SECRET;
const REDIRECT_URI = 'http://localhost:8080'; // Must match your Withings app config
const TOKEN_FILE = path.join(__dirname, 'tokens.json');

// --- UTILITY FUNCTIONS ---

function saveTokens(data) {
    // Calculate expiration (expires_in is in seconds)
    const expiry = Date.now() + (data.expires_in * 1000);
    const payload = { ...data, expiry_date: expiry };
    fs.writeFileSync(TOKEN_FILE, JSON.stringify(payload, null, 2));
    return payload;
}

function postRequest(endpoint, params) {
    return new Promise((resolve, reject) => {
        const postData = querystring.stringify(params);
        const options = {
            hostname: 'wbsapi.withings.net',
            path: endpoint,
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': postData.length
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.status !== 0) reject(`API Error Status: ${json.status} - ${JSON.stringify(json)}`);
                    else resolve(json.body);
                } catch (e) { reject(e); }
            });
        });
        req.on('error', (e) => reject(e));
        req.write(postData);
        req.end();
    });
}

async function getValidToken() {
    if (!fs.existsSync(TOKEN_FILE)) {
        throw new Error("No token found. Run first: node wrapper.js auth");
    }

    let tokens = JSON.parse(fs.readFileSync(TOKEN_FILE));

    // Refresh if token expires in less than 60 seconds
    if (Date.now() > (tokens.expiry_date - 60000)) {
        console.error("Token expired, refreshing...");
        try {
            const newTokens = await postRequest('/v2/oauth2', {
                action: 'requesttoken',
                grant_type: 'refresh_token',
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                refresh_token: tokens.refresh_token
            });
            tokens = saveTokens(newTokens);
        } catch (e) {
            throw new Error(`Failed to refresh token: ${e}`);
        }
    }
    return tokens.access_token;
}

// --- COMMANDS ---

async function auth(code) {
    if (!code) {
        const url = `https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=user.metrics,user.activity&state=init`;
        console.log("\n=== AUTHENTICATION REQUIRED ===");
        console.log("1. Open this link in your browser:");
        console.log(url);
        console.log("\n2. After login, you'll be redirected to an error page (this is normal).");
        console.log("3. Copy the code from the URL (e.g., ?code=my_code&...)");
        console.log("4. Run: node wrapper.js auth YOUR_CODE_HERE\n");
        return;
    }

    try {
        const tokens = await postRequest('/v2/oauth2', {
            action: 'requesttoken',
            grant_type: 'authorization_code',
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: code,
            redirect_uri: REDIRECT_URI
        });
        saveTokens(tokens);
        console.log("Authentication successful! Tokens saved.");
    } catch (e) {
        console.error("Authentication error:", e);
    }
}

async function getWeight() {
    try {
        const token = await getValidToken();
        const data = await postRequest('/measure', {
            action: 'getmeas',
            access_token: token,
            meastype: 1, // 1 = Weight
            category: 1
        });
        
        // Withings returns raw values with a power of 10 (unit)
        const measures = data.measuregrps.map(grp => {
            const date = new Date(grp.date * 1000).toISOString();
            const meas = grp.measures.find(m => m.type === 1);
            const weight = meas.value * Math.pow(10, meas.unit);
            return { date, weight: weight.toFixed(2) + ' kg' };
        });

        console.log(JSON.stringify(measures.slice(0, 5), null, 2)); // Last 5 entries
    } catch (e) {
        console.error(e.message);
    }
}

// Measure types reference:
// 1 = Weight (kg), 4 = Height (m), 5 = Fat Free Mass (kg), 6 = Fat Ratio (%)
// 8 = Fat Mass Weight (kg), 9 = Diastolic BP (mmHg), 10 = Systolic BP (mmHg)
// 11 = Heart Pulse (bpm), 76 = Muscle Mass (kg), 77 = Hydration (kg), 88 = Bone Mass (kg)

async function getBodyComposition() {
    try {
        const token = await getValidToken();
        // Request all body composition measures at once
        const data = await postRequest('/measure', {
            action: 'getmeas',
            access_token: token,
            category: 1 // Real measurements only
        });
        
        const measures = data.measuregrps.map(grp => {
            const date = new Date(grp.date * 1000).toISOString();
            const result = { date };
            
            grp.measures.forEach(m => {
                const value = m.value * Math.pow(10, m.unit);
                switch (m.type) {
                    case 1: result.weight = value.toFixed(2) + ' kg'; break;
                    case 6: result.fat_percent = value.toFixed(1) + '%'; break;
                    case 8: result.fat_mass = value.toFixed(2) + ' kg'; break;
                    case 76: result.muscle_mass = value.toFixed(2) + ' kg'; break;
                    case 77: result.hydration = value.toFixed(1) + '%'; break;
                    case 88: result.bone_mass = value.toFixed(2) + ' kg'; break;
                }
            });
            
            return result;
        }).filter(m => Object.keys(m).length > 1); // Only include if we have data

        console.log(JSON.stringify(measures.slice(0, 5), null, 2));
    } catch (e) {
        console.error(e.message);
    }
}

async function getActivity(days = 7) {
    try {
        const token = await getValidToken();
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);
        
        const formatDate = (d) => d.toISOString().split('T')[0];
        
        const data = await postRequest('/v2/measure', {
            action: 'getactivity',
            access_token: token,
            startdateymd: formatDate(startDate),
            enddateymd: formatDate(endDate)
        });
        
        if (!data.activities || data.activities.length === 0) {
            console.log("[]");
            return;
        }
        
        const formatMinutes = (min) => {
            if (!min) return '0 min';
            return min + ' min';
        };
        
        const activities = data.activities.map(a => ({
            date: a.date,
            steps: a.steps || 0,
            distance: ((a.distance || 0) / 1000).toFixed(2) + ' km',
            calories: a.calories || 0,
            active_calories: a.active_calories || 0,
            soft_activity: formatMinutes(a.soft),
            moderate_activity: formatMinutes(a.moderate),
            intense_activity: formatMinutes(a.intense)
        }));
        
        console.log(JSON.stringify(activities.reverse(), null, 2)); // Most recent first
    } catch (e) {
        console.error(e.message);
    }
}

async function getSleep(days = 7) {
    try {
        const token = await getValidToken();
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);
        
        const formatDate = (d) => d.toISOString().split('T')[0];
        
        const data = await postRequest('/v2/sleep', {
            action: 'getsummary',
            access_token: token,
            startdateymd: formatDate(startDate),
            enddateymd: formatDate(endDate)
        });
        
        if (!data.series || data.series.length === 0) {
            console.log("[]");
            return;
        }
        
        const formatDuration = (seconds) => {
            if (!seconds) return '0min';
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            if (h > 0) return `${h}h ${m}min`;
            return `${m}min`;
        };
        
        const formatTime = (timestamp) => {
            const d = new Date(timestamp * 1000);
            return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        };
        
        const sleepData = data.series.map(s => ({
            date: s.date,
            start: formatTime(s.startdate),
            end: formatTime(s.enddate),
            duration: formatDuration(s.data?.total_sleep_time || s.data?.durationtosleep),
            deep_sleep: formatDuration(s.data?.deepsleepduration),
            light_sleep: formatDuration(s.data?.lightsleepduration),
            rem_sleep: formatDuration(s.data?.remsleepduration),
            awake: formatDuration(s.data?.wakeupcount ? s.data.wakeupduration : 0),
            sleep_score: s.data?.sleep_score || null
        }));
        
        console.log(JSON.stringify(sleepData.reverse(), null, 2)); // Most recent first
    } catch (e) {
        console.error(e.message);
    }
}

// --- MAIN ---
const args = process.argv.slice(2);
const command = args[0];

if (command === 'auth') auth(args[1]);
else if (command === 'weight') getWeight();
else if (command === 'body') getBodyComposition();
else if (command === 'activity') getActivity(parseInt(args[1]) || 7);
else if (command === 'sleep') getSleep(parseInt(args[1]) || 7);
else console.log("Commands: auth, weight, body, activity [days], sleep [days]");
