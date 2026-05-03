# 🤖 Zyno AI Userbot

Advanced Telegram Userbot with Hinglish AI personality, powered by OpenRouter.

---

## 📁 File Structure

```
zyno-userbot/
├── main.py          ← Entry point, Telethon event handlers
├── ai.py            ← OpenRouter API calls
├── personality.py   ← System prompts & mood detection
├── memory.py        ← Per-user conversation history
├── .env             ← Your credentials (DO NOT SHARE)
├── .env.example     ← Template for .env
└── requirements.txt ← Dependencies
```

---

## ⚙️ Setup

### 1. Clone & Install

```bash
pip install -r requirements.txt
```

### 2. Configure .env

```bash
cp .env.example .env
nano .env   # fill in your credentials
```

Required values:
| Key | Where to get |
|-----|-------------|
| `TELEGRAM_API_ID` | https://my.telegram.org/apps |
| `TELEGRAM_API_HASH` | https://my.telegram.org/apps |
| `OPENROUTER_API_KEY` | https://openrouter.ai/keys |

### 3. Run

```bash
python main.py
```

First run will ask for your phone number + OTP to create the session file.

---

## 🧠 How It Works

| Feature | Detail |
|---------|--------|
| **Modes** | cute / sad / flirty / angry / funny / romantic — auto-detected |
| **Memory** | Last 10 messages per user stored in RAM |
| **Group behaviour** | Only replies when mentioned, trigger word used, or replied to |
| **Trigger words** | `zyno`, `zyna`, `hey zyno` |
| **Anti-spam** | Ignores unrelevant group messages |
| **Typing simulation** | Dynamic delay based on reply length |

---

## 🔒 Security Tips

- Never share your `.env` file or session file (`zyno_session.session`)
- Rotate your API keys if accidentally exposed
- Keep the session file private — it's equivalent to your Telegram login

---

## 🚀 Run 24/7 (VPS)

```bash
# Using screen
screen -S zyno
python main.py
# Ctrl+A then D to detach

# Or using pm2 (node required)
pm2 start main.py --interpreter python3 --name zyno
```

---

## 🛠️ Customization

- **Add trigger words** → Edit `TRIGGER_WORDS` list in `main.py`
- **Change AI model** → Set `AI_MODEL` in `.env`
- **Tune personality** → Edit `personality.py`
- **More memory** → Increase `max_history` in `MemoryManager()`
