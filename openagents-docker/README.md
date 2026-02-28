# OpenAgents Deployment Guide for Zeabur

## Option 1: One-Click Template (Easiest)

### Steps:
1. Go to https://zeabur.com/templates
2. Search "OpenAgents"
3. Click "Deploy"
4. Configure:
   - Subdomain: `jarvis.zeabur.app`
   - Region: Tokyo/Jakarta (closest to HK)
   - Cluster: Flex Shared (free tier)
5. Deploy! (1-2 minutes)

### If Template Not Found:
Zeabur templates change frequently. If OpenAgents isn't listed, use Option 2.

---

## Option 2: Manual Docker Deployment

### Via Zeabur Dashboard:
1. Go to https://zeabur.com/dashboard
2. Click "New Service"
3. Select "Docker"
4. Image: `ghcr.io/openagents-org/openagents:latest`
5. Configure ports: 8700 (HTTP), 8600 (gRPC)
6. Add environment variables:
   ```
   ALIYUN_API_KEY=sk-sp-8eec812bc72d47c3866d388cef6372f8
   MAX_SPAWN_DEPTH=2
   MAX_CONCURRENT=8
   TIMEOUT=900
   ```
7. Deploy!

### Via GitHub (Recommended):
1. Create repo: `openagents-deploy`
2. Add `docker-compose.yml` (provided)
3. Connect Zeabur to GitHub repo
4. Deploy!

---

## Option 3: Alternative Agent Frameworks

If OpenAgents doesn't work, try these Zeabur-compatible frameworks:

### A. LangChain + FastAPI
- Template available on Zeabur
- Supports multi-agent workflows
- Python-based

### B. AutoGen (Microsoft)
- Docker deployment
- Native sub-agent support
- Well-documented

### C. CrewAI
- Lightweight
- Role-based agents
- Easy Zeabur deployment

---

## Jarvis Configuration (Chief-of-Staff)

### Main Agent Prompt:
```
You are Jarvis, the chief-of-staff orchestrator.

Your role:
1. Receive user requests
2. Instantly delegate to specialized sub-agents
3. Keep responses concise and actionable
4. Monitor sub-agent progress
5. Consolidate results

Delegation rules:
- Research tasks → Research Agent
- Code tasks → Coding Agent
- Schedule/Admin → Admin Agent
- General chat → Handle directly

Keep the main interface responsive!
```

### Sub-Agent Configuration:

| Agent | Role | Model | Max Tokens |
|-------|------|-------|------------|
| **Research** | Search, analysis | DeepSeek | 4000 |
| **Coding** | Code generation | DeepSeek Coder | 8000 |
| **Admin** | Schedule, reminders | Lightweight | 2000 |

---

## Delegation Commands

### Spawn Sub-Agent:
```
/subagents spawn research "Search for AI news"
/subagents spawn coding "Write Python hello world"
```

### Steer Sub-Agent:
```
/subagents steer <agentId> "Focus on performance"
```

### Check Status:
```
/subagents list
/subagents status <agentId>
```

---

## Optimization Tips

### Keep Lightweight:
- Use cheap models (DeepSeek, Aliyun Turbo)
- Limit concurrency: `maxConcurrent: 8`
- Set timeouts: `900s`
- Monitor Zeabur credits

### Monitor Usage:
- Zeabur Dashboard → Usage tab
- Watch compute credits
- Set alerts for high usage

### Scale When Needed:
- Start with Flex Shared (free)
- Upgrade to Pro if heavy use
- Most personal use fits free tier

---

## Testing Checklist

- [ ] OpenAgents deployed
- [ ] Jarvis agent created
- [ ] Sub-agents created (Research, Coding, Admin)
- [ ] Delegation tested (`/subagents spawn`)
- [ ] Response time < 5 seconds
- [ ] Zeabur usage within free tier

---

## Troubleshooting

### Sub-agents not spawning:
- Check `MAX_SPAWN_DEPTH` env variable
- Verify model API keys
- Check Zeabur logs

### High latency:
- Switch to Tokyo/Jakarta region
- Use lighter models
- Reduce maxConcurrent

### Credits running low:
- Reduce model quality
- Lower concurrency
- Set usage alerts

---

## Next Steps

1. Deploy OpenAgents (choose option above)
2. Share deployment URL
3. I'll help configure Jarvis + sub-agents
4. Test delegation
5. Update Kanban (proj-009 → Done!)

---

**Questions? Share what you see in Zeabur templates!**
