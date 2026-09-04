# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
#   ⚡️ پنل سلف 3OUTHBOY ⚡️
#   یوزربات مدیریت اکانت تلگرام + پنل ربات تلگرامی
#   Ubuntu 24.04 | Python 3.12
# ═══════════════════════════════════════════════════════════════

# ── سازگاری با پایتون 3.13+ ──
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import json, os, random, re, time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import aiohttp
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from pyrogram.raw import functions, types as raw
from pyrogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
)

# ═══════════════════════════════════════════════
#  ⚙️ تنظیمات — از فایل config.py خونده می‌شه
#  (نمونه: config.example.py رو به config.py کپی کن)
# ═══════════════════════════════════════════════
try:
    from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, STRING_SESSION, AI_API_KEY
except ImportError:
    API_ID = 0
    API_HASH = ""
    BOT_TOKEN = ""
    OWNER_ID = 0
    STRING_SESSION = ""
    AI_API_KEY = ""

PREFIX = "."
AI_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

DOWNLOAD_DIR = "downloads"
DB_FILE = "userbot_db.json"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ═══════════════════════════════════════════════
#  💾 دیتابیس
# ═══════════════════════════════════════════════
DEFAULT_DB = {
    "clock": False, "online": False,
    "autoreact": False, "react_emojis": ["👍", "❤️", "🔥", "👏"],
    "autoreply": False,
    "autoreply_text": "سلام! الان در دسترس نیستم، به‌زودی جواب می‌دم 🙂",
    "keyword_replies": {},
    "forwarder": False, "fwd_pairs": [],
    "autosave": False, "pw": "", "orig_last": "",
    "clock_style": "plain", "clock_tz": "",
    "userreply": False, "user_replies": {}, "userreply_cd": 60,
    "greet_only": True,
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
            for k, v in DEFAULT_DB.items():
                d.setdefault(k, v)
            return d
        except Exception:
            pass
    return DEFAULT_DB.copy()

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

db = load_db()

# ═══════════════════════════════════════════════
#  📡 کلاینت‌ها (یوزربات + ربات پنل)
# ═══════════════════════════════════════════════
app = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION if STRING_SESSION else None,
)
me = None

bot = Client(
    "control_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN if BOT_TOKEN else None,
)

# ═══════════════════════════════════════════════
#  ✍️ فونت‌ها
# ═══════════════════════════════════════════════
_F = {
    "bold": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"),
    "italic": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"),
    "mono": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"),
    "double": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"),
}

# ═══════════════════════════════════════════════
#  ⏰ استایل‌های ساعت (۲۰ استایل)
# ═══════════════════════════════════════════════
DIG_BOLD   = str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
DIG_MONO   = str.maketrans("0123456789", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿")
DIG_DOUBLE = str.maketrans("0123456789", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡")
DIG_CIRCLE = str.maketrans("0123456789", "⓪①②③④⑤⑥⑦⑧⑨")

_HOUR_EMOJI = ["🕛","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚"]
_HALF_EMOJI = ["🕧","🕜","🕝","🕞","🕟","🕠","🕡","🕢","🕣","🕤","🕥","🕦"]
CLOCK_STYLE_NAMES = ["plain","bold","mono","double","circle","face","facebold",
                     "watch","watchmono","alarm","glass","flower","brackets",
                     "corner","stars","line","dots","night","moon","heart"]

def _face(h, m):
    return _HALF_EMOJI[h % 12] if m >= 30 else _HOUR_EMOJI[h % 12]

def fmt_clock(style, now):
    t, h, m = now.strftime("%H:%M"), now.hour, now.minute
    b  = t.translate(DIG_BOLD)
    mo = t.translate(DIG_MONO)
    d  = t.translate(DIG_DOUBLE)
    c  = t.translate(DIG_CIRCLE)
    S = {
        "plain": t, "bold": b, "mono": mo, "double": d, "circle": c,
        "face":      f"{_face(h,m)} {t}",
        "facebold":  f"{_face(h,m)} {b}",
        "watch":     f"⌚ {t}",
        "watchmono": f"⌚{mo}",
        "alarm":     f"⏰{t}",
        "glass":     f"⏳ {t}",
        "flower":    f"✿ {t} ✿",
        "brackets":  f"「{t}」",
        "corner":    f"『{t}』",
        "stars":     f"✦ {t} ✦",
        "line":      f"┆{t}┆",
        "dots":      f"• {t} •",
        "night":     ("🌙" if (h >= 19 or h < 6) else "☀️") + f" {t}",
        "moon":      f"🌙 {mo}",
        "heart":     f"♥ {t} ♥",
    }
    return S.get(style, t)

# ═══════════════════════════════════════════════
#  🌍 منطقه زمانی
# ═══════════════════════════════════════════════
TZ_ALIASES = {
    "ایران": "Asia/Tehran", "iran": "Asia/Tehran", "tehran": "Asia/Tehran",
    "دبی": "Asia/Dubai", "امارات": "Asia/Dubai", "dubai": "Asia/Dubai",
    "ترکیه": "Europe/Istanbul", "istanbul": "Europe/Istanbul",
    "آلمان": "Europe/Berlin", "berlin": "Europe/Berlin",
    "لندن": "Europe/London", "انگلیس": "Europe/London", "london": "Europe/London",
    "نیویورک": "America/New_York", "newyork": "America/New_York",
    "لاس": "America/Los_Angeles", "california": "America/Los_Angeles",
    "مسکو": "Europe/Moscow", "روسیه": "Europe/Moscow",
    "استرالیا": "Australia/Sydney", "sydney": "Australia/Sydney",
    "ژاپن": "Asia/Tokyo", "tokyo": "Asia/Tokyo",
    "هند": "Asia/Kolkata", "india": "Asia/Kolkata",
    "قطر": "Asia/Qatar", "doha": "Asia/Qatar",
    "عراق": "Asia/Baghdad", "بغداد": "Asia/Baghdad",
    "افغانستان": "Asia/Kabul", "kabul": "Asia/Kabul",
    "پاکستان": "Asia/Karachi", "karachi": "Asia/Karachi",
    "کانادا": "America/Toronto", "toronto": "America/Toronto",
    "فرانسه": "Europe/Paris", "paris": "Europe/Paris",
}

def get_now():
    tz = db.get("clock_tz")
    if tz:
        try:
            return datetime.now(ZoneInfo(tz))
        except Exception:
            pass
    return datetime.now()

# ═══════════════════════════════════════════════
#  🚪 فیلتر سلام (منشی فقط به سلام جواب بده)
# ═══════════════════════════════════════════════
GREET_SUB = ("سلام", "درود", "hello", "سلم")          # هرجای پیام باشه شناسایی می‌شه
GREET_WORD = ("hi", "hey", "هی", "slm", "salam")      # فقط اگه کلمه کامل باشه

def is_greeting(text):
    if not text:
        return False
    t = text.lower().strip()
    if any(g in t for g in GREET_SUB):
        return True
    return any(re.search(rf"\b{re.escape(g)}\b", t) for g in GREET_WORD)

# ═══════════════════════════════════════════════
#  🎛 پنل
# ═══════════════════════════════════════════════
PANEL_TEXT = (
    "═══════════✧═══════════\n"
    "  「 ⚡️ **پنل سلف 3OUTHBOY** ⚡️ 」\n"
    "═══════════✧═══════════\n\n"
    "🌙 **با آغوش باز خوش اومدی!** ✨\n"
    "از این لحظه، فرماندهیِ کامل اکانتت دست خودته 🤝\n"
    "هر چی بخوای، فقط یه دستور فاصله داری 🎯\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "💠 **راهنمای دستورات**\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "👤 **پروفایل و بیو**\n"
    "» `.name اسم` — تغییر اسم\n"
    "» `.bio متن` — تغییر بیو\n"
    "» `.username آیدی` — تغییر آیدی\n"
    "» `.setpic` — تغییر عکس (ریپلای به عکس)\n\n"
    "⏰ **ساعت و فونت**\n"
    "» `.clock on` — ساعت زنده کنار اسم\n"
    "» `.clockstyle` — ۲۰ استایل خوشگل 🎨\n"
    "» `.clocktz ایران` — ساعت هر کشور 🌍\n"
    "» `.font bold متن` — متن با فونت فان\n\n"
    "🛡 **بلاک و سکوت**\n"
    "» `.block` / `.unblock` — بلاک (ریپلای)\n"
    "» `.mute 10m` / `.unmute` — سکوت در گروه\n\n"
    "🔒 **امنیت و AutoSave**\n"
    "» `.2fa رمز` — قفل دو مرحله‌ای\n"
    "» `.autosave` — ذخیره خودکار مدیا\n\n"
    "🟢 **آنلاین و اکشن**\n"
    "» `.online` — همیشه آنلاین\n"
    "» `.typing 30` — در حال نوشتنِ فیک ✍️\n\n"
    "⚡️ **ریاکشن خودکار**\n"
    "» `.react` — روشن/خاموش\n"
    "» `.reactlist ❤️ 🔥 👑` — ایموجی‌های دلخواه\n\n"
    "🤖 **منشی و پاسخ خودکار**\n"
    "» `.setreply متن` — جواب اختصاصی هر نفر (ریپلای)\n"
    "» `.unsetreply` — حذف جواب\n"
    "» `.greetonly` — فقط به سلام جواب بده 🚪\n"
    "» `.userreplies` — لیست منشی‌ها\n\n"
    "📢 **تبچی و تایمر**\n"
    "» `.fwd add @مبدا @مقصد` — اتصال دو چت\n"
    "» `.timer 30s متن` — یادآور زمان‌دار ⏱\n\n"
    "📋 **ابزارهای کاربردی**\n"
    "» `.ping` `.id` `.info` `.stats`\n"
    "» `.purge` — پاکسازی پیام‌ها (ریپلای)\n"
    "» `.join @کانال` / `.leave` — عضویت/خروج\n\n"
    "🧠 **هوش مصنوعی**\n"
    "» `.ai سوالت` — گفتگو با AI\n\n"
    "💡 برای راهنمای هر بخش، دکمه‌های زیر رو بزن 👇\n\n"
    "═══════════✿═══════════\n"
    "  「 💖 **سپاس از حضورت** 💖 」\n"
    "═══════════✿═══════════\n\n"
    "🌱 ممنون که این پنل رو برای مدیریت اکانتت انتخاب کردی\n"
    "🚀 ما همیشه دنبال بهترین تجربه برات هستیم\n"
    "🌟 اگه خوشت اومد، به رفاقاتت هم معرفی کن\n"
    "🌸 روزت پر از لبخند و لحظه‌های قشنگ باشه 🌸"
)

HELP = {
    "profile": "👤 **پروفایل و بیو**\n\n`.name اسم فامیلی`\n`.bio متن`\n`.username آیدی`\n`.setpic` (ریپلای به عکس)",
    "clock": "⏰ **ساعت و فونت**\n\n`.clock on | off`\n`.clockstyle` → ۲۰ استایل\n`.clocktz ایران` → ساعت هر کشور\n`.font bold متن` → bold, italic, mono, double",
    "block": "🛡 **بلاک و سکوت**\n\n`.block` / `.unblock` (ریپلای یا @کاربر)\n`.mute 10m` / `.unmute` (ریپلای، در سوپرگروه)",
    "security": "🔒 **امنیت و AutoSave**\n\n`.2fa رمز` / `.2fa off`\n`.autosave` → ذخیره خودکار مدیای پی‌وی",
    "online": "🟢 **آنلاین و اکشن**\n\n`.online on | off`\n`.typing 30`",
    "react": "⚡️ **ریاکشن خودکار**\n\n`.react on | off`\n`.reactlist ❤️ 🔥 👑`",
    "reply": "🤖 **منشی و پاسخ خودکار**\n\n`.setreply متن` (ریپلای) → جواب اختصاصی\n`.unsetreply` → حذف\n`.userreplies` → لیست\n`.greetonly on | off` → فقط سلام\n`.reply on | off | متن` → جواب عمومی\n`.addreply کلمه | جواب` / `.delreply کلمه`",
    "fwd": "📢 **تبچی و تایمر**\n\n`.fwd on | off | add | list | clear`\n`.fwd add @مبدا @مقصد` (با `.` چت فعلی)\n`.timer 30s متن` — مدت‌ها: s, m, h, d",
    "tools": "📋 **ابزارها**\n\n`.ping` `.id` `.info` `.stats`\n`.purge` (ریپلای) `.del` `.join @کانال` `.leave`",
    "ai": "🧠 **هوش مصنوعی**\n\n`.ai سوالت`\nبرای فعال‌شدن، `AI_API_KEY` رو در اول فایل بذار.",
}

def panel_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 پروفایل و بیو", "help:profile"),
         InlineKeyboardButton("⏰ ساعت و فونت", "help:clock")],
        [InlineKeyboardButton("🛡 بلاک و سکوت", "help:block"),
         InlineKeyboardButton("🔒 امنیت و AutoSave", "help:security")],
        [InlineKeyboardButton("🟢 آنلاین", "help:online"),
         InlineKeyboardButton("⚡️ ریاکشن", "help:react")],
        [InlineKeyboardButton("🤖 منشی", "help:reply"),
         InlineKeyboardButton("📢 تبچی و تایمر", "help:fwd")],
        [InlineKeyboardButton("📋 ابزارها", "help:tools"),
         InlineKeyboardButton("🧠 هوش مصنوعی", "help:ai")],
        [InlineKeyboardButton("📊 وضعیت قابلیت‌ها", "status"),
         InlineKeyboardButton("✖ بستن", "close")],
    ])

def status_text():
    s = lambda k: "✅" if db.get(k) else "❌"
    return ("📊 **وضعیت قابلیت‌ها**\n\n"
            f"⏰ ساعت در نام: {s('clock')}\n"
            f"🟢 همیشه آنلاین: {s('online')}\n"
            f"⚡️ ریاکشن خودکار: {s('autoreact')}\n"
            f"🤖 منشی اختصاصی: {s('userreply')}\n"
            f"🚪 فیلتر سلام: {s('greet_only')}\n"
            f"📢 تبچی: {s('forwarder')}\n"
            f"📥 AutoSave: {s('autosave')}\n\n"
            "برای روشن/خاموش‌کردن، دکمه‌ش رو بزن.")

def status_kb():
    items = [("clock", "⏰ ساعت"), ("online", "🟢 آنلاین"), ("autoreact", "⚡️ ریاکشن"),
             ("userreply", "🤖 منشی"), ("greet_only", "🚪 فیلتر سلام"),
             ("forwarder", "📢 تبچی"), ("autosave", "📥 AutoSave")]
    rows = [[InlineKeyboardButton(f"{lbl} {'✅' if db.get(k) else '❌'}", f"toggle:{k}")]
            for k, lbl in items]
    rows.append([InlineKeyboardButton("🔙 بازگشت", "back")])
    return InlineKeyboardMarkup(rows)

# ═══════════════════════════════════════════════
#  🧰 ابزارهای کمکی
# ═══════════════════════════════════════════════
def parse_time(s: str) -> int:
    s = s.strip().lower()
    if s and s[-1] in "smhd":
        return int(s[:-1]) * {"s": 1, "m": 60, "h": 3600, "d": 86400}[s[-1]]
    return int(s)

async def toggle_key(key, state=None):
    if state is None:
        state = not db.get(key)
    db[key] = state
    save_db()
    return state

async def toggle_clock(state=None):
    if state is None:
        state = not db.get("clock")
    if state and not db.get("clock"):
        db["orig_last"] = (me.last_name if me else "") or ""
    db["clock"] = state
    save_db()
    if not state:
        try:
            await app.update_profile(last_name=db.get("orig_last", "") or "")
        except Exception:
            pass
    return state

async def react_to(message: Message, emoji: str):
    try:
        await app.invoke(functions.messages.SendReaction(
            peer=await app.resolve_peer(message.chat.id),
            msg_id=message.id,
            reaction=[raw.ReactionEmoji(emoticon=emoji)],
        ))
    except Exception:
        pass

async def get_target_user(m: Message):
    if m.reply_to_message:
        return m.reply_to_message.from_user
    if len(m.command) > 1:
        try:
            return await app.get_users(m.command[1])
        except Exception:
            pass
    return None

async def resolve_target(t: str, current_id: int) -> int:
    if t == ".":
        return current_id
    if t.lstrip("-").isdigit():
        return int(t)
    chat = await app.get_chat(t)
    return chat.id

async def ask_ai(prompt: str) -> str:
    if not AI_API_KEY:
        return "❌ کلید AI تنظیم نشده. `AI_API_KEY` رو در اول فایل بذار."
    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": "تو یک دستیار مفید هستی. کوتاه و به فارسی جواب بده."},
            {"role": "user", "content": prompt},
        ],
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(AI_URL, json=payload,
                              headers={"Authorization": f"Bearer {AI_API_KEY}"},
                              timeout=aiohttp.ClientTimeout(total=60)) as r:
                data = await r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ خطا در ارتباط با AI: {e}"

# ═══════════════════════════════════════════════
#  🔄 تسک‌های پس‌زمینه
# ═══════════════════════════════════════════════
async def clock_loop():
    while True:
        if db.get("clock"):
            try:
                await app.update_profile(
                    last_name=fmt_clock(db.get("clock_style", "plain"), get_now()))
            except FloodWait as e:
                await asyncio.sleep(e.value + 5)
            except Exception:
                pass
        await asyncio.sleep(60)

async def online_loop():
    while True:
        if db.get("online"):
            try:
                await app.invoke(functions.account.UpdateStatus(offline=False))
            except Exception:
                pass
        await asyncio.sleep(55)

# ═══════════════════════════════════════════════
#  📝 دستورات یوزربات (با . در سیو مسیج)
# ═══════════════════════════════════════════════

@app.on_message(filters.me & filters.command(["panel", "help", "menu"], prefixes=PREFIX))
async def panel_cmd(c, m):
    await m.edit(PANEL_TEXT, reply_markup=panel_kb())

# ── پروفایل و بیو ──
@app.on_message(filters.me & filters.command("name", prefixes=PREFIX))
async def name_cmd(c, m):
    parts = m.text.split(maxsplit=2)
    first = parts[1] if len(parts) > 1 else me.first_name
    last = parts[2] if len(parts) > 2 else ""
    await c.update_profile(first_name=first, last_name=last)
    await m.edit(f"✅ اسم تغییر کرد به: **{first} {last}**".strip())

@app.on_message(filters.me & filters.command("bio", prefixes=PREFIX))
async def bio_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.bio متن بیو`")
    await c.update_profile(bio=parts[1][:70])
    await m.edit("✅ بیو آپدیت شد")

@app.on_message(filters.me & filters.command("username", prefixes=PREFIX))
async def username_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.username آیدی`")
    try:
        await c.set_username(parts[1].strip("@"))
        await m.edit("✅ آیدی تغییر کرد")
    except Exception as e:
        await m.edit(f"❌ {e}")

@app.on_message(filters.me & filters.command("setpic", prefixes=PREFIX))
async def setpic_cmd(c, m):
    if not (m.reply_to_message and m.reply_to_message.photo):
        return await m.edit("💡 به یک عکس ریپلای کن")
    f = await m.reply_to_message.download()
    await c.set_profile_photo(photo=f)
    os.remove(f)
    await m.edit("✅ عکس پروفایل تغییر کرد")

# ── ساعت و فونت ──
@app.on_message(filters.me & filters.command("clock", prefixes=PREFIX))
async def clock_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else None
    state = None if arg not in ("on", "off") else arg == "on"
    val = await toggle_clock(state)
    await m.edit(f"⏰ ساعت در نام: {'✅ روشن' if val else '❌ خاموش'}")

@app.on_message(filters.me & filters.command("clockstyle", prefixes=PREFIX))
async def clockstyle_cmd(c, m):
    now = get_now()
    args = m.text.split()
    if len(args) > 1:
        pick = args[1]
        if pick.isdigit():
            i = int(pick) - 1
            if 0 <= i < len(CLOCK_STYLE_NAMES):
                pick = CLOCK_STYLE_NAMES[i]
            else:
                return await m.edit("❌ شماره بین 1 تا 20 باشه")
        if pick not in CLOCK_STYLE_NAMES:
            return await m.edit("❌ این استایل وجود نداره. `.clockstyle` رو بزن تا لیست ببینی.")
        db["clock_style"] = pick
        save_db()
        if db.get("clock"):
            try:
                await app.update_profile(last_name=fmt_clock(pick, get_now()))
            except Exception:
                pass
        return await m.edit(f"✅ استایل ساعت: **{pick}**\n"
                           f"پیش‌نمایش: {fmt_clock(pick, get_now())}")
    lines = ["🎨 **استایل‌های ساعت**\n`.clockstyle شماره` برای انتخاب\n"]
    for i, name in enumerate(CLOCK_STYLE_NAMES, 1):
        lines.append(f"`{i:>2}.` {fmt_clock(name, now)}")
    cur = db.get("clock_style", "plain")
    lines.append(f"\n📌 فعلی: **{cur}** → {fmt_clock(cur, now)}")
    await m.edit("\n".join(lines))

@app.on_message(filters.me & filters.command("clocktz", prefixes=PREFIX))
async def clocktz_cmd(c, m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        cur = db.get("clock_tz", "")
        lines = ["🌍 **منطقه زمانی ساعت**\n\n",
                 f"📌 فعلی: `{cur or 'ساعت سیستم سرور'}`\n",
                 f"🕐 الان: {fmt_clock(db.get('clock_style', 'plain'), get_now())}\n\n",
                 "⚙️ تنظیم: `.clocktz ایران`\n",
                 "🔁 برگشت: `.clocktz off`\n\n",
                 "**کشورهای آماده:**"]
        for n in ["ایران", "دبی", "ترکیه", "آلمان", "لندن", "نیویورک",
                  "لاس", "مسکو", "استرالیا", "ژاپن"]:
            lines.append(f"• `{n}`")
        lines.append("\n💡 هر شهر دیگه هم انگلیسی: `.clocktz Paris`")
        return await m.edit("\n".join(lines))
    inp = args[1].strip()
    if inp.lower() in ("off", "خاموش", "سیستم"):
        db["clock_tz"] = ""
        save_db()
        return await m.edit("🔁 ساعت به منطقه زمانی سرور برگشت.")
    tz = TZ_ALIASES.get(inp.lower(), inp)
    try:
        now = datetime.now(ZoneInfo(tz))
    except Exception:
        return await m.edit("❌ منطقه زمانی پیدا نشد!\nمثال: `.clocktz ایران` یا `.clocktz Asia/Tehran`")
    db["clock_tz"] = tz
    save_db()
    if db.get("clock"):
        try:
            await app.update_profile(last_name=fmt_clock(db.get('clock_style', 'plain'), now))
        except Exception:
            pass
    await m.edit(f"🌍 **منطقه زمانی:** `{tz}`\n"
                 f"🕐 ساعت الان: {fmt_clock(db.get('clock_style', 'plain'), now)}")

@app.on_message(filters.me & filters.command("font", prefixes=PREFIX))
async def font_cmd(c, m):
    args = m.text.split(maxsplit=2)
    if len(args) < 2:
        return await m.edit("💡 `.font bold متن` | استایل‌ها: bold, italic, mono, double")
    if len(args) == 3 and args[1].lower() in _F:
        style, text = args[1].lower(), args[2]
    else:
        style, text = random.choice(list(_F)), " ".join(args[1:])
    await m.edit(text.translate(_F[style]))

# ── بلاک و سکوت ──
@app.on_message(filters.me & filters.command(["block", "unblock"], prefixes=PREFIX))
async def block_cmd(c, m):
    u = await get_target_user(m)
    if not u:
        return await m.edit("💡 ریپلای کن یا @کاربر رو بنویس")
    if m.command[0] == "block":
        await c.block_user(u.id)
        await m.edit(f"🚫 {u.first_name} بلاک شد")
    else:
        await c.unblock_user(u.id)
        await m.edit(f"✅ {u.first_name} آنبلاک شد")

@app.on_message(filters.me & filters.command(["mute", "unmute"], prefixes=PREFIX))
async def mute_cmd(c, m):
    if not m.reply_to_message:
        return await m.edit("💡 ریپلای کن (فقط در سوپرگروه‌ها)")
    uid = m.reply_to_message.from_user.id
    rights = raw.ChatBannedRights(
        until_date=datetime.now() + timedelta(seconds=parse_time(m.command[1]) if m.command[0] == "mute" and len(m.command) > 1 else 3600),
        send_messages=True) if m.command[0] == "mute" else raw.ChatBannedRights(until_date=datetime.now())
    try:
        await app.invoke(functions.channels.EditBanned(
            channel=await app.resolve_peer(m.chat.id),
            participant=await app.resolve_peer(uid),
            banned_rights=rights))
        await m.edit("🔇 کاربر ساکت شد" if m.command[0] == "mute" else "🔊 کاربر آزاد شد")
    except Exception as e:
        await m.edit(f"❌ {e}")

# ── امنیت و AutoSave ──
@app.on_message(filters.me & filters.command("2fa", prefixes=PREFIX))
async def twofa_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1] == "off":
        try:
            await c.disable_cloud_password(db.get("pw", ""))
            db["pw"] = ""
            save_db()
            await m.edit("🔓 رمز دو مرحله‌ای حذف شد")
        except Exception as e:
            await m.edit(f"⚠️ {e}")
    else:
        pw = parts[1]
        try:
            if db.get("pw"):
                await c.change_cloud_password(db["pw"], pw)
            else:
                await c.enable_cloud_password(pw)
            db["pw"] = pw
            save_db()
            await m.edit(f"🔐 قفل دو مرحله‌ای ست شد: {'*' * len(pw)}")
        except Exception as e:
            await m.edit(f"⚠️ {e}")

@app.on_message(filters.me & filters.command("autosave", prefixes=PREFIX))
async def autosave_cmd(c, m):
    val = await toggle_key("autosave")
    await m.edit(f"📥 AutoSave: {'✅ روشن' if val else '❌ خاموش'}")

# ── آنلاین و اکشن ──
@app.on_message(filters.me & filters.command("online", prefixes=PREFIX))
async def online_cmd(c, m):
    val = await toggle_key("online")
    await m.edit(f"🟢 همیشه آنلاین: {'✅ روشن' if val else '❌ خاموش'}")

@app.on_message(filters.me & filters.command("typing", prefixes=PREFIX))
async def typing_cmd(c, m):
    secs = 10
    if len(m.command) > 1:
        try:
            secs = parse_time(m.command[1])
        except Exception:
            pass
    await m.delete()
    end = time.time() + secs
    while time.time() < end:
        try:
            await app.send_chat_action(m.chat.id, "typing")
        except Exception:
            break
        await asyncio.sleep(4)

# ── ریاکشن خودکار ──
@app.on_message(filters.me & filters.command("react", prefixes=PREFIX))
async def react_cmd(c, m):
    val = await toggle_key("autoreact")
    await m.edit(f"⚡️ ریاکشن خودکار: {'✅ روشن' if val else '❌ خاموش'}")

@app.on_message(filters.me & filters.command("reactlist", prefixes=PREFIX))
async def reactlist_cmd(c, m):
    parts = m.text.split()
    if len(parts) > 1:
        db["react_emojis"] = parts[1:]
        save_db()
        await m.edit("✅ لیست ریاکشن‌ها آپدیت شد")
    else:
        await m.edit("لطفاً حداقل یک ایموجی بفرست 🥺")

# ── منشی عمومی ──
@app.on_message(filters.me & filters.command("reply", prefixes=PREFIX))
async def reply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.reply on | off | متن جواب`")
    if parts[1] == "on" or parts[1] == "off":
        val = await toggle_key("autoreply", parts[1] == "on")
        await m.edit(f"🤖 جواب عمومی: {'✅ روشن' if val else '❌ خاموش'}")
    else:
        db["autoreply_text"] = parts[1]
        save_db()
        await m.edit("✅ متن جواب عمومی ذخیره شد")

@app.on_message(filters.me & filters.command("addreply", prefixes=PREFIX))
async def addreply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or "|" not in parts[1]:
        return await m.edit("💡 `.addreply کلمه | جواب`")
    k, v = parts[1].split("|", 1)
    db["keyword_replies"][k.strip().lower()] = v.strip()
    save_db()
    await m.edit("✅ جواب خودکار ثبت شد")

@app.on_message(filters.me & filters.command("delreply", prefixes=PREFIX))
async def delreply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.delreply کلمه`")
    db["keyword_replies"].pop(parts[1].strip().lower(), None)
    save_db()
    await m.edit("✅ حذف شد")

# ── تبچی و تایمر ──
@app.on_message(filters.me & filters.command("fwd", prefixes=PREFIX))
async def fwd_cmd(c, m):
    parts = m.text.split()
    if len(parts) < 2 or parts[1] in ("on", "off"):
        val = await toggle_key("forwarder")
        await m.edit(f"📢 تبچی: {'✅ روشن' if val else '❌ خاموش'}")
        return
    if parts[1] == "add" and len(parts) == 4:
        try:
            src = await resolve_target(parts[2], m.chat.id)
            dst = await resolve_target(parts[3], m.chat.id)
            db["fwd_pairs"].append([src, dst])
            save_db()
            await m.edit(f"✅ اضافه شد: `{src}` → `{dst}`")
        except Exception as e:
            await m.edit(f"❌ {e}")
    elif parts[1] == "list":
        txt = "\n".join(f"`{s}` → `{d}`" for s, d in db["fwd_pairs"]) or "خالی!"
        await m.edit(f"📢 لیست تبچی:\n{txt}")
    elif parts[1] == "clear":
        db["fwd_pairs"] = []
        save_db()
        await m.edit("✅ لیست پاک شد")

@app.on_message(filters.me & filters.command("timer", prefixes=PREFIX))
async def timer_cmd(c, m):
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.edit("💡 `.timer 30s متن` (مدت: s/m/h/d)")
    secs, text = parse_time(parts[1]), parts[2]

    async def later():
        await asyncio.sleep(secs)
        await app.send_message(m.chat.id, f"⏰ {text}")

    asyncio.create_task(later())
    await m.edit(f"⏱ تایمر {parts[1]} فعال شد")

# ── ابزارها ──
@app.on_message(filters.me & filters.command("ping", prefixes=PREFIX))
async def ping_cmd(c, m):
    t = time.time()
    msg = await m.edit("🏓")
    await msg.edit(f"🏓 پونگ! `{(time.time() - t) * 1000:.0f}ms`")

@app.on_message(filters.me & filters.command("id", prefixes=PREFIX))
async def id_cmd(c, m):
    uid = m.reply_to_message.from_user.id if m.reply_to_message else me.id
    await m.edit(f"🆔 چت: `{m.chat.id}`\n👤 کاربر: `{uid}`")

@app.on_message(filters.me & filters.command("info", prefixes=PREFIX))
async def info_cmd(c, m):
    u = m.reply_to_message.from_user if m.reply_to_message else me
    await m.edit(
        f"👤 **{u.first_name} {u.last_name or ''}**\n"
        f"🆔 `{u.id}`\n🔗 @{u.username or '-'}\n"
        f"🤖 ربات: {'بله' if u.is_bot else 'نه'}\n"
        f"⭐ پرمیوم: {'بله' if getattr(u, 'is_premium', False) else 'نه'}")

@app.on_message(filters.me & filters.command("stats", prefixes=PREFIX))
async def stats_cmd(c, m):
    await m.edit("⏳ در حال شمارش...")
    users = bots = groups = channels = 0
    async for d in c.get_dialogs():
        t = d.chat.type
        if t == "private":
            bots += 1 if d.chat.is_bot else 0
            users += 0 if d.chat.is_bot else 1
        elif t in ("group", "supergroup"):
            groups += 1
        elif t == "channel":
            channels += 1
    await m.edit(f"📊 **آمار اکانت**\n\n👤 چت‌های شخصی: {users}\n"
                 f"🤖 ربات‌ها: {bots}\n👥 گروه‌ها: {groups}\n📢 کانال‌ها: {channels}")

@app.on_message(filters.me & filters.command(["del", "purge"], prefixes=PREFIX))
async def del_cmd(c, m):
    if m.command[0] == "del":
        if m.reply_to_message:
            await m.reply_to_message.delete()
        await m.delete()
    else:
        if not m.reply_to_message:
            return await m.edit("💡 ریپلای کن")
        ids = list(range(m.reply_to_message.id, m.id + 1))
        for i in range(0, len(ids), 100):
            await c.delete_messages(m.chat.id, ids[i:i + 100])
        await m.delete()

@app.on_message(filters.me & filters.command("join", prefixes=PREFIX))
async def join_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.join @کانال یا لینک`")
    try:
        await c.join_chat(parts[1])
        await m.edit("✅ عضو شدم")
    except Exception as e:
        await m.edit(f"❌ {e}")

@app.on_message(filters.me & filters.command("leave", prefixes=PREFIX))
async def leave_cmd(c, m):
    await m.chat.leave()

# ── هوش مصنوعی ──
@app.on_message(filters.me & filters.command("ai", prefixes=PREFIX))
async def ai_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.edit("💡 `.ai سوالت`")
    await m.edit("🧠 دارم فکر می‌کنم...")
    answer = await ask_ai(parts[1])
    await m.edit(answer[:4000], parse_mode=None)

# ── منشی اختصاصی: دستورات ──
@app.on_message(filters.me & filters.command("setreply", prefixes=PREFIX))
async def setreply_cmd(c, m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.edit("💡 **دو روش:**\n\n"
                            "۱. ریپلای به پیام طرف + `.setreply متن جواب`\n"
                            "۲. `.setreply @آیدی | متن جواب`")
    if m.reply_to_message and m.reply_to_message.from_user:
        u, text = m.reply_to_message.from_user, args[1]
    else:
        if "|" not in args[1]:
            return await m.edit("💡 فرمت درست: `.setreply @آیدی | متن`")
        ident, text = args[1].split("|", 1)
        ident, text = ident.strip(), text.strip()
        if not text:
            return await m.edit("❌ متن جواب خالیه!")
        try:
            u = await c.get_users(ident.strip("@"))
        except Exception:
            return await m.edit("❌ کاربر پیدا نشد! آیدی رو درست بنویس یا ریپلای بزن.")
    db.setdefault("user_replies", {})
    db["user_replies"][str(u.id)] = {"name": u.first_name, "text": text.strip()}
    db["userreply"] = True
    save_db()
    await m.edit(f"✅ جواب اختصاصی برای **{u.first_name}** ثبت شد:\n\n{text.strip()[:800]}")

@app.on_message(filters.me & filters.command(["unsetreply", "delreplyuser"], prefixes=PREFIX))
async def unsetreply_cmd(c, m):
    urep = db.setdefault("user_replies", {})
    if m.reply_to_message and m.reply_to_message.from_user:
        uid = str(m.reply_to_message.from_user.id)
    elif m.chat.type == "private" and m.chat.id != me.id:
        uid = str(m.chat.id)
    elif len(m.command) > 1:
        try:
            u = await c.get_users(m.command[1].strip("@"))
            uid = str(u.id)
        except Exception:
            return await m.edit("❌ کاربر پیدا نشد!")
    else:
        return await m.edit("💡 ریپلای به پیام طرف بزن + `.unsetreply` یا: `.unsetreply @آیدی`")
    if urep.pop(uid, None):
        save_db()
        await m.edit("🗑 حذف شد!")
    else:
        await m.edit("❓ برای این کاربر جوابی ثبت نشده بود.")

@app.on_message(filters.me & filters.command(["userreplies", "listreplies"], prefixes=PREFIX))
async def userreplies_cmd(c, m):
    urep = db.get("user_replies", {})
    if not urep:
        return await m.edit("📭 هنوز جوابی ثبت نشده!\nبا `.setreply` اضافه کن.")
    lines = [f"📇 **جواب‌های اختصاصی ({len(urep)} نفر)**\n"]
    for uid, ent in urep.items():
        preview = ent["text"][:60] + ("..." if len(ent["text"]) > 60 else "")
        lines.append(f"👤 {ent['name']} (`{uid}`)\n↳ {preview}\n")
    lines.append("🗑 حذف: `.unsetreply` (ریپلای)")
    await m.edit("\n".join(lines))

@app.on_message(filters.me & filters.command("userreply", prefixes=PREFIX))
async def userreply_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else ""
    if arg in ("on", "روشن"):
        db["userreply"] = True; save_db()
        await m.edit("✅ منشی اختصاصی **روشن** شد!")
    elif arg in ("off", "خاموش"):
        db["userreply"] = False; save_db()
        await m.edit("❌ منشی اختصاصی **خاموش** شد!")
    elif arg == "time" and len(m.command) > 2:
        try:
            db["userreply_cd"] = max(0, int(m.command[2])); save_db()
            await m.edit(f"⏳ فاصله جواب هر نفر: **{db['userreply_cd']} ثانیه**")
        except Exception:
            await m.edit("💡 `.userreply time 120`")
    else:
        s = "✅ روشن" if db.get("userreply") else "❌ خاموش"
        await m.edit(f"🤖 **منشی اختصاصی:** {s}\n"
                     f"⏳ فاصله جواب: {db.get('userreply_cd', 60)} ثانیه\n\n"
                     "`.userreply on | off`\n`.userreply time 120`")

@app.on_message(filters.me & filters.command("greetonly", prefixes=PREFIX))
async def greetonly_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else ""
    if arg in ("on", "روشن"):
        db["greet_only"] = True; save_db()
        await m.edit("🚪 حالت «فقط سلام» ✅ روشن\nفقط به پیام‌های سلام جواب می‌ده")
    elif arg in ("off", "خاموش"):
        db["greet_only"] = False; save_db()
        await m.edit("🚪 حالت «فقط سلام» ❌ خاموش\nبه همه پیام‌ها جواب می‌ده")
    else:
        s = "✅ فقط سلام" if db.get("greet_only", True) else "🌐 همه پیام‌ها"
        await m.edit(f"🚪 **فیلتر سلام**\nحالت فعلی: {s}\n\n`.greetonly on | off`")

# ═══════════════════════════════════════════════
#  ⚙️ هندلرهای خودکار
# ═══════════════════════════════════════════════

@app.on_message(~filters.service, group=10)  # 📢 تبچی
async def fwd_handler(c, m):
    if not db.get("forwarder"):
        return
    for src, dst in db.get("fwd_pairs", []):
        if m.chat.id == src:
            try:
                await m.copy(dst)
            except Exception:
                try:
                    await m.forward(dst)
                except Exception:
                    pass

REPLY_COOLDOWN = {}

@app.on_message(filters.private & filters.incoming & ~filters.me & ~filters.bot & ~filters.service, group=11)  # 🤖 منشی
async def secretary_handler(c, m):
    text = m.text or ""
    # ۱) جواب‌های کلمه‌ای (`.addreply`)
    if text:
        for key, val in db.get("keyword_replies", {}).items():
            if key in text.lower():
                try:
                    await m.reply(val)
                except Exception:
                    pass
                return
    # 🚪 فیلتر سلام: اگه فقط-سلام فعاله و پیام سلام نیست → بی‌خیال
    if db.get("greet_only", True) and not is_greeting(text):
        return
    # ۲) جواب اختصاصی همین شخص (`.setreply`)
    if db.get("userreply"):
        ent = db.get("user_replies", {}).get(str(m.from_user.id))
        if ent:
            cd = db.get("userreply_cd", 60)
            k = f"u{m.from_user.id}"
            if time.time() - REPLY_COOLDOWN.get(k, 0) > cd:
                REPLY_COOLDOWN[k] = time.time()
                try:
                    await m.reply(ent["text"], parse_mode=None)
                except Exception:
                    pass
            return
    # ۳) جواب عمومی (`.reply on`)
    if db.get("autoreply") and time.time() - REPLY_COOLDOWN.get(m.chat.id, 0) > 300:
        REPLY_COOLDOWN[m.chat.id] = time.time()
        try:
            await m.reply(db["autoreply_text"])
        except Exception:
            pass

@app.on_message(filters.incoming & ~filters.me & ~filters.service, group=12)  # ⚡️ ریاکشن
async def autoreact_handler(c, m):
    if db.get("autoreact"):
        await react_to(m, random.choice(db.get("react_emojis", ["👍"])))

@app.on_message(filters.private & filters.incoming & ~filters.me, group=13)  # 📥 AutoSave
async def autosave_handler(c, m):
    if db.get("autosave") and (m.photo or m.video or m.document or m.audio):
        try:
            path = await m.download(file_name=DOWNLOAD_DIR)
            print(f"[AutoSave] ذخیره شد: {path}")
        except Exception:
            pass

# ═══════════════════════════════════════════════
#  🎛 کال‌بک‌های پنل (سیو مسیج)
# ═══════════════════════════════════════════════
@app.on_callback_query()
async def callbacks(c, q: CallbackQuery):
    data = q.data or ""
    try:
        if data == "close":
            await q.message.delete()
        elif data == "back":
            await q.message.edit_text(PANEL_TEXT, reply_markup=panel_kb())
        elif data == "status":
            await q.message.edit_text(status_text(), reply_markup=status_kb())
        elif data.startswith("toggle:"):
            key = data.split(":", 1)[1]
            await toggle_clock() if key == "clock" else await toggle_key(key)
            await q.message.edit_text(status_text(), reply_markup=status_kb())
        elif data.startswith("help:"):
            await q.message.edit_text(
                HELP.get(data.split(":", 1)[1], "یافت نشد"),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 بازگشت", "back")]]))
        await q.answer()
    except Exception:
        pass

# ═══════════════════════════════════════════════
#  🤖 پنل ربات تلگرامی (کنترل با / کامندها)
# ═══════════════════════════════════════════════
BF = filters.user(OWNER_ID) & filters.private

@bot.on_message(BF & filters.command(["start", "panel", "help", "menu"], prefixes="/"))
async def bot_panel_cmd(c, m):
    await m.reply(PANEL_TEXT, reply_markup=panel_kb())

# ── پروفایل ──
@bot.on_message(BF & filters.command("name", prefixes="/"))
async def bot_name_cmd(c, m):
    parts = m.text.split(maxsplit=2)
    first = parts[1] if len(parts) > 1 else me.first_name
    last = parts[2] if len(parts) > 2 else ""
    await app.update_profile(first_name=first, last_name=last)
    await m.reply(f"✅ اسم تغییر کرد به: **{first} {last}**".strip())

@bot.on_message(BF & filters.command("bio", prefixes="/"))
async def bot_bio_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.reply("💡 `/bio متن بیو`")
    await app.update_profile(bio=parts[1][:70])
    await m.reply("✅ بیو آپدیت شد")

@bot.on_message(BF & filters.command("username", prefixes="/"))
async def bot_username_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.reply("💡 `/username آیدی`")
    try:
        await app.set_username(parts[1].strip("@"))
        await m.reply("✅ آیدی تغییر کرد")
    except Exception as e:
        await m.reply(f"❌ {e}")

@bot.on_message(BF & filters.command("setpic", prefixes="/"))
async def bot_setpic_cmd(c, m):
    r = m.reply_to_message
    if not (r and r.photo):
        return await m.reply("💡 یه عکس بفرست، ریپلایش کن و /setpic بزن")
    f = await r.download()
    await app.set_profile_photo(photo=f)
    os.remove(f)
    await m.reply("✅ عکس پروفایل تغییر کرد")

# ── ساعت ──
@bot.on_message(BF & filters.command("clock", prefixes="/"))
async def bot_clock_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else None
    state = None if arg not in ("on", "off") else arg == "on"
    val = await toggle_clock(state)
    await m.reply(f"⏰ ساعت در نام: {'✅ روشن' if val else '❌ خاموش'}")

@bot.on_message(BF & filters.command("clockstyle", prefixes="/"))
async def bot_clockstyle_cmd(c, m):
    args = m.text.split()
    if len(args) > 1:
        pick = args[1]
        if pick.isdigit():
            i = int(pick) - 1
            if 0 <= i < len(CLOCK_STYLE_NAMES):
                pick = CLOCK_STYLE_NAMES[i]
            else:
                return await m.reply("❌ شماره بین 1 تا 20 باشه")
        if pick not in CLOCK_STYLE_NAMES:
            return await m.reply("❌ استایل وجود نداره. `/clockstyle` رو تنها بزن.")
        db["clock_style"] = pick
        save_db()
        if db.get("clock"):
            try:
                await app.update_profile(last_name=fmt_clock(pick, get_now()))
            except Exception:
                pass
        return await m.reply(f"✅ استایل: **{pick}**\nپیش‌نمایش: {fmt_clock(pick, get_now())}")
    lines = ["🎨 **استایل‌های ساعت** — انتخاب با `/clockstyle شماره`\n"]
    for i, name in enumerate(CLOCK_STYLE_NAMES, 1):
        lines.append(f"`{i:>2}.` {fmt_clock(name, get_now())}")
    lines.append(f"\n📌 فعلی: **{db.get('clock_style', 'plain')}**")
    await m.reply("\n".join(lines))

@bot.on_message(BF & filters.command("clocktz", prefixes="/"))
async def bot_clocktz_cmd(c, m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("💡 `/clocktz ایران` — برگشت: `/clocktz off`")
    inp = args[1].strip()
    if inp.lower() in ("off", "خاموش", "سیستم"):
        db["clock_tz"] = ""
        save_db()
        return await m.reply("🔁 ساعت به منطقه سیستم برگشت.")
    tz = TZ_ALIASES.get(inp.lower(), inp)
    try:
        now = datetime.now(ZoneInfo(tz))
    except Exception:
        return await m.reply("❌ پیدا نشد! مثال: `/clocktz ایران`")
    db["clock_tz"] = tz
    save_db()
    if db.get("clock"):
        try:
            await app.update_profile(last_name=fmt_clock(db.get('clock_style', 'plain'), now))
        except Exception:
            pass
    await m.reply(f"🌍 منطقه زمانی: `{tz}`\n🕐 الان: {fmt_clock(db.get('clock_style', 'plain'), now)}")

# ── سوییچ‌های ساده ──
_SIMPLE = {"online": ("🟢 همیشه آنلاین", "online"),
           "react": ("⚡️ ریاکشن خودکار", "autoreact"),
           "autosave": ("📥 AutoSave", "autosave")}

@bot.on_message(BF & filters.command(list(_SIMPLE), prefixes="/"))
async def bot_simple_toggles(c, m):
    lbl, key = _SIMPLE[m.command[0]]
    val = await toggle_key(key)
    await m.reply(f"{lbl}: {'✅ روشن' if val else '❌ خاموش'}")

@bot.on_message(BF & filters.command("greetonly", prefixes="/"))
async def bot_greetonly_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else ""
    if arg in ("on", "روشن"):
        db["greet_only"] = True; save_db()
    elif arg in ("off", "خاموش"):
        db["greet_only"] = False; save_db()
    s = "✅ فقط سلام" if db.get("greet_only", True) else "🌐 همه پیام‌ها"
    await m.reply(f"🚪 فیلتر سلام: {s}")

@bot.on_message(BF & filters.command("reactlist", prefixes="/"))
async def bot_reactlist_cmd(c, m):
    parts = m.text.split()
    if len(parts) > 1:
        db["react_emojis"] = parts[1:]
        save_db()
        await m.reply("✅ لیست ریاکشن‌ها آپدیت شد")
    else:
        await m.reply("ایموجی‌های فعلی: " + " ".join(db.get("react_emojis", ["👍"])))

# ── منشی ──
@bot.on_message(BF & filters.command("reply", prefixes="/"))
async def bot_reply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.reply("💡 `/reply on | off | متن جواب عمومی`")
    if parts[1] in ("on", "off"):
        val = await toggle_key("autoreply", parts[1] == "on")
        await m.reply(f"🤖 جواب عمومی: {'✅ روشن' if val else '❌ خاموش'}")
    else:
        db["autoreply_text"] = parts[1]
        save_db()
        await m.reply("✅ متن جواب عمومی ذخیره شد")

@bot.on_message(BF & filters.command("setreply", prefixes="/"))
async def bot_setreply_cmd(c, m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        return await m.reply("💡 **دو روش:**\n\n۱. پیام طرف رو فوروارد کن به این ربات، ریپلایش کن + `/setreply متن`\n۲. `/setreply @آیدی | متن`")
    r = m.reply_to_message
    if r and getattr(r, "forward_from", None):
        u, text = r.forward_from, args[1]
    else:
        if "|" not in args[1]:
            return await m.reply("💡 فرمت: `/setreply @آیدی | متن`")
        ident, text = args[1].split("|", 1)
        ident, text = ident.strip(), text.strip()
        if not text:
            return await m.reply("❌ متن جواب خالیه!")
        try:
            u = await c.get_users(ident.strip("@"))
        except Exception:
            return await m.reply("❌ کاربر پیدا نشد! (اگه فوروارد مخفیه، از @آیدی استفاده کن)")
    db.setdefault("user_replies", {})
    db["user_replies"][str(u.id)] = {"name": u.first_name, "text": text.strip()}
    db["userreply"] = True
    save_db()
    await m.reply(f"✅ جواب اختصاصی **{u.first_name}** ثبت شد:\n\n{text.strip()[:800]}")

@bot.on_message(BF & filters.command(["unsetreply", "delreplyuser"], prefixes="/"))
async def bot_unsetreply_cmd(c, m):
    urep = db.setdefault("user_replies", {})
    r = m.reply_to_message
    if r and getattr(r, "forward_from", None):
        uid = str(r.forward_from.id)
    elif len(m.command) > 1:
        try:
            u = await c.get_users(m.command[1].strip("@"))
            uid = str(u.id)
        except Exception:
            return await m.reply("❌ کاربر پیدا نشد!")
    else:
        return await m.reply("💡 `/unsetreply @آیدی` یا فوروارد پیام طرف رو ریپلای کن")
    if urep.pop(uid, None):
        save_db()
        await m.reply("🗑 حذف شد!")
    else:
        await m.reply("❓ جوابی ثبت نشده بود.")

@bot.on_message(BF & filters.command(["userreplies", "listreplies"], prefixes="/"))
async def bot_userreplies_cmd(c, m):
    urep = db.get("user_replies", {})
    if not urep:
        return await m.reply("📭 هنوز جوابی ثبت نشده! با /setreply اضافه کن.")
    lines = [f"📇 **جواب‌های اختصاصی ({len(urep)} نفر)**\n"]
    for uid, ent in urep.items():
        preview = ent["text"][:60] + ("..." if len(ent["text"]) > 60 else "")
        lines.append(f"👤 {ent['name']} (`{uid}`)\n↳ {preview}\n")
    await m.reply("\n".join(lines))

@bot.on_message(BF & filters.command("userreply", prefixes="/"))
async def bot_userreply_cmd(c, m):
    arg = m.command[1] if len(m.command) > 1 else ""
    if arg in ("on", "روشن"):
        db["userreply"] = True; save_db()
    elif arg in ("off", "خاموش"):
        db["userreply"] = False; save_db()
    elif arg == "time" and len(m.command) > 2:
        try:
            db["userreply_cd"] = max(0, int(m.command[2])); save_db()
        except Exception:
            pass
    s = "✅ روشن" if db.get("userreply") else "❌ خاموش"
    await m.reply(f"🤖 منشی اختصاصی: {s}\n⏳ فاصله: {db.get('userreply_cd', 60)} ثانیه")

@bot.on_message(BF & filters.command("addreply", prefixes="/"))
async def bot_addreply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or "|" not in parts[1]:
        return await m.reply("💡 `/addreply کلمه | جواب`")
    k, v = parts[1].split("|", 1)
    db["keyword_replies"][k.strip().lower()] = v.strip()
    save_db()
    await m.reply("✅ ثبت شد")

@bot.on_message(BF & filters.command("delreply", prefixes="/"))
async def bot_delreply_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.reply("💡 `/delreply کلمه`")
    db["keyword_replies"].pop(parts[1].strip().lower(), None)
    save_db()
    await m.reply("✅ حذف شد")

# ── تبچی و تایمر ──
@bot.on_message(BF & filters.command("fwd", prefixes="/"))
async def bot_fwd_cmd(c, m):
    parts = m.text.split()
    if len(parts) < 2 or parts[1] in ("on", "off"):
        val = await toggle_key("forwarder")
        return await m.reply(f"📢 تبچی: {'✅ روشن' if val else '❌ خاموش'}")
    if parts[1] == "add" and len(parts) == 4:
        try:
            src = await resolve_target(parts[2], 0)
            dst = await resolve_target(parts[3], 0)
            db["fwd_pairs"].append([src, dst])
            save_db()
            await m.reply(f"✅ اضافه شد: `{src}` → `{dst}`")
        except Exception as e:
            await m.reply(f"❌ {e}")
    elif parts[1] == "list":
        txt = "\n".join(f"`{s}` → `{d}`" for s, d in db["fwd_pairs"]) or "خالی!"
        await m.reply(f"📢 لیست تبچی:\n{txt}")
    elif parts[1] == "clear":
        db["fwd_pairs"] = []
        save_db()
        await m.reply("✅ لیست پاک شد")

@bot.on_message(BF & filters.command("timer", prefixes="/"))
async def bot_timer_cmd(c, m):
    parts = m.text.split(maxsplit=2)
    if len(parts) < 3:
        return await m.reply("💡 `/timer 30s متن` (s/m/h/d)")
    secs, text = parse_time(parts[1]), parts[2]
    chat_id = m.chat.id
    async def later():
        await asyncio.sleep(secs)
        try:
            await bot.send_message(chat_id, f"⏰ {text}")
        except Exception:
            pass
    asyncio.create_task(later())
    await m.reply(f"⏱ تایمر {parts[1]} فعال شد — همین‌جا یادآوری می‌دم!")

# ── بلاک و امنیت ──
@bot.on_message(BF & filters.command(["block", "unblock"], prefixes="/"))
async def bot_block_cmd(c, m):
    r = m.reply_to_message
    if r and getattr(r, "forward_from", None):
        u = r.forward_from
    elif len(m.command) > 1:
        try:
            u = await c.get_users(m.command[1].strip("@"))
        except Exception:
            return await m.reply("❌ کاربر پیدا نشد!")
    else:
        return await m.reply("💡 `/block @آیدی`")
    if m.command[0] == "block":
        await app.block_user(u.id)
        await m.reply(f"🚫 {u.first_name} بلاک شد")
    else:
        await app.unblock_user(u.id)
        await m.reply(f"✅ {u.first_name} آنبلاک شد")

@bot.on_message(BF & filters.command("2fa", prefixes="/"))
async def bot_2fa_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1] == "off":
        try:
            await app.disable_cloud_password(db.get("pw", ""))
            db["pw"] = ""
            save_db()
            await m.reply("🔓 رمز دو مرحله‌ای حذف شد")
        except Exception as e:
            await m.reply(f"⚠️ {e}")
    else:
        pw = parts[1]
        try:
            if db.get("pw"):
                await app.change_cloud_password(db["pw"], pw)
            else:
                await app.enable_cloud_password(pw)
            db["pw"] = pw
            save_db()
            await m.reply("🔐 قفل دو مرحله‌ای ست شد")
        except Exception as e:
            await m.reply(f"⚠️ {e}")

# ── ابزارها ──
@bot.on_message(BF & filters.command("ping", prefixes="/"))
async def bot_ping_cmd(c, m):
    t = time.time()
    msg = await m.reply("🏓")
    await msg.edit(f"🏓 پونگ! `{(time.time() - t) * 1000:.0f}ms`")

@bot.on_message(BF & filters.command("stats", prefixes="/"))
async def bot_stats_cmd(c, m):
    msg = await m.reply("⏳ در حال شمارش...")
    users = bots = groups = channels = 0
    async for d in app.get_dialogs():
        t = d.chat.type
        if t == "private":
            if d.chat.is_bot: bots += 1
            else: users += 1
        elif t in ("group", "supergroup"): groups += 1
        elif t == "channel": channels += 1
    await msg.edit(f"📊 **آمار اکانت**\n\n👤 چت‌های شخصی: {users}\n"
                   f"🤖 ربات‌ها: {bots}\n👥 گروه‌ها: {groups}\n📢 کانال‌ها: {channels}")

@bot.on_message(BF & filters.command(["info", "id"], prefixes="/"))
async def bot_info_cmd(c, m):
    if len(m.command) > 1:
        try:
            u = await c.get_users(m.command[1].strip("@"))
        except Exception:
            return await m.reply("❌ کاربر پیدا نشد!")
    else:
        u = me
    await m.reply(f"👤 **{u.first_name} {u.last_name or ''}**\n"
                  f"🆔 `{u.id}`\n🔗 @{u.username or '-'}")

@bot.on_message(BF & filters.command("ai", prefixes="/"))
async def bot_ai_cmd(c, m):
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        return await m.reply("💡 `/ai سوالت`")
    msg = await m.reply("🧠 دارم فکر می‌کنم...")
    answer = await ask_ai(parts[1])
    await msg.edit(answer[:4000], parse_mode=None)

# ── دکمه‌های پنل ربات ──
@bot.on_callback_query(filters.user(OWNER_ID))
async def bot_callbacks(c, q):
    data = q.data or ""
    try:
        if data == "close":
            await q.message.delete()
        elif data == "back":
            await q.message.edit_text(PANEL_TEXT, reply_markup=panel_kb())
        elif data == "status":
            await q.message.edit_text(status_text(), reply_markup=status_kb())
        elif data.startswith("toggle:"):
            key = data.split(":", 1)[1]
            if key == "clock":
                await toggle_clock()
            else:
                await toggle_key(key)
            await q.message.edit_text(status_text(), reply_markup=status_kb())
        elif data.startswith("help:"):
            await q.message.edit_text(
                HELP.get(data.split(":", 1)[1], "یافت نشد"),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 بازگشت", "back")]]))
        await q.answer()
    except Exception:
        pass

# ═══════════════════════════════════════════════
#  🚀 اجرا
# ═══════════════════════════════════════════════
async def main():
    global me
    await app.start()
    me = await app.get_me()
    asyncio.create_task(clock_loop())
    asyncio.create_task(online_loop())
    if BOT_TOKEN:
        await bot.start()
        print("🤖 پنل ربات تلگرامی هم وصل شد!")
        if OWNER_ID:
            try:
                await bot.send_message(OWNER_ID,
                    "🟢 **پنل ربات وصل شد!**\nاز این به بعد از همین‌جا کنترلم کن 🎛",
                    reply_markup=panel_kb())
            except Exception:
                pass
    print(f"⚡️ یوزربات {me.first_name} روشن شد!")
    await idle()
    await app.stop()
    if BOT_TOKEN:
        await bot.stop()

if __name__ == "__main__":
    app.run(main())