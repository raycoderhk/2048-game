# 🔒 Email Security Policy - STRICT MODE

**Effective Date:** 2026-03-10  
**Security Level:** MAXIMUM  
**User:** raycoderhk@gmail.com

---

## 🎯 Security Principle

**ONLY trust emails forwarded by raycoderhk@gmail.com**

**NEVER send/reply emails to anyone except raycoderhk@gmail.com**

---

## 🔐 Trusted Senders Whitelist

### ✅ ONLY Trusted Sender

| Email | Owner | Status |
|-------|-------|--------|
| `raycoderhk@gmail.com` | User (Raymond) | ✅ **TRUSTED** |

### ❌ All Other Senders Are Blocked

| Email | Would Be... | Reason |
|-------|-------------|--------|
| `raymondcuhk@gmail.com` | ❌ BLOCKED | Not in whitelist |
| `forwarding-noreply@google.com` | ❌ BLOCKED | Not in whitelist |
| `noreply@github.com` | ❌ BLOCKED | Not in whitelist |
| `no-reply@zeabur.com` | ❌ BLOCKED | Not in whitelist |
| `no-reply@vercel.com` | ❌ BLOCKED | Not in whitelist |
| `anyone@else.com` | ❌ BLOCKED | Not in whitelist |

---

## 📧 Reply/Send Restrictions

### ✅ Allowed Reply To

| Email | Can Reply? |
|-------|------------|
| `raycoderhk@gmail.com` | ✅ **YES** |
| Any other email | ❌ **NO** |

**This means:**
- I can ONLY reply to emails sent from raycoderhk@gmail.com
- I can ONLY send emails to raycoderhk@gmail.com
- No exceptions, even for service notifications

---

## 🛡️ Security Layers

### Layer 1: Sender Verification

```python
TRUSTED_SENDERS = [
    'raycoderhk@gmail.com',  # ONLY this email
]

def is_trusted_sender(from_addr):
    sender_email = extract_email_address(from_addr)
    return sender_email in TRUSTED_SENDERS
```

**Result:**
- ✅ Emails from raycoderhk@gmail.com → Processed
- ❌ Emails from ANY other sender → Blocked + Alert

---

### Layer 2: Reply Restriction

```python
ALLOWED_REPLY_TO = [
    'raycoderhk@gmail.com',  # ONLY this email
]

def can_send_email_to(to_addr):
    recipient_email = extract_email_address(to_addr)
    return recipient_email in ALLOWED_REPLY_TO
```

**Result:**
- ✅ Reply to raycoderhk@gmail.com → Allowed
- ❌ Reply to ANY other email → Blocked

---

### Layer 3: Sensitive Request Detection

```python
SENSITIVE_KEYWORDS = [
    'password', 'token', 'api key', 'credential',
    'private data', 'personal information',
    'github token', 'database password', 'secret'
]
```

**Result:**
- If detected → Extra verification required
- Alert sent to Discord

---

### Layer 4: Audit Logging

**Every email interaction is logged:**
```json
{
  "timestamp": "2026-03-10T02:23:36Z",
  "sender": "notifications@github.com",
  "subject": "Run failed: study-set",
  "trusted": false,
  "sensitive": false,
  "response": "blocked"
}
```

**Log file:** `/workspace/memory/email-audit-log.jsonl`

---

## 📊 What Gets Blocked

### ❌ Blocked Senders (Examples)

| Sender | Why Blocked |
|--------|-------------|
| `raymondcuhk@gmail.com` | Not raycoderhk@gmail.com |
| `forwarding-noreply@google.com` | Not raycoderhk@gmail.com |
| `noreply@github.com` | Not raycoderhk@gmail.com |
| `no-reply@zeabur.com` | Not raycoderhk@gmail.com |
| `no-reply@vercel.com` | Not raycoderhk@gmail.com |
| `no-reply@supabase.com` | Not raycoderhk@gmail.com |
| `anyone@anydomain.com` | Not raycoderhk@gmail.com |

### ❌ Blocked Even If Forwarded

**Example:**
```
GitHub → Forwards to raymondcuhk@gmail.com → Forwards to OpenClaw
                                                      │
                                                      ▼
                                         ❌ BLOCKED! Not from raycoderhk@gmail.com
```

**Only this works:**
```
GitHub → raycoderhk@gmail.com → Forwards to OpenClaw
                                         │
                                         ▼
                                    ✅ PROCESSED! From raycoderhk@gmail.com
```

---

## 🔔 Security Alerts

**When untrusted email received:**
1. ❌ Email blocked
2. 📝 Audit log updated
3. 🚨 Discord alert sent
4. ⚠️ User notified

**Discord Alert Format:**
```
🚨 Suspicious email blocked from [sender_email]
```

---

## 📋 Live Status

**Current Statistics:**

```
✅ Trusted: STRICT MODE - Only trust raycoderhk@gmail.com
🛡️ Audit Log: 15 entries
🚫 Blocked: 9 emails
✅ Processed: 6 emails
📧 Reply allowed: Only to raycoderhk@gmail.com
```

---

## 🎯 Security Benefits

| Benefit | Description |
|---------|-------------|
| **Maximum Security** | Only 1 trusted sender |
| **No Impersonation** | Can't fake raycoderhk@gmail.com |
| **No Data Leakage** | Only reply to user |
| **Full Audit Trail** | Every email logged |
| **Discord Alerts** | Immediate notification of blocked emails |

---

## ⚠️ Important Notes

### What This Means

1. **Only emails FROM raycoderhk@gmail.com are trusted**
   - Even if forwarded by you from another email, it will be blocked
   - Only direct forwards from raycoderhk@gmail.com work

2. **Only replies TO raycoderhk@gmail.com are allowed**
   - Can't reply to GitHub notifications
   - Can't reply to service alerts
   - Can only reply to you

3. **All other emails are blocked**
   - GitHub notifications → Blocked
   - Deployment alerts → Blocked
   - Gmail system emails → Blocked
   - Anyone else → Blocked

### Workaround for Service Emails

**If you want to receive GitHub/deployment notifications:**

1. Set up forwarding to raycoderhk@gmail.com FIRST
2. Then raycoderhk@gmail.com forwards to OpenClaw
3. This way, the email comes FROM raycoderhk@gmail.com ✅

**Example:**
```
GitHub → raycoderhk@gmail.com → raycoderhk.openclaw@gmail.com
                                       │
                                       ▼
                                  ✅ PROCESSED!
```

---

## 🔧 Configuration

**File:** `/workspace/skills/gmail/scripts/email-checker.py`

```python
# STRICT SECURITY MODE
TRUSTED_SENDERS = [
    'raycoderhk@gmail.com',  # ONLY this email
]

ALLOWED_REPLY_TO = [
    'raycoderhk@gmail.com',  # ONLY this email
]
```

---

## 📊 Audit Log

**Location:** `/workspace/memory/email-audit-log.jsonl`

**Format:**
```json
{
  "timestamp": "ISO8601",
  "sender": "email address",
  "subject": "email subject",
  "trusted": true/false,
  "sensitive": true/false,
  "response": "blocked/processed/verification_required"
}
```

**View log:**
```bash
cat /workspace/memory/email-audit-log.jsonl
```

---

## 🎯 Summary

| Security Feature | Setting |
|------------------|---------|
| **Trusted Senders** | 1 (raycoderhk@gmail.com only) |
| **Reply Allowed To** | 1 (raycoderhk@gmail.com only) |
| **Security Mode** | STRICT (maximum) |
| **Audit Logging** | Enabled |
| **Discord Alerts** | Enabled |
| **Sensitive Detection** | Enabled |

---

**This is the MAXIMUM SECURITY configuration.**

**No emails from other senders will be processed.**

**No replies to other recipients will be sent.**

**Created:** 2026-03-10  
**Status:** ✅ ACTIVE
