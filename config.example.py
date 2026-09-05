# ═══════════════════════════════════════════════════════
#  ⚙️ 3OUTHBOY UserBot — Configuration
# ═══════════════════════════════════════════════════════
#
#  HOW TO USE:
#  Copy this file to config.py and fill in your values:
#
#      cp config.example.py config.py
#      nano config.py
#
#  ⚠️  config.py contains your secrets — it is in
#      .gitignore and will NEVER be uploaded to GitHub.
#      Never share it with anyone!
# ═══════════════════════════════════════════════════════

# ── Telegram API credentials ────────────────────────────
# Get these from: https://my.telegram.org
#   1. Log in with your phone number
#   2. Go to "API development tools"
#   3. Create an app — then copy API_ID and API_HASH here

API_ID = 12345                    # ← Your numeric App ID
API_HASH = "your_api_hash_here"   # ← Your App Hash string

# ── Control Panel Bot (optional but recommended) ────────
# Create a bot with @BotFather (/newbot) and paste its token here.
# This gives you the beautiful /panel interface in a bot chat.

BOT_TOKEN = "123456789:AA_your_bot_token_here"

# ── Owner ID (REQUIRED) ─────────────────────────────────
# Your numeric Telegram ID — only this user can control the bot.
# Get it from @userinfobot (send any message to it).

OWNER_ID = 123456789

# ── Session (advanced) ──────────────────────────────────
# Leave EMPTY on your server — on first run the bot will ask
# for your phone number and login code (sent inside Telegram),
# then save the session automatically.
# Only fill this if you know how to generate a session string.

STRING_SESSION = ""

# ── AI Assistant (optional) ─────────────────────────────
# Get a free key from: https://openrouter.ai
# (Create account → Keys → Create Key)
# Enables the /ai command.

AI_API_KEY = ""