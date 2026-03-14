#!/usr/bin/env node
/**
 * Discord WebSocket Health Monitor
 * Checks gateway logs for WebSocket instability and reports to #system-status
 * 
 * Usage: node discord-ws-monitor.js
 * Schedule: Every 10 minutes via cron
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const LOG_DIR = '/tmp/openclaw';
const STATE_FILE = path.join(__dirname, '../memory/discord-ws-state.json');
const CHANNEL_ID = '1476504784583393394'; // #system-status
const ALERT_THRESHOLD = {
    websocketErrors: 5,
    slowListeners: 2
};

// Get today's log file
const today = new Date().toISOString().split('T')[0];
const LOG_FILE = path.join(LOG_DIR, `openclaw-${today}.log`);

// Initialize state
function loadState() {
    try {
        if (fs.existsSync(STATE_FILE)) {
            return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('Failed to load state:', e.message);
    }
    return {
        lastCheck: null,
        lastDisconnect: null,
        disconnectCount: 0,
        consecutiveErrors: 0,
        health: 'unknown',
        lastReport: null
    };
}

function saveState(state) {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// Analyze logs
function analyzeLogs() {
    const metrics = {
        websocketErrors: 0,
        slowListeners: 0,
        pairingErrors: 0,
        lastErrorTime: null
    };

    try {
        if (!fs.existsSync(LOG_FILE)) {
            console.log('Log file not found:', LOG_FILE);
            return metrics;
        }

        // Read last 1000 lines
        const logContent = execSync(`tail -1000 "${LOG_FILE}"`, { encoding: 'utf8' });
        const lines = logContent.split('\n');

        for (const line of lines) {
            try {
                const log = JSON.parse(line);
                const msg = log[0] || '';
                const time = log.time || null;

                // Check for WebSocket errors
                if (msg.includes('WebSocket connection closed') || 
                    (log[1] && log[1].handshake === 'failed')) {
                    metrics.websocketErrors++;
                    metrics.lastErrorTime = time;
                }

                // Check for slow listeners
                if (msg.includes('Slow listener detected')) {
                    metrics.slowListeners++;
                }

                // Check for pairing errors
                if (msg.includes('pairing required')) {
                    metrics.pairingErrors++;
                }
            } catch (e) {
                // Skip non-JSON lines
            }
        }
    } catch (e) {
        console.error('Failed to analyze logs:', e.message);
    }

    return metrics;
}

// Determine health status
function getHealthStatus(metrics) {
    if (metrics.websocketErrors > ALERT_THRESHOLD.websocketErrors || 
        metrics.slowListeners > ALERT_THRESHOLD.slowListeners) {
        return { status: '⚠️ DEGRADED', emoji: '⚠️', health: 'unhealthy' };
    } else if (metrics.websocketErrors > 0 || metrics.slowListeners > 0) {
        return { status: '🟡 WARNING', emoji: '🟡', health: 'warning' };
    } else {
        return { status: '✅ HEALTHY', emoji: '✅', health: 'healthy' };
    }
}

// Generate report
function generateReport(metrics, state, healthInfo) {
    const now = new Date().toISOString();
    
    const report = {
        channel: CHANNEL_ID,
        message: `## ${healthInfo.emoji} Discord WebSocket Health Check

**Status:** ${healthInfo.status}
**Time:** ${now}

### Metrics (Last 10 min)
| Metric | Value |
|--------|-------|
| 🔌 WebSocket Errors | ${metrics.websocketErrors} |
| 🐌 Slow Listeners | ${metrics.slowListeners} |
| 🔐 Pairing Errors | ${metrics.pairingErrors} |

### Trends
- **Total Disconnects:** ${state.disconnectCount}
- **Consecutive Errors:** ${state.consecutiveErrors}
- **Health Status:** ${healthInfo.health}

---
*Next check: 10 minutes*`
    };

    return report;
}

// Send message via OpenClaw
function sendMessage(report) {
    try {
        // Use OpenClaw CLI to send message
        const messageCmd = `openclaw message send --target "discord:channel:${report.channel}" --message ${JSON.stringify(report.message).replace(/"/g, '\\"')}`;
        execSync(messageCmd, { stdio: 'inherit' });
        console.log('Report sent successfully');
        return true;
    } catch (e) {
        console.error('Failed to send message:', e.message);
        return false;
    }
}

// Main execution
function main() {
    console.log('Starting Discord WebSocket health check...');
    
    // Load state
    const state = loadState();
    
    // Analyze logs
    const metrics = analyzeLogs();
    
    // Get health status
    const healthInfo = getHealthStatus(metrics);
    
    // Update state
    const now = new Date().toISOString();
    state.lastCheck = now;
    state.health = healthInfo.health;
    
    if (metrics.websocketErrors > 0) {
        state.disconnectCount += metrics.websocketErrors;
        state.consecutiveErrors++;
        if (metrics.lastErrorTime) {
            state.lastDisconnect = metrics.lastErrorTime;
        }
    } else {
        state.consecutiveErrors = 0;
    }
    
    // Save state
    saveState(state);
    
    // Generate and send report
    const report = generateReport(metrics, state, healthInfo);
    
    // Always send if unhealthy, otherwise send every 6th check (hourly summary)
    const shouldSend = healthInfo.health !== 'healthy' || state.consecutiveErrors === 0;
    
    if (shouldSend) {
        sendMessage(report);
    } else {
        console.log('Skipping report (healthy, will send hourly summary)');
    }
    
    console.log(`Health check complete: ${healthInfo.status}`);
    console.log(`Metrics: WS=${metrics.websocketErrors}, Slow=${metrics.slowListeners}, Pairing=${metrics.pairingErrors}`);
}

main();
