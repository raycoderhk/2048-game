# Discord WebSocket Health Monitor

**Status:** ✅ Active  
**Schedule:** Every 10 minutes  
**Reports To:** #system-status (Discord)

---

## Overview

Automated monitoring system that checks OpenClaw Gateway logs for Discord WebSocket instability and reports health status to the #system-status channel.

---

## What It Monitors

### 1. WebSocket Disconnections
- **Error Codes:** 1005 (No Status), 1006 (Abnormal), 1008 (Policy Violation)
- **Source:** Gateway logs (`/tmp/openclaw/openclaw-YYYY-MM-DD.log`)
- **Indicates:** Discord API connection issues, network instability, or rate limiting

### 2. Slow Listeners
- **Threshold:** >10 seconds message processing time
- **Source:** `Slow listener detected` log entries
- **Indicates:** Agent overload, memory pressure, or processing bottlenecks

### 3. Pairing Errors
- **Source:** `pairing required` log entries
- **Indicates:** Authentication/authorization issues (usually harmless in containerized environments)

---

## Alert Thresholds

| Status | Condition | Emoji |
|--------|-----------|-------|
| **✅ HEALTHY** | No errors detected | ✅ |
| **🟡 WARNING** | >0 WebSocket errors OR >0 slow listeners | 🟡 |
| **⚠️ DEGRADED** | >5 WebSocket errors OR >2 slow listeners | ⚠️ |

---

## Report Format

Reports are sent to #system-status with the following structure:

```markdown
## [Emoji] Discord WebSocket Health Check

**Status:** [STATUS]
**Time:** [ISO Timestamp]

### Metrics (Last 10 min)
| Metric | Value |
|--------|-------|
| 🔌 WebSocket Errors | X |
| 🐌 Slow Listeners | X |
| 🔐 Pairing Errors | X |

### Trends
- **Total Disconnects:** X (cumulative)
- **Consecutive Errors:** X (streak)
- **Health Status:** [healthy|warning|unhealthy]

---
*Next check: 10 minutes*
```

---

## Files

| File | Purpose |
|------|---------|
| `scripts/discord-ws-monitor.js` | Main monitoring script |
| `cron/jobs/discord-ws-health.json` | Cron job configuration |
| `memory/discord-ws-state.json` | State tracking (last check, counts, trends) |
| `docs/discord-ws-monitor.md` | This documentation |

---

## State File Schema

```json
{
  "lastCheck": "2026-03-13T08:27:40Z",
  "lastDisconnect": "2026-03-13T08:19:34Z",
  "disconnectCount": 5,
  "consecutiveErrors": 1,
  "health": "warning",
  "lastReport": "2026-03-13T08:27:40Z"
}
```

---

## Manual Testing

```bash
# Run manual health check
node /home/node/.openclaw/workspace/scripts/discord-ws-monitor.js

# View current state
cat /home/node/.openclaw/workspace/memory/discord-ws-state.json

# View recent logs
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## Cron Schedule

**Expression:** `*/10 * * * *`  
**Meaning:** Every 10 minutes  
**Timezone:** UTC (server time)

**Schedule Examples:**
- 08:00, 08:10, 08:20, 08:30, ... (UTC)
- 16:00, 16:10, 16:20, 16:30, ... (HKT)

---

## Troubleshooting

### No Reports Appearing

1. Check if cron job is enabled:
   ```bash
   cat /home/node/.openclaw/cron/jobs/discord-ws-health.json
   ```

2. Check cron logs:
   ```bash
   grep "discord-ws-health" /tmp/openclaw/openclaw-*.log
   ```

3. Manually run the script to test:
   ```bash
   node /home/node/.openclaw/workspace/scripts/discord-ws-monitor.js
   ```

### False Positives

**Gateway Restart:** After a gateway restart, expect 5-10 WebSocket errors as the system reconnects. This is normal and should clear within 10-20 minutes.

**Pairing Errors:** `pairing required` messages are expected in containerized environments and don't indicate actual problems with message processing.

### High Error Counts

If you see sustained high error counts (>10 per check):

1. **Check Discord Status:** https://discordstatus.com/
2. **Restart Gateway:** `openclaw gateway restart`
3. **Check Network:** Verify no firewall/proxy blocking Discord API
4. **Review Logs:** `tail -1000 /tmp/openclaw/openclaw-*.log | grep -E "(WebSocket|Slow listener)"`

---

## Alert Response Guide

### 🟡 WARNING (1-5 errors)

**Action:** Monitor closely  
**Likely Causes:**
- Temporary network glitch
- Discord API hiccup
- Gateway reconnection cycle

**Response:**
- Wait for next check (10 min)
- If persists, check Discord status page
- No immediate action needed

### ⚠️ DEGRADED (>5 errors or >2 slow listeners)

**Action:** Investigate  
**Likely Causes:**
- Sustained network issues
- Gateway overload
- Discord API problems
- Memory/CPU pressure

**Response:**
1. Check Discord status: https://discordstatus.com/
2. Check system resources: `free -h && top -bn1`
3. Review gateway logs: `tail -200 /tmp/openclaw/openclaw-*.log`
4. Consider gateway restart if issues persist >30 min

---

## Future Enhancements

- [ ] Add response time monitoring (ping Discord API)
- [ ] Add memory/CPU threshold alerts
- [ ] Add weekly summary reports
- [ ] Add escalation to #general-chat if degraded >1 hour
- [ ] Add historical trend tracking (daily/weekly charts)

---

## Related Documentation

- [OpenClaw Gateway Troubleshooting](./openclaw-gateway-troubleshooting.md)
- [Discord Bot Setup](./discord-bot-setup.md)
- [Cron Job Configuration](./cron-jobs.md)

---

**Created:** 2026-03-13  
**Author:** OpenClaw Assistant  
**Version:** 1.0
