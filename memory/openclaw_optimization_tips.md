# OpenClaw Optimization Tips

## Token Usage Optimization
*Recorded: Thursday, February 26, 2026, 2:15 AM UTC (10:15 AM HKT)*

### **Core Strategies:**

#### 1. **Batch Processing**
- Group similar operations in single sessions
- Example: Update all family events at once instead of separate messages
- Batch tool calls when possible (multiple reads/writes in sequence)

#### 2. **Memory Management**
- Use `memory_search` before `memory_get` to find exact snippets
- Read only needed sections with offset/limit parameters
- Archive completed tasks to separate files
- Update MEMORY.md periodically, not after every interaction

#### 3. **Caching & Efficiency**
- Implement local caching for external data (like Reddit scraper)
- Store frequently accessed data locally
- Use fallback data when APIs fail
- Reduce external API calls

#### 4. **Session Optimization**
- Monitor usage with `session_status` regularly
- Use appropriate models for different tasks
- Spawn sub-agents only for complex, isolated tasks
- Keep main session focused on core interactions

#### 5. **Tool Call Optimization**
- Combine multiple file operations when possible
- Use efficient search before reading large files
- Leverage built-in tool features (offset, limit, filters)
- Avoid unnecessary tool calls

### **Practical Applications for Current Setup:**

#### **Family Coordination:**
- Batch all family event updates in single sessions
- Create consolidated family calendar views
- Update HEARTBEAT.md with multiple reminders at once
- Use memory files for event tracking instead of constant tool calls

#### **Skill Development:**
- Test new skills in isolated sessions first
- Cache skill outputs for reuse
- Implement health checks during low-usage periods
- Share skill learnings in community format

#### **Heartbeat Efficiency:**
- Combine multiple checks (email, calendar, notifications)
- Use HEARTBEAT.md checklist approach
- Implement smart sleep-hour management
- Reduce heartbeat frequency during quiet periods

#### **File Management:**
- Use `exec` for batch file operations
- Implement cleanup scripts for old data
- Organize memory files by date and topic
- Use symbolic links for frequently accessed data

### **Monitoring & Measurement:**
1. **Regular Status Checks**: Use `session_status` to track token usage
2. **Cost Analysis**: Review API usage patterns weekly
3. **Efficiency Metrics**: Track tasks completed per token
4. **Optimization Targets**: Identify high-cost operations for improvement

### **Community Best Practices:**
- Learn from r/OpenClawUseCases community
- Share successful optimization strategies
- Contribute back to community knowledge base
- Adapt proven patterns to personal workflow

### **Implementation Priority:**
1. **Immediate**: Batch family event updates
2. **Short-term**: Implement caching for external data
3. **Medium-term**: Optimize heartbeat checks
4. **Long-term**: Develop comprehensive monitoring system

---
*Inspired by: "11 OpenClaw Hacks That Completely Changed How I Work" - r/OpenClawUseCases*
*Related to: API Cost Optimization hack (#6)*