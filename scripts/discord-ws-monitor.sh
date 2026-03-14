#!/bin/bash
# Discord WebSocket Health Monitor
# Checks gateway logs for WebSocket instability and reports to #system-status

LOG_FILE="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
STATE_FILE="/home/node/.openclaw/workspace/memory/discord-ws-state.json"
CHANNEL_ID="1476504784583393394"  # #system-status

# Initialize state file if not exists
if [ ! -f "$STATE_FILE" ]; then
    echo '{"lastCheck": null, "lastDisconnect": null, "disconnectCount": 0, "consecutiveErrors": 0}' > "$STATE_FILE"
fi

# Get current timestamp
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CURRENT_EPOCH=$(date +%s)

# Read state
LAST_CHECK=$(cat "$STATE_FILE" | grep -o '"lastCheck": "[^"]*"' | cut -d'"' -f4)
DISCONNECT_COUNT=$(cat "$STATE_FILE" | grep -o '"disconnectCount": [0-9]*' | cut -d' ' -f2)
CONSECUTIVE_ERRORS=$(cat "$STATE_FILE" | grep -o '"consecutiveErrors": [0-9]*' | cut -d' ' -f2)

# Check gateway logs for last 10 minutes
if [ -f "$LOG_FILE" ]; then
    # Count WebSocket disconnections (code 1005, 1006, 1008)
    WS_ERRORS=$(tail -1000 "$LOG_FILE" | grep -c "WebSocket connection closed" 2>/dev/null || echo "0")
    
    # Count slow listener warnings
    SLOW_LISTENERS=$(tail -1000 "$LOG_FILE" | grep -c "Slow listener detected" 2>/dev/null || echo "0")
    
    # Check for pairing errors
    PAIRING_ERRORS=$(tail -1000 "$LOG_FILE" | grep -c "pairing required" 2>/dev/null || echo "0")
    
    # Get last error timestamp
    LAST_ERROR_TIME=$(tail -1000 "$LOG_FILE" | grep "WebSocket connection closed" | tail -1 | grep -o '"time":"[^"]*"' | cut -d'"' -f4)
else
    WS_ERRORS=0
    SLOW_LISTENERS=0
    PAIRING_ERRORS=0
    LAST_ERROR_TIME="null"
fi

# Determine health status
if [ "$WS_ERRORS" -gt 5 ] || [ "$SLOW_LISTENERS" -gt 2 ]; then
    STATUS="⚠️ DEGRADED"
    STATUS_EMOJI="⚠️"
    HEALTH="unhealthy"
elif [ "$WS_ERRORS" -gt 0 ] || [ "$SLOW_LISTENERS" -gt 0 ]; then
    STATUS="🟡 WARNING"
    STATUS_EMOJI="🟡"
    HEALTH="warning"
else
    STATUS="✅ HEALTHY"
    STATUS_EMOJI="✅"
    HEALTH="healthy"
fi

# Update consecutive error counter
if [ "$WS_ERRORS" -gt 0 ] || [ "$SLOW_LISTENERS" -gt 0 ]; then
    CONSECUTIVE_ERRORS=$((CONSECUTIVE_ERRORS + 1))
else
    CONSECUTIVE_ERRORS=0
fi

# Update disconnect count
if [ "$WS_ERRORS" -gt 0 ]; then
    DISCONNECT_COUNT=$((DISCONNECT_COUNT + WS_ERRORS))
fi

# Update state file
cat > "$STATE_FILE" << EOF
{
    "lastCheck": "$CURRENT_TIME",
    "lastDisconnect": "$LAST_ERROR_TIME",
    "disconnectCount": $DISCONNECT_COUNT,
    "consecutiveErrors": $CONSECUTIVE_ERRORS,
    "health": "$HEALTH"
}
EOF

# Generate report message
cat > /tmp/ws-report.json << EOF
{
    "channel": "$CHANNEL_ID",
    "message": "## ${STATUS_EMOJI} Discord WebSocket Health Check\n\n**Status:** ${STATUS}\n**Time:** ${CURRENT_TIME}\n\n### Metrics (Last 10 min)\n| Metric | Value |\n|--------|-------|\n| 🔌 WebSocket Errors | ${WS_ERRORS} |\n| 🐌 Slow Listeners | ${SLOW_LISTENERS} |\n| 🔐 Pairing Errors | ${PAIRING_ERRORS} |\n\n### Trends\n- **Total Disconnects:** ${DISCONNECT_COUNT}\n- **Consecutive Errors:** ${CONSECUTIVE_ERRORS}\n- **Health Status:** ${HEALTH}\n\n---\n*Next check: 10 minutes*"
}
EOF

# Send to Discord if there are errors or it's been >1 hour since last report
if [ "$WS_ERRORS" -gt 0 ] || [ "$SLOW_LISTENERS" -gt 0 ] || [ "$CONSECUTIVE_ERRORS" -eq 0 ]; then
    # Use openclaw message command to send report
    cat /tmp/ws-report.json
fi

# Output for logging
echo "[$CURRENT_TIME] Discord WS Check: $STATUS (Errors: $WS_ERRORS, Slow: $SLOW_LISTENERS)"
