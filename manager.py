# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════
#   🖥️  3OUTHBOY UserBot — Server Manager
#   Beautiful blue-themed terminal control panel
#   Works on: Ubuntu/Linux & Windows
# ═══════════════════════════════════════════════════════

import os
import sys
import json
import time
import shutil
import subprocess

IS_WIN = os.name == "nt"
IS_ROOT = True if IS_WIN else os.geteuid() == 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE = "userbot"
VENV_PY = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe") if IS_WIN \
    else os.path.join(BASE_DIR, "venv", "bin", "python")

# ═══════════════ 🎨 Colors (blue theme) ═══════════════
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

def colors_on():
    if IS_WIN:
        os.system("")

colors_on()

# ═══════════════ 🧰 Helpers ═══════════════

def clear():
    os.system("cls" if IS_WIN else "clear")

W = 52

def banner():
    clear()
    print()
    print(f"{BLUE}╔{'═' * W}╗{RESET}")
    mid = "⚡ 3OUTHBOY UserBot ⚡"
    pad = (W - len(mid)) // 2
    print(f"{BLUE}║{RESET}{' ' * pad}{BOLD}{CYAN}{mid}{RESET}{' ' * (W - pad - len(mid))}{BLUE}║{RESET}")
    print(f"{BLUE}╠{'═' * W}╣{RESET}")
    sub = "🖥 Server Manager Panel"
    pad2 = (W - len(sub)) // 2
    print(f"{BLUE}║{RESET}{' ' * pad2}{MAGENTA}{sub}{RESET}{' ' * (W - pad2 - len(sub))}{BLUE}║{RESET}")
    print(f"{BLUE}╚{'═' * W}╝{RESET}")
    py = f"{GREEN}✔ installed{RESET}" if os.path.exists(VENV_PY) else f"{RED}✖ not installed{RESET}"
    print(f"{DIM}   🌍  :{RESET} {CYAN}{'🪟 Windows' if IS_WIN else '🐧 Linux / Ubuntu'}{RESET}")
    print(f"{DIM}   📂  :{RESET} {DIM}{BASE_DIR}{RESET}")
    print(f"{DIM}   🐍  :{RESET} {py}")
    print(f"{DIM}   🕐  :{RESET} {time.strftime('%Y-%m-%d %H:%M')}")
    print(f"{BLUE}  {'─' * W}{RESET}")

def pause():
    input(f"\n  {DIM}⏸  Press Enter to return...{RESET}")

def ok(msg):    print(f"  {GREEN}✔ {msg}{RESET}")
def err(msg):   print(f"  {RED}✖ {msg}{RESET}")
def warn(msg):  print(f"  {YELLOW}⚠ {msg}{RESET}")

def confirm(q):
    return input(f"  {YELLOW}❓ {q}{RESET} {BOLD}(y/N):{RESET} ").strip().lower() == "y"

def header(title):
    print(f"\n  {BOLD}{BLUE}◈ {title}{RESET}")
    print(f"  {BLUE}{'─' * 44}{RESET}\n")

def spinner(text, secs=1.2):
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end = time.time() + secs
    i = 0
    while time.time() < end:
        print(f"\r  {CYAN}{frames[i % len(frames)]}{RESET} {text}   ", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 60 + "\r", end="")

# ═══════════════ ⚙️ Service helpers ═══════════════

def svc(action):
    if IS_WIN:
        warn("systemd services are Linux-only.")
        return False
    if not IS_ROOT:
        warn("Need root:  sudo python3 manager.py")
        return False
    r = subprocess.run(["systemctl", action, SERVICE], capture_output=True, text=True)
    return r.returncode == 0

def svc_status():
    if IS_WIN:
        return None
    r = subprocess.run(["systemctl", "is-active", SERVICE], capture_output=True, text=True)
    s = r.stdout.strip()
    if s == "active":
        return f"{GREEN}{BOLD}● Running{RESET} {GREEN}— bot is alive & healthy 🌿{RESET}"
    if s == "inactive":
        return f"{RED}{BOLD}● Stopped{RESET} {RED}— service is off{RESET}"
    if s == "failed":
        return f"{RED}{BOLD}✖ Crashed{RESET} {RED}— check logs (menu 6){RESET}"
    return f"{YELLOW}● {s or 'unknown'}{RESET}"

# ═══════════════ 📋 Actions ═══════════════

def action_status():
    banner()
    header("📊 STATUS")
    if IS_WIN:
        print(f"  🤖 Service: {BLUE}{BOLD}● Windows Mode{RESET} {DIM}— run bot via menu 2{RESET}")
    else:
        print(f"  🤖 Service: {svc_status()}\n")
        r = subprocess.run(["systemctl", "status", SERVICE, "--no-pager", "-l"],
                           capture_output=True, text=True)
        for ln in (r.stdout or "").splitlines():
            s = ln.strip()
            if s.startswith(("●", "Active:", "Main PID:")) or "bot.py" in s:
                print(f"  {DIM}{s}{RESET}")
        print()
    dbf = os.path.join(BASE_DIR, "userbot_db.json")
    if os.path.exists(dbf):
        try:
            with open(dbf, encoding="utf-8") as f:
                db = json.load(f)
            on = [k for k, v in db.items() if v is True]
            print(f"  {CYAN}🎛  Features ON :{RESET} {GREEN}{', '.join(on) if on else '—'}{RESET}")
            print(f"  {CYAN}📇  Replies    :{RESET} {len(db.get('user_replies', {}))} users")
            print(f"  {CYAN}📢  Fwd pairs  :{RESET} {len(db.get('fwd_pairs', []))}")
        except Exception:
            pass
    else:
        warn("userbot_db.json not found yet (bot never ran).")
    pause()

def action_foreground():
    banner()
    header("🚀 RUN IN FOREGROUND")
    if not os.path.exists(VENV_PY):
        err("venv missing — run installer first!")
        return pause()
    print(f"  {DIM}📱 First login? It asks phone + code (code arrives inside Telegram).{RESET}")
    print(f"  {DIM}🛑 Stop with Ctrl+C{RESET}\n")
    try:
        subprocess.run([VENV_PY, os.path.join(BASE_DIR, "bot.py")])
    except KeyboardInterrupt:
        pass
    pause()

def action_logs():
    banner()
    header("📜 LIVE LOGS")
    if IS_WIN:
        warn("journalctl is Linux-only. Use menu option 2 on Windows.")
    else:
        print(f"  {DIM}press Ctrl+C to exit{RESET}\n")
        try:
            subprocess.run(["journalctl", "-u", SERVICE, "-f", "--no-pager"])
        except KeyboardInterrupt:
            pass
    pause()

def action_update():
    banner()
    header("⬇️  UPDATE FROM GITHUB")
    spinner("Fetching updates...")
    r = subprocess.run(["git", "pull"], cwd=BASE_DIR, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    if "Already up to date" in out:
        ok("Already up to date! ✨")
    elif r.returncode == 0:
        ok("Code updated successfully.")
        if not IS_WIN and IS_ROOT and confirm("Restart service now?"):
            spinner("Restarting...")
            svc("restart")
            ok(f"Restarted → {svc_status()}")
        else:
            warn("Remember to restart the bot (menu 5).")
    else:
        err("git pull failed — check internet.")
        print(out)
    pause()

def action_session():
    banner()
    header("🔑 SESSION & CONFIG")
    sess = [f for f in os.listdir(BASE_DIR) if f.endswith(".session")]
    if sess:
        print(f"  {CYAN}📱 Sessions:{RESET}")
        for f in sess:
            kb = os.path.getsize(os.path.join(BASE_DIR, f)) // 1024
            print(f"     {GREEN}•{RESET} {f}  {DIM}({kb} KB){RESET}")
    else:
        print(f"  {CYAN}📱 Sessions:{RESET} {YELLOW}none (not logged in){RESET}")
    cfg = os.path.join(BASE_DIR, "config.py")
    if os.path.exists(cfg):
        print(f"  {CYAN}⚙️  config.py:{RESET} {GREEN}✓ exists{RESET}")
    else:
        print(f"  {CYAN}⚙️  config.py:{RESET} {RED}✖ missing{RESET}")
    print(f"\n  {BOLD}{BLUE}Options:{RESET}")
    print(f"   {MAGENTA}[1]{RESET} 🗑  Delete session  {DIM}(force re-login){RESET}")
    print(f"   {MAGENTA}[2]{RESET} 🔧  Reset config.py")
    print(f"   {MAGENTA}[3]{RESET} 🔙  Back")
    c = input(f"\n  {BOLD}{CYAN}Select [1-3]:{RESET} ").strip()
    if c == "1" and sess and confirm(f"Delete {len(sess)} session file(s)?"):
        for f in sess:
            os.remove(os.path.join(BASE_DIR, f))
        ok("Sessions deleted.")
    elif c == "2" and os.path.exists(cfg) and confirm("Reset config.py?"):
        os.remove(cfg)
        ok("Deleted. Re-run installer:  bash install.sh")
    pause()

def action_backup():
    banner()
    header("💾 BACKUP")
    bdir = os.path.join(BASE_DIR, "backups")
    os.makedirs(bdir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    bfile = os.path.join(bdir, f"backup_{stamp}.zip")
    import zipfile
    print(f"  {DIM}📦 Packing...{RESET}")
    targets = ["userbot_db.json", "config.py"]
    sess = [f for f in os.listdir(BASE_DIR) if f.endswith(".session")]
    with zipfile.ZipFile(bfile, "w") as z:
        for t in targets + sess:
            p = os.path.join(BASE_DIR, t)
            if os.path.exists(p):
                z.write(p, t)
                print(f"   {GREEN}+{RESET} {t}")
    ok(f"Backup saved → {DIM}{bfile}{RESET}")
    print(f"  {YELLOW}⚠  Contains session & secrets — keep it safe!{RESET}")
    pause()

def action_uninstall():
    banner()
    header("🧹 UNINSTALL")
    print(f"  {RED}{BOLD}This deletes EVERYTHING: service, sessions, config, files.{RESET}\n")
    print(f"  {DIM}After uninstall, in Telegram:{RESET}")
    print(f"   🤖 @BotFather → /revoke")
    print(f"   📱 Settings → Devices → Terminate this session\n")
    if not confirm(f"{RED}REALLY uninstall everything?{RESET}"):
        print(f"\n  {GREEN}😅 Cancelled — phew!{RESET}")
        return pause()
    if not confirm(f"{RED}FINAL — no going back. Continue?{RESET}"):
        print(f"\n  {GREEN}😅 Cancelled.{RESET}")
        return pause()
    if not IS_WIN:
        spinner("Removing service...")
        svc("stop")
        subprocess.run(["systemctl", "disable", SERVICE], capture_output=True)
        sp = f"/etc/systemd/system/{SERVICE}.service"
        if os.path.exists(sp):
            os.remove(sp)
        subprocess.run(["systemctl", "daemon-reload"], capture_output=True)
    spinner("Deleting files...")
    for item in os.listdir(BASE_DIR):
        if item in ("manager.py", ".git"):
            continue
        p = os.path.join(BASE_DIR, item)
        try:
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        except Exception:
            pass
    print()
    print(f"  {MAGENTA}{'═' * 44}{RESET}")
    print(f"  {MAGENTA}{BOLD}  🌸  Thank you for using 3OUTHBOY UserBot!{RESET}")
    print(f"  {CYAN}  ⭐  github.com/3OUTHBOY/3outhboy-userbot{RESET}")
    print(f"  {MAGENTA}{'═' * 44}{RESET}\n")
    input("  Press Enter to exit...")
    sys.exit(0)

def action_start():
    banner()
    header("▶️  START SERVICE")
    spinner("Starting...")
    if svc("start"):
        ok(f"Started → {svc_status()}")
    else:
        err("Failed — need sudo?")
    pause()

def action_stop():
    banner()
    header("⏹  STOP SERVICE")
    spinner("Stopping...")
    if svc("stop"):
        ok(f"Stopped → {svc_status()}")
    else:
        err("Failed — need sudo?")
    pause()

def action_restart():
    banner()
    header("🔄 RESTART SERVICE")
    spinner("Restarting...")
    if svc("restart"):
        ok(f"Restarted → {svc_status()}")
    else:
        err("Failed — need sudo?")
    pause()

# ═══════════════ 🖼 Main menu ═══════════════

def menu():
    banner()
    if IS_WIN:
        st = f"{BLUE}{BOLD}● Windows Mode{RESET} {DIM}— run bot via menu 2{RESET}"
    else:
        st = svc_status()
    print(f"  🤖 Service: {st}\n")
    print(f"  {BOLD}{BLUE}╔═[ 📋 MENU ]══════════════════════════════╗{RESET}")
    rows = [
        (" 1", "📊 Status",         "bot state & summary"),
        (" 2", "🚀 Run foreground", "start bot directly"),
        (" 3", "▶  Start",          "start background service"),
        (" 4", "⏹  Stop",           "stop background service"),
        (" 5", "🔄 Restart",        "restart the service"),
        (" 6", "📜 Logs",           "live logs (Ctrl+C to exit)"),
        (" 7", "⬇  Update",        "pull latest from GitHub"),
        (" 8", "🔑 Session & Config","manage login & config"),
        (" 9", "💾 Backup",         "zip sessions & settings"),
        ("10", "🧹 Uninstall",      "remove everything"),
        (" 0", "🚪 Exit",           "goodbye!"),
    ]
    for num, name, desc in rows:
        print(f"  {BLUE}║{RESET} {GREEN}{BOLD}[{num}]{RESET} {CYAN}{name:<19}{RESET}{DIM}{desc}{RESET} {BLUE}║{RESET}")
    print(f"  {BOLD}{BLUE}╚════════════════════════════════════════╝{RESET}")
    print()

def main():
    while True:
        menu()
        choice = input(f"  {BOLD}{CYAN}👉  Select:{RESET} ").strip()
        actions = {
            "1": action_status,
            "2": action_foreground,
            "3": action_start,
            "4": action_stop,
            "5": action_restart,
            "6": action_logs,
            "7": action_update,
            "8": action_session,
            "9": action_backup,
            "10": action_uninstall,
        }
        if choice == "0":
            print(f"\n  {MAGENTA}👋  Goodbye! Made with 💜{RESET}\n")
            break
        act = actions.get(choice)
        if act:
            act()
        else:
            warn("Invalid option.")
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {MAGENTA}👋  Goodbye!{RESET}\n")
