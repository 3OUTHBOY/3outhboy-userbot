⚡️ 3OUTHBOY UserBot
🎮 پنل مدیریت، شخصی‌سازی و خودکارسازی اکانت تلگرام

یوزربات پیشرفته با دو رابط: پنل ربات تلگرامی 🤖 + دستورات سریع در سیو‌مسیج 💬

PythonPyrogramLicense

✨ امکانات
دسته	قابلیت‌ها
👤 پروفایل	تغییر اسم، بیو، آیدی و عکس — همه با دستور
⏰ ساعت زنده	۲۰ استایل زیبا + منطقه زمانی هر کشور 🌍
🛡 مدیریت	بلاک / آنبلاک / سکوت کاربران در گروه
🔒 امنیت	قفل دو مرحله‌ای (2FA) + AutoSave مدیا
🟢 حضور	همیشه آنلاین + اکشن‌های فیک (تایپینگ...)
⚡️ تعامل	ریاکشن خودکار با ایموجی‌های دلخواه
🤖 منشی هوشمند	جواب اختصاصی برای هر شخص + فیلتر «فقط سلام»
📢 تبچی	فوروارد خودکار بین چت‌ها + تایمر یادآور
🎛 دو رابط	پنل ربات با دکمه‌های شیشه‌ای + کامندهای .
🧠 هوش مصنوعی	گفتگو با AI (اختیاری)
🚀 نصب روی سرور (Ubuntu 24.04)
# پیش‌نیازهاapt update && apt install python3 python3-pip python3-venv -y# دریافت پروژهgit clone https://github.com/USERNAME/REPO.gitcd REPO# نصب کتابخونه‌هاpython3 -m venv venvsource venv/bin/activatepip install -r requirements.txt# تنظیماتcp config.example.py config.pynano config.py# اجرا (بار اول شماره و کد تأیید می‌پرسه)python bot.py
🕐 اجرای دائمی ۲۴ ساعته (systemd)
bash

nano /etc/systemd/system/userbot.service
ini

[Unit]
Description=3OUTHBOY UserBot
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/root/REPO
ExecStart=/root/REPO/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
bash

systemctl daemon-reload
systemctl enable --now userbot
⚙️ تنظیمات (config.py)
متغیر
توضیح
از کجا؟
API_ID	شناسه اپلیکیشن	my.telegram.org
API_HASH	هش اپلیکیشن	my.telegram.org
BOT_TOKEN	توکن ربات پنل	@BotFather
OWNER_ID	آیدی عددی صاحب اکانت	@userinfobot
AI_API_KEY	کلید هوش مصنوعی (اختیاری)	openrouter.ai

📖 استفاده
بعد از اجرا، ربات پنل رو خودکار می‌فرسته:

چت با ربات پنل: /panel — منوی کامله با دکمه‌های شیشه‌ای 🎛
هر چتی (سیو‌مسیج و...): .panel — دستورات سریع با نقطه
فقط OWNER_ID می‌تونه به ربات فرمان بده — بقیه بلاک هستن 🔒

⚠️ هشدارها
استفاده از یوزربات ممکنه با قوانین تلگرام در تعارض باشه — مسئولیت استفاده با خودته
قابلیت‌های خودکار (ریاکشن، تبچی) رو معقول استفاده کن تا اکانت محدود نشه
فایل‌های .session و config.py مثل رمز اکانتت هستن — هرگز به اشتراک نذار!
🤝 مشارکت
پیشنهاد یا باگ داری؟ Issue بزن یا Pull Request بفرشت! 💜

📜 لایسنس
این پروژه تحت لایسنس GPL-3.0 منتشر شده.

<div align="center">

🌸 روزت پر از لبخند باشه 🌸

</div>
```