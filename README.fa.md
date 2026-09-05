<div align="center">

# ⚡️ پنل سلف 3OUTHBOY

**🎮 یک پنل شیشه‌ای برای مدیریت، شخصی‌سازی و خودکارسازی اکانت تلگرام**

یوزربات پیشرفته با **دو رابط**: پنل ربات تلگرامی با دکمه‌های شیشه‌ای 🤖 + دستورات سریع نقطه‌ای در هر چتی 💬

[English](README.md) | **فارسی**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-orange?logo=telegram&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-GPL--3.0-green)

</div>

---

<div align="center">

> «✨ همه‌چی یک‌جا؛ ساده، سریع، حرفه‌ای.»

</div>

---

## ✨ امکانات

| دسته | قابلیت‌ها |
|---|---|
| 👤 **پروفایل و بیو** | تغییر اسم، بیو، آیدی و عکس پروفایل — همه با دستور |
| ⏰ **ساعت زنده** | ۲۰ استایل زیبا کنار اسمت + منطقه زمانی هر کشور 🌍 |
| 🛡 **مدیریت** | بلاک / آنبلاک / سکوت کاربران در گروه |
| 🔒 **امنیت** | قفل دو مرحله‌ای (2FA) + ذخیره خودکار مدیا |
| 🟢 **حضور** | حالت همیشه‌آنلاین + اکشن‌های فیک (تایپینگ، ضبط...) |
| ⚡️ **تعامل** | ریاکشن خودکار با ایموجی‌های دلخواه |
| 🤖 **منشی هوشمند** | جواب اختصاصی برای هر شخص + فیلتر «فقط سلام» |
| 📢 **تبچی و تایمر** | فوروارد خودکار بین چت‌ها + یادآور زمان‌دار |
| 🎛 **دو رابط** | پنل ربات با دکمه‌های شیشه‌ای + کامندهای سریع `.` |
| 🧠 **هوش مصنوعی** | گفتگو با AI (اختیاری — سازگار با OpenRouter) |
| 📋 **ابزارها** | پینگ، آمار، پاکسازی، عضویت/خروج، اطلاعات کاربر و... |

---

## 🖼 پیش‌نمایش

<!-- اسکرین‌شاتت رو اینجا اضافه کن:
![پنل](screenshot.png)
-->

---

## 🚀 نصب

### ⭐ نصب سریع — نصاب تعاملی (پیشنهادی)

فقط **یه دستور**! نصاب خودش همه‌کار رو انجام می‌ده: پکیج‌های سیستم رو نصب می‌کنه، محیط مجازی می‌سازه، **تنظیمات رو به‌صورت سوال ازت می‌پرسه** (بدون ویرایش دستی فایل!)، سرویس ۲۴ ساعته systemd رو راه می‌ندازه و ورود به تلگرام رو هم قدم‌به‌قدم باهات انجام می‌ده ✨

```bash
git clone https://github.com/3OUTHBOY/3outhboy-userbot.git
cd 3outhboy-userbot
bash install.sh
```

نصاب ازت این‌ها رو می‌پرسه:

- 🔑 `API_ID` و `API_HASH` — از [my.telegram.org](https://my.telegram.org)
- 🤖 `BOT_TOKEN` — از [@BotFather](https://t.me/BotFather) *(اختیاری — Enter بزن تا رد شه)*
- 👤 `OWNER_ID` — آیدی عددی خودت از [@userinfobot](https://t.me/userinfobot)
- 🧠 `AI_API_KEY` — از [openrouter.ai](https://openrouter.ai) *(اختیاری — Enter بزن تا رد شه)*

بعدش خودش ربات رو برای اولین ورود روشن می‌کنه (شماره تلفن + کد ورود که داخل خود تلگرام میاد) و در آخر سرویس ۲۴ ساعته رو خودکار فعال می‌کنه ✅

### 🔧 نصب دستی (روش جایگزین)

<details>
<summary>باز کن برای دیدن مراحل دستی</summary>

#### پیش‌نیازها

- 🐍 پایتون 3.10 به بالا (پیشنهادی: **3.12**)
- 🌐 یه سرور یا VPS (پیشنهادی: Ubuntu 24.04) — یا خود PC خودت
- 🔑 `API_ID` و `API_HASH` از [my.telegram.org](https://my.telegram.org)

#### قدم ۱ — دریافت پروژه و نصب

```bash
apt update && apt install python3 python3-pip python3-venv -y

git clone https://github.com/3OUTHBOY/3outhboy-userbot.git
cd 3outhboy-userbot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### قدم ۲ — تنظیمات

```bash
cp config.example.py config.py
nano config.py
```

| متغیر | توضیح | از کجا بگیرمش؟ |
|---|---|---|
| `API_ID` | شناسه اپلیکیشن | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | هش اپلیکیشن | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | توکن ربات پنل (اختیاری) | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | آیدی عددی خودت | [@userinfobot](https://t.me/userinfobot) |
| `STRING_SESSION` | روی سرور خالی بذار | — |
| `AI_API_KEY` | کلید OpenRouter (اختیاری) | [openrouter.ai](https://openrouter.ai) |

#### قدم ۳ — اولین اجرا

```bash
python bot.py
```

ازت شماره تلفن و کد ورود رو می‌پرسه (کد **داخل خود تلگرام** میاد، نه SMS). این فقط **یک بار** اتفاق می‌افته ✅

#### قدم ۴ — اجرای دائمی ۲۴ ساعته با systemd 🕐

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

### 🛠 مدیریت سرویس

| کار | دستور |
|---|---|
| دیدن لاگ زنده | `journalctl -u userbot -f` |
| ری‌استارت (بعد از تغییر کد) | `systemctl restart userbot` |
| خاموش / روشن | `systemctl stop userbot` / `systemctl start userbot` |
| آپدیت ربات | `cd 3outhboy-userbot && git pull && systemctl restart userbot` |

---

## 📖 طرز استفاده

بعد از اجرا، پنل خودکار برات ارسال می‌شه:

- **چت با ربات:** `/panel` — کنترل کامل با دکمه‌های شیشه‌ای 🎛
- **هر چتی (سیو‌مسیج و...):** `.panel` — دستورات سریع با نقطه

فقط `OWNER_ID` می‌تونه به ربات فرمان بده — بقیه کامل نادیده گرفته می‌شن 🔒

### مرجع دستورات

<details>
<summary>👤 پروفایل و بیو</summary>

- `/name اسم فامیلی` — تغییر اسم
- `/bio متن` — تغییر بیو
- `/username آیدی` — تغییر آیدی
- `/setpic` (ریپلای به عکس) — عکس پروفایل

</details>

<details>
<summary>⏰ ساعت و فونت</summary>

- `/clock on / off` — ساعت زنده کنار اسم
- `/clockstyle` — ۲۰ استایل زیبا (ساعت ایموجی، فونت‌های دیجیتال و...)
- `/clocktz ایران` — منطقه زمانی خودکار هر کشور
- `.font bold متن` — متن با فونت فان (bold, italic, mono, double)

</details>

<details>
<summary>🤖 منشی (جواب خودکار)</summary>

- `/setreply متن` (ریپلای به پیام) — جواب اختصاصی همون شخص
- `/setreply @آیدی | متن` — همین، با آیدی
- `/unsetreply` — حذف جواب اختصاصی
- `/userreplies` — لیست همه‌ی جواب‌ها
- `/greetonly on / off` — جواب **فقط** به سلام‌ها («سلام»، «hi»...)
- `/reply on / off / متن` — جواب عمومی
- `/addreply کلمه | جواب` — جواب بر اساس کلمه کلیدی

</details>

<details>
<summary>🛡 مدیریت و امنیت</summary>

- `/block @کاربر` / `/unblock @کاربر` — بلاک / آنبلاک
- `.mute 10m` / `.unmute` (ریپلای، سوپرگروه) — سکوت کاربر
- `/2fa رمز` / `/2fa off` — قفل دو مرحله‌ای
- `/autosave` — ذخیره خودکار مدیای دریافتی

</details>

<details>
<summary>⚡️ حضور و ریاکشن</summary>

- `/online` — حالت همیشه‌آنلاین
- `.typing 30` — اکشن فیک «در حال نوشتن»
- `/react` — روشن/خاموش ریاکشن خودکار
- `/reactlist ❤️ 🔥 👑` — تنظیم ایموجی‌های ریاکشن

</details>

<details>
<summary>📢 تبچی، تایمر و ابزارها</summary>

- `/fwd add @مبدا @مقصد` — اتصال دو چت
- `/timer 30s متن` — یادآور زمان‌دار (s/m/h/d)
- `/ping` — تست سرعت
- `/stats` — آمار اکانت
- `/info @کاربر` — اطلاعات کاربر
- `.purge` (ریپلای) — پاکسازی گروهی پیام‌ها
- `.join @کانال` / `.leave` — عضویت / خروج

</details>

<details>
<summary>🧠 هوش مصنوعی</summary>

- `/ai سوالت` — گفتگو با هوش مصنوعی (نیاز به `AI_API_KEY`)

</details>

---

## 🖥 کاربران ویندوز

روی ویندوز هم کار می‌کنه! فقط مطمئن شو **Python 3.12** داری (نسخه‌های جدیدتر ممکنه Pyrogram رو بشکنن):

```
pip install pyrogram aiohttp
python bot.py
```

> 💡 روی ویندوز نصب `tgcrypto` به Visual C++ Build Tools نیاز داره — اختیاریه و بدون اون هم همه‌چیز کار می‌کنه.

---

## ⚠️ هشدارها

- استفاده از یوزربات ممکنه با قوانین تلگرام در تعارض باشه — **مسئولیت اکانت با خودته**
- قابلیت‌های خودکار (ریاکشن، تبچی) رو **معقول** استفاده کن تا اکانتت محدود نشه
- فایل‌های `.session` و `config.py` مثل **رمز اکانتت** حساسن — هرگز به کسی ندی!
- همون اکانت رو روی دو دستگاه هم‌زمان اجرا نکن (جواب‌های دوبل و FloodWait)

---

## 🧹 حذف کامل — پاک کردن از روی سرور

می‌خوای 3OUTHBOY UserBot رو به‌طور کامل از سرورت پاک کنی؟ این دستورات رو **به ترتیب** بزن:

```bash
# ۱. خاموش و غیرفعال‌کردن سرویس ۲۴ ساعته
systemctl stop userbot
systemctl disable userbot

# ۲. حذف فایل سرویس
rm -f /etc/systemd/system/userbot.service
systemctl daemon-reload

# ۳. حذف کامل ربات (کد، venv، سشن ورود، تنظیمات، دیتابیس)
cd ~
rm -rf 3outhboy-userbot
```

⚠️ **قدم ۳ همه‌چیز رو پاک می‌کنه** — شامل سشن ورودت (`my_account.session`) و تمام تنظیمات ربات (`userbot_db.json`).

### 🔐 مراحل امنیتی تکمیلی (خارج از سرور — پیشنهادی):

| قدم | چطوری |
|---|---|
| 🤖 **ابطال توکن ربات پنل** | به [@BotFather](https://t.me/BotFather) بزن `/revoke` (یا `/mybots` → رباتت → API Token → Revoke) |
| 📱 **قطع سشن از داخل تلگرام** | تنظیمات تلگرام → Devices → سشن سرور رو پیدا کن → **Terminate Session** |
| 🔑 **ساخت مجدد API** (اختیاری — خیلی امن) | [my.telegram.org](https://my.telegram.org) — اپ قبلی رو حذف و اپ جدید بساز |

> 💡 قطع کردن سشن از تنظیمات تلگرام **فوری کار می‌کنه** و حتی اگه فایل‌ها رو قبلاً پاک کرده باشی هم جواب می‌ده — موقع شک، همینو انجام بده.

بعد از این مراحل، هیچ اثری از ربات روی سرورت نمی‌مونه و همه‌ی دسترسی‌ها به اکانتت باطل شدن 🌸

---

## 🤝 مشارکت

باگ پیدا کردی؟ ایده‌ی باحالی داری؟ خوشحال می‌شیم [Issue](https://github.com/3OUTHBOY/3outhboy-userbot/issues) بزنی یا Pull Request بفرستی! 💜

---

## 📜 لایسنس

<div align="center">

**3OUTHBOY UserBot** تحت لایسنس
**[GNU General Public License v3.0](LICENSE)** منتشر شده 🍃

> «نرم‌افزار آزاد بحث آزادیه، نه قیمت.» — RMS

`🄯 3OUTHBOY — کاپی‌لفت، همه‌ی حقوق برعکس!`

استفاده کن. بشکن. بهترش کن. دوباره به اشتراک بذار. 💜

</div>

---

<div align="center">

**ساخته‌شده با 💜 برای جامعه‌ی تلگرام**

⭐ اگه خوشت اومد، به ریپو ستاره بده!

🌸 روزت پر از لبخند باشه 🌸

</div>
