# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#   🖥️  3OUTHBOY UserBot — Server Manager
#   A beautiful interactive management panel
#   Works on: Ubuntu/Linux & Windows
# ═══════════════════════════════════════════════════════

import os
import sys
import subprocess
import shutil
import time

IS_WIN = os.name == "nt"
IS_ROOT = not IS_WIN and os.geteuid() == 0 if not IS_WIN else True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE = "userbot"
VENV_PY = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe") if IS_WIN \
    else os.path.join(BASE_DIR, "venv", "bin", "python")

# ═══════════════ UI helpers ═══════════════

def clear():
    os.system("cls" if IS_WIN else "clear")

def line(char="═", n=50):
    return char * n

def banner():
    clear()
    print(f"""
{line()}
     ⚡️  3OUTHBOY UserBot — Manager  ⚡️
{line()}
   🌍 Platform: {'Windows' if IS_WIN else 'Linux/Ubuntu'}
   📂 Folder:   {BASE_DIR}
   🐍 Python:   {VENV_PY if os.path.exists(VENV_PY) else '❌ Not installed'}
   🕐 Time:     {time.strftime('%Y-%m-%d %H:%M:%S')}
{line()}
""")

def pause():
    input("\n  ⏸  Press Enter to return to menu... ")

def ok(msg):
    print(f"  ✅ {msg}")

def err(msg):
    print(f"  ❌ {msg}")

def warn(msg):
    print(f"  ⚠️  {msg}")

def confirm(question):
    return input(f"  ❓ {question} (y/N): ").strip().lower() == "y"

# ═══════════════ core actions ═══════════════

def svc(action):
    """systemctl wrapper (Linux only)."""
    if IS_WIN:
        warn("Systemd services are not available on Windows.")
        return False
    if not IS_ROOT:
        warn("Need root access. Try:  sudo python manager.py")
        return False
    r = subprocess.run(["systemctl", action, SERVICE],
                       capture_output=True, text=True)
    return r.returncode == 0

def svc_status():
    if IS_WIN:
        return "❌ (service mode is Linux-only)"
    r = subprocess.run(["systemctl", "is-active", SERVICE],
                       capture_output=True, text=True)
    state = r.stdout.strip()
    return {"active": "🟢 RUNNING", "inactive": "🔴 STOPPED",
            "failed": "💥 FAILED"}.get(state, f"⚪ {state or 'unknown'}")

def run_bot_interactive():
    """Run bot.py directly (foreground, for first login / debug)."""
    if not os.path.exists(VENV_PY):
        err("venv not found! Run the installer first (bash install.sh).")
        return
    print(f"""
{line('─')}
  🚀 Starting bot in foreground mode...
  📱 First time? It will ask for your phone number & login code.
  🛑 To stop: press Ctrl+C
{line('─')}
""")
    try:
        subprocess.run([VENV_PY, os.path.join(BASE_DIR, "bot.py")])
    except KeyboardInterrupt:
        print("\n  🛑 Bot stopped.")

# ═══════════════ menu actions ═══════════════

def action_status():
    banner()
    print(f"  🤖 Bot service: {svc_status()}\n")
    if not IS_WIN:
        r = subprocess.run(["systemctl", "status", SERVICE, "--no-pager", "-l"],
                           capture_output=True, text=True)
        # show only the important lines
        for ln in (r.stdout or "").splitlines():
            s = ln.strip()
            if s.startswith(("●", "Active:", "Main PID:", "CGroup:")) or "python bot.py" in s:
                print("  " + s)
        print()
    # db summary
    dbf = os.path.join(BASE_DIR, "userbot_db.json")
    if os.path.exists(dbf):
        try:
            import json
            with open(dbf, encoding="utf-8") as f:
                db = json.load(f)
            on = [k for k, v in db.items() if v is True]
            print(f"  🎛 Enabled features: {', '.join(on) if on else 'none'}")
            print(f"  📇 Custom replies: {len(db.get('user_replies', {}))} users")
            print(f"  📢 Forwarder pairs: {len(db.get('fwd_pairs', []))}")
        except Exception:
            pass
    else:
        warn("userbot_db.json not found (bot hasn't run yet).")
    pause()

def action_logs():
    banner()
    if IS_WIN:
        warn("Live logs via journalctl are Linux-only.")
        warn("On Windows, run the bot in foreground (menu option 2) to see logs.")
    else:
        print(f"""
{line('─')}
  📜 Live logs — press Ctrl+C to exit
{line('─')}
""")
        try:
            subprocess.run(["journalctl", "-u", SERVICE, "-f", "--no-pager"])
        except KeyboardInterrupt:
            print("\n  📜 Logs closed.")
    pause()

def action_start():
    banner()
    if svc("start"):
        ok(f"Bot service started → {svc_status()}")
    else:
        err("Failed to start service.")
        warn("Try:  sudo python manager.py")
    pause()

def action_stop():
    banner()
    if svc("stop"):
        ok(f"Bot service stopped → {svc_status()}")
    pause()

def action_restart():
    banner()
    if svc("restart"):
        ok(f"Bot restarted → {svc_status()}")
    else:
        err("Failed to restart service.")
    pause()

def action_foreground():
    banner()
    run_bot_interactive()
    pause()

def action_update():
    banner()
    print(f"""
{line('─')}
  🔄 Updating 3OUTHBOY UserBot from GitHub...
{line('─')}
""")
    r = subprocess.run(["git", "pull"], cwd=BASE_DIR,
                       capture_output=True, text=True)
    print(r.stdout or r.stderr)
    if "Already up to date" in (r.stdout + r.stderr):
        ok("Already up to date! ✨")
    elif r.returncode == 0:
        ok("Code updated.")
        if not IS_WIN and IS_ROOT:
            if confirm("Restart the bot service now?"):
                svc("restart")
                ok(f"Bot restarted → {svc_status()}")
        else:
            warn("Don't forget to restart the bot (menu option 5).")
    else:
        err("Git pull failed — check your internet / repository.")
    pause()

def action_session():
    banner()
    print(f"""
{line('─')}
  🔑 Session & Config Manager
{line('─')}
""")
    sess = [f for f in os.listdir(BASE_DIR) if f.endswith(".session")]
    if sess:
        print("  📱 Found session files:")
        for f in sess:
            kb = os.path.getsize(os.path.join(BASE_DIR, f)) // 1024
            print(f"     • {f}  ({kb} KB)")
    else:
        print("  📱 No session files found (bot not logged in).")
    print()
    cfg = os.path.join(BASE_DIR, "config.py")
    print(f"  ⚙️  config.py: {'✅ exists' if os.path.exists(cfg) else '❌ missing'}")
    print("""
  What do you want to do?
  [1] 🗑  Delete session (log out & force re-login next start)
  [2] 🔧 Reset config.py (re-enter credentials)
  [3] 🔙  Back
""")
    c = input("  Select [1-3]: ").strip()
    if c == "1":
        if sess and confirm(f"Delete {len(sess)} session file(s)? You'll need to re-login!"):
            for f in sess:
                os.remove(os.path.join(BASE_DIR, f))
            ok("Sessions deleted.")
    elif c == "2":
        if os.path.exists(cfg) and confirm("Reset config.py?"):
            os.remove(cfg)
            ok("config.py deleted.")
            if not IS_WIN:
                print("  💡 Run the installer again:  bash install.sh")
            else:
                print("  💡 Copy config.example.py to config.py and edit it.")
    pause()

def action_backup():
    banner()
    bdir = os.path.join(BASE_DIR, "backups")
    os.makedirs(bdir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    bfile = os.path.join(bdir, f"backup_{stamp}.zip")
    print(f"""
{line('─')}
  💾 Backup Manager — creates a zip of your data
{line('─')}
""")
    import zipfile
    targets = ["userbot_db.json", "config.py"]
    sess = [f for f in os.listdir(BASE_DIR) if f.endswith(".session")]
    with zipfile.ZipFile(bfile, "w") as z:
        for t in targets:
            p = os.path.join(BASE_DIR, t)
            if os.path.exists(p):
                z.write(p, t)
                print(f"  + {t}")
        for f in sess:
            z.write(os.path.join(BASE_DIR, f), f)
            print(f"  + {f}")
    ok(f"Backup saved: {bfile}")
    print("  💡 Keep this file safe — it contains your login session & secrets!")
    pause()

def action_uninstall():
    banner()
    print(f"""
{line('─')}
  🧹 Uninstall — removes 3OUTHBOY UserBot completely
{line('─')}
""")
    warn("This will delete: service, sessions, config, database, all files!")
    print("""
  ⚠️  Recommended outside steps (do these in Telegram after):
     🤖 @BotFather → /revoke  (kill the panel bot token)
     📱 Telegram Settings → Devices → Terminate this session
""")
    if not confirm("Are you REALLY sure you want to uninstall?"):
        print("\n  😅 Phew! Uninstall cancelled.")
        pause()
        return
    if not confirm("FINAL CONFIRMATION — everything will be gone. Continue?"):
        print("\n  😅 Cancelled.")
        pause()
        return

    if not IS_WIN:
        svc("stop")
        subprocess.run(["systemctl", "disable", SERVICE], capture_output=True)
        sp = f"/etc/systemd/system/{SERVICE}.service"
        if os.path.exists(sp):
            os.remove(sp)
        subprocess.run(["systemctl", "daemon-reload"], capture_output=True)
        print("  🧹 Service removed.")

    print("  🧹 Deleting files...")
    pause_marker = os.path.join(BASE_DIR, ".manager_keep")
    with open(pause_marker, "w") as f:
        f.write("temp")
    # delete everything except manager itself & marker
    for item in os.listdir(BASE_DIR):
        if item in ("manager.py", ".manager_keep", ".git"):
            continue
        p = os.path.join(BASE_DIR, item)
        try:
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        except Exception:
            pass
    os.remove(pause_marker)
    ok("Everything deleted!")
    print("""
{line('✿')}
   🌸 Thank you for using 3OUTHBOY UserBot!
   🌟 Star the repo if you enjoyed it:
      github.com/3OUTHBOY/3outhboy-userbot
{line('✿')}
""")
    input("  Press Enter to exit... ")
    sys.exit(0)

# ═══════════════ main menu ═══════════════

MENU = """
  📋 MAIN MENU
  ─────────────────────────────────────────────────
   [ 1] 📊 Status        — bot state & quick summary
   [ 2] 🚀 Run foreground — start bot directly / first login
   [ 3] ▶️  Start        — start background service
   [ 4] ⏹  Stop         — stop background service
   [ 5] 🔄 Restart       — restart (after code changes)
   [ 6] 📜 Logs          — live logs (journalctl)
   [ 7] ⬇️  Update       — pull latest code from GitHub
   [ 8] 🔑 Session/Config— manage login & credentials
   [ 9] 💾 Backup        — save sessions/settings to a zip
  [10] 🧹 Uninstall      — remove everything completely
   [ 0] 🚪 Exit
  ─────────────────────────────────────────────────
"""

ACTIONS = {
    "1": action_status, "2": action_foreground, "3": action_start,
    "4": action_stop, "5": action_restart, "6": action_logs,
    "7": action_update, "8": action_session, "9": action_backup,
    "10": action_uninstall,
}

def main():
    while True:
        banner()
        state = svc_status() if not IS_WIN else "🖥 Windows mode"
        print(f"  🤖 Service status: {state}\n")
        print(MENU)
        choice = input("  👉 Select an option: ").strip()
        if choice == "0":
            print("\n  👋 Goodbye! Made with 💜\n")
            break
        act = ACTIONS.get(choice)
        if act:
            act()
        else:
            warn("Invalid option — try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 Goodbye!\n")
