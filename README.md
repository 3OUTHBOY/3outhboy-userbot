<div align="center">

# ⚡️ 3OUTHBOY UserBot

**🎮 A glass panel for managing, customizing & automating your Telegram account**

An advanced Telegram userbot with **two interfaces**: a beautiful Telegram Bot panel 🤖 + fast dot-commands anywhere 💬

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-orange?logo=telegram&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-GPL--3.0-green)

[English](README.md) | [فارسی](README.fa.md)

</div>

---

<div align="center">

> *"Everything in one place — simple, fast, professional."*

</div>

---

## ✨ Features

| Category | What you get |
|---|---|
| 👤 **Profile & Bio** | Change name, bio, username & profile photo — all via commands |
| ⏰ **Live Clock** | 20 beautiful clock styles in your name + timezone support for any country 🌍 |
| 🛡 **Management** | Block / unblock / mute users in groups |
| 🔒 **Security** | Two-factor authentication (2FA) + AutoSave media |
| 🟢 **Presence** | Always-online mode + fake actions (typing, recording...) |
| ⚡️ **Interactions** | Auto reactions with custom emoji list |
| 🤖 **Smart Secretary** | Custom auto-reply for each person + "greetings only" filter |
| 📢 **Forwarder** | Auto-forward messages between chats + reminder timer |
| 🎛 **Dual Interface** | Glass panel bot with inline buttons + fast `.` commands |
| 🧠 **AI Assistant** | Chat with AI (optional, OpenRouter-ready) |
| 📋 **Utilities** | ping, stats, purge, join/leave, info & more |

---

## 🖼 Preview

<!-- Add your screenshot here:
![Panel](screenshot.png)
-->

---

## 🚀 Installation

### ⭐ Quick Install — Interactive Installer (recommended)

One command, and the installer does everything: installs packages, creates the
virtual environment, **asks you for your credentials interactively** (no manual
file editing!), sets up the 24/7 systemd service and walks you through the
Telegram login.

```bash
git clone https://github.com/3OUTHBOY/3outhboy-userbot.git
cd 3outhboy-userbot
bash install.sh
```

The installer will ask for:

- 🔑 `API_ID` & `API_HASH` — from [my.telegram.org](https://my.telegram.org)
- 🤖 `BOT_TOKEN` — from [@BotFather](https://t.me/BotFather) *(optional, Enter to skip)*
- 👤 `OWNER_ID` — your numeric ID from [@userinfobot](https://t.me/userinfobot)
- 🧠 `AI_API_KEY` — from [openrouter.ai](https://openrouter.ai) *(optional, Enter to skip)*

Then it starts the bot for the first login (phone number + login code) and
enables the 24/7 service automatically. ✨

### 🔧 Manual Install (alternative)

<details>
<summary>Click to expand manual steps</summary>

#### Requirements

- 🐍 Python 3.10+ (recommended: **3.12**)
- 🌐 A VPS or server (Ubuntu 24.04 recommended) — or your own PC
- 🔑 Telegram `API_ID` & `API_HASH` from [my.telegram.org](https://my.telegram.org)

#### Step 1 — Clone & Setup

```bash
apt update && apt install python3 python3-pip python3-venv -y

git clone https://github.com/3OUTHBOY/3outhboy-userbot.git
cd 3outhboy-userbot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 2 — Configure

```bash
cp config.example.py config.py
nano config.py
```

| Variable | Description | Where to get it |
|---|---|---|
| `API_ID` | Telegram app ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram app hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Panel bot token (optional) | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | Your numeric Telegram ID | [@userinfobot](https://t.me/userinfobot) |
| `STRING_SESSION` | Leave empty on server | — |
| `AI_API_KEY` | OpenRouter key (optional) | [openrouter.ai](https://openrouter.ai) |

#### Step 3 — First Run

```bash
python bot.py
```

You'll be asked for your phone number and the login code (sent inside your
Telegram app, not SMS). This happens **only once**.

#### Step 4 — Run 24/7 with systemd 🕐

```bash
nano /etc/systemd/system/userbot.service
```

```ini
[Unit]
Description=3OUTHBOY UserBot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/root/3outhboy-userbot
ExecStart=/root/3outhboy-userbot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now userbot
```

</details>

### 🛠 Service Management

| Action | Command |
|---|---|
| Live logs | `journalctl -u userbot -f` |
| Restart (after code changes) | `systemctl restart userbot` |
| Stop / Start | `systemctl stop userbot` / `systemctl start userbot` |
| Update the bot | `cd 3outhboy-userbot && git pull && systemctl restart userbot` |

---

## 📖 Usage

Once running, the panel is automatically delivered to you:

- **Bot chat:** `/panel` — full control with beautiful inline buttons 🎛
- **Any chat (Saved Messages, etc.):** `.panel` — fast dot-commands

Only the `OWNER_ID` can control the bot — everyone else is ignored 🔒

### Command Reference

<details>
<summary>👤 Profile & Bio</summary>

- `/name First Last` — change your name
- `/bio text` — change your bio
- `/username new_id` — change your @username
- `/setpic` (reply to a photo) — set profile photo

</details>

<details>
<summary>⏰ Clock & Fonts</summary>

- `/clock on / off` — live clock next to your name
- `/clockstyle` — 20 beautiful styles (emoji clock, digital fonts & more)
- `/clocktz Iran` — automatic timezone for any country
- `.font bold text` — fancy text styles (bold, italic, mono, double)

</details>

<details>
<summary>🤖 Secretary (Auto-Reply)</summary>

- `/setreply text` (reply to a message) — custom reply for that specific person
- `/setreply @username | text` — same, by username
- `/unsetreply` — remove a custom reply
- `/userreplies` — list all custom replies
- `/greetonly on / off` — reply **only** to greetings ("hi", "سلام"...)
- `/reply on / off / text` — general auto-reply
- `/addreply keyword | answer` — keyword-based replies

</details>

<details>
<summary>🛡 Management & Security</summary>

- `/block @user` / `/unblock @user` — block users
- `.mute 10m` / `.unmute` (reply, supergroups) — silence users
- `/2fa password` / `/2fa off` — two-factor authentication
- `/autosave` — auto-save incoming media

</details>

<details>
<summary>⚡️ Presence & Reactions</summary>

- `/online` — always-online mode
- `.typing 30` — fake "typing..." action
- `/react` — auto-reactions toggle
- `/reactlist ❤️ 🔥 👑` — set your reaction emojis

</details>

<details>
<summary>📢 Forwarder, Timer & Tools</summary>

- `/fwd add @source @target` — connect two chats
- `/timer 30s text` — reminder timer (s/m/h/d)
- `/ping` — latency check
- `/stats` — account statistics
- `/info @user` — user info
- `.purge` (reply) — bulk delete messages
- `.join @channel` / `.leave` — join/leave chats

</details>

<details>
<summary>🧠 AI Assistant</summary>

- `/ai your question` — chat with AI (requires `AI_API_KEY`)

</details>

---

## 🖥 Windows Users

Works on Windows too! Just make sure you have **Python 3.12** (newer versions may break Pyrogram):

```
pip install pyrogram aiohttp
python bot.py
```

> 💡 On Windows, `tgcrypto` requires Visual C++ Build Tools — it's optional, everything works without it.

---

## ⚠️ Warnings

- Using a userbot may conflict with Telegram's Terms of Service — **you are responsible for your own account**
- Use automated features (reactions, forwarder) responsibly to avoid getting limited
- Your `.session` files and `config.py` are **as sensitive as your password** — never share them!
- Don't run the same account on two machines at once (duplicate replies / FloodWait)

---

## 🧹 Uninstall — Complete Removal

Want to remove 3OUTHBOY UserBot from your server completely? Run these commands **in order**:

```bash
# 1. Stop and disable the 24/7 service
systemctl stop userbot
systemctl disable userbot

# 2. Delete the service file
rm -f /etc/systemd/system/userbot.service
systemctl daemon-reload

# 3. Delete the bot (code, venv, sessions, config, database)
cd ~
rm -rf 3outhboy-userbot
```

⚠️ **Step 3 removes everything** — including your login session
(`my_account.session`) and all your bot settings (`userbot_db.json`).

### 🔐 Recommended extra security steps (outside the server):

| Step | How |
|---|---|
| 🤖 **Revoke the panel bot token** | Message [@BotFather](https://t.me/BotFather) → `/revoke` (or `/mybots` → your bot → API Token → Revoke) |
| 📱 **Terminate the session inside Telegram** | Telegram Settings → Devices → find this server's session → **Terminate Session** |
| 🔑 **Regenerate API credentials** (optional, extra safe) | [my.telegram.org](https://my.telegram.org) — revoke and create a new app |

> 💡 Terminating the session from Telegram Settings is **instant and works even
> if you already deleted the files** — when in doubt, do this.

After these steps, no trace of the bot remains on your server, and all access
to your account is revoked. 🌸

---

## 🤝 Contributing

Found a bug? Have a cool idea? Feel free to open an [Issue](https://github.com/3OUTHBOY/3outhboy-userbot/issues) or submit a Pull Request! 💜

---

## 📜 License

<div align="center">

**3OUTHBOY UserBot** is licensed under the
**[GNU General Public License v3.0](LICENSE)** 🍃

> *"Free software is a matter of liberty, not price."* — RMS

`🄯 3OUTHBOY — Copyleft, all rights reversed.`

Use it. Break it. Improve it. Share it back. 💜

</div>

---

<div align="center">

**Made with 💜 for the Telegram community**

⭐ Star this repo if you like it!

</div>
