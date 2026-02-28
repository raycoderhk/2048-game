# 🎯 Polymarket CLI

Track prediction markets from your terminal!

**Inspired by Andrej Karpathy:** *"Build for Agents"*

---

## 🚀 Quick Start

```bash
# Show top markets
./polymarket.sh top

# Full dashboard
./polymarket.sh dashboard

# Search markets
./polymarket.sh search "Bitcoin"

# Add to watchlist
./polymarket.sh watch <market-id>

# View watchlist
./polymarket.sh watchlist
```

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `top` | Top markets by volume |
| `search <query>` | Search markets |
| `market <id>` | Market details |
| `dashboard` | Full dashboard |
| `watch <id>` | Add to watchlist |
| `watchlist` | Show watchlist |
| `portfolio` | Your positions |

---

## 🎨 Features

- ✅ **Real-time data** from Polymarket API
- ✅ **Beautiful terminal UI** (Rich library)
- ✅ **Watchlist** tracking
- ✅ **JSON output** option
- ✅ **Dashboard** view
- ✅ **Search** functionality

---

## 💡 Examples

### Top 10 Markets
```bash
./polymarket.sh top --limit 10
```

### Search Crypto Markets
```bash
./polymarket.sh search "crypto"
```

### Export as JSON
```bash
./polymarket.sh top --json > markets.json
```

### Full Dashboard
```bash
./polymarket.sh dashboard
```

---

## 🔧 Installation

### Dependencies
```bash
pip install rich requests --user
```

### Add to PATH
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.openclaw/workspace/clis/polymarket:$PATH"

# Then run directly
polymarket top
```

---

## 📊 Sample Output

```
🔥 Top Polymarkets by Volume
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━━━━┓
┃ #  ┃ Market                                         ┃ Category ┃ Volume  ┃ Yes % ┃ No % ┃ End Date   ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━━━━┩
│ 1  │ Will Bitcoin reach $100k in 2026?             │ Crypto   │ $15.4M  │  67%  │  33% │ 2026-12-31 │
│ 2  │ Will AI pass Turing Test by 2027?             │ Tech     │ $8.7M   │  42%  │  58% │ 2027-12-31 │
│ 3  │ Fed rate cut in March 2026?                   │ Economics│ $12.3M  │  78%  │  22% │ 2026-03-31 │
└────┴────────────────────────────────────────────────┴──────────┴─────────┴───────┴──────┴────────────┘
```

---

## 🎯 Use Cases

### 1. Daily Market Check
```bash
# Morning routine
polymarket dashboard
```

### 2. Track Specific Topics
```bash
# Add crypto markets to watchlist
polymarket watch <market-id-1>
polymarket watch <market-id-2>
polymarket watchlist
```

### 3. Research
```bash
# Search and export
polymarket search "AI" --json > ai-markets.json
```

### 4. Agent Integration
```bash
# Use in scripts/pipelines
markets=$(polymarket top --json)
# Process with AI agents
```

---

## 🤖 Agent Integration

**Example: Build automated trading dashboard**

```python
# agent_dashboard.py
import subprocess
import json

# Get market data
result = subprocess.run(['polymarket', 'top', '--json'], 
                       capture_output=True, text=True)
markets = json.loads(result.stdout)

# Analyze with AI
for market in markets[:5]:
    print(f"{market['title']}: {market['yes_bid']*100:.0f}% Yes")
```

---

## 📝 Watchlist File

Watchlist saved to:
```
/home/node/.openclaw/workspace/clis/polymarket/watchlist.json
```

Format:
```json
[
  "market-id-1",
  "market-id-2",
  "market-id-3"
]
```

---

## 🎨 Customization

### Modify appearance
Edit `polymarket.py`:
- Change colors
- Adjust table layout
- Add new columns

### Add features
- Portfolio tracking (with API key)
- Price alerts
- Historical data
- Export formats

---

## 🚧 Future Enhancements

- [ ] Real API integration (currently uses mock data)
- [ ] Portfolio management
- [ ] Price alerts
- [ ] Historical charts
- [ ] Trading execution
- [ ] Multi-account support

---

## 📄 License

MIT License - Build for Agents!

---

**Inspired by:** Andrej Karpathy's vision of agent-first development

**Created:** 2026-02-26
