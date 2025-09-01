# Created by: https://github.com/HamidYaraliOfficial
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import threading
import os
import zipfile
import random
import shutil
import sqlite3
import string
import time

api_id = 12345678 #اپی ایدی
api_hash = "hash" #اپی هش
bot_token = "token" #توکن ربات
OWNER_ID = 6391226739 #ایدی عددی مالک

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

running_processes = {}
output_handles = {}
files_store = {}
user_state = {}
ui_state = {}
pending_delete = {}
interactive_sessions = {}
pending_input = {}

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS files (
    code_id TEXT PRIMARY KEY,
    file_path TEXT,
    folder_path TEXT
)
""")
conn.commit()

def generate_code_id():
    while True:
        cid = str(random.randint(1000, 9999))
        cur.execute("SELECT 1 FROM files WHERE code_id=?", (cid,))
        if not cur.fetchone():
            return cid

def save_file(code_id, file_path, folder):
    cur.execute("INSERT OR REPLACE INTO files VALUES (?, ?, ?)", (code_id, file_path, folder))
    conn.commit()

def remove_file_record(code_id):
    cur.execute("DELETE FROM files WHERE code_id=?", (code_id,))
    conn.commit()

def load_files():
    cur.execute("SELECT code_id, file_path, folder_path FROM files")
    return cur.fetchall()

def is_running(proc):
    try:
        return proc and (proc.poll() is None)
    except Exception:
        return False

def cleanup_folder(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

def human_welcome(lang="fa"):
    if lang == "en":
        return (
            "✨ Welcome to the world of smart Python code execution!\n\n"
            "I'm here to run your code with minimal hassle, install libraries, send outputs, "
            "and even show you the live status of your running code. 🚀\n"
            "Each code gets a unique 'personal code' to keep everything organized and traceable. "
            "You can cancel execution, view outputs, rerun, or delete code files with a tap. 🧹\n\n"
            "Start with the buttons below and enjoy a neat, fast, and friendly bot! 😎🤝"
        )
    elif lang == "zh":
        return (
            "✨ 欢迎体验智能 Python 代码执行！\n\n"
            "我可以帮你轻松运行代码，安装库，发送输出，"
            "甚至实时显示代码运行状态。🚀\n"
            "每段代码都有一个唯一的“个人代码”，让一切井然有序且可追踪。"
            "你可以随时取消执行、查看输出、重新运行或一键删除代码文件。🧹\n\n"
            "点击下面的按钮开始，享受一个整洁、快速且友好的机器人！😎🤝"
        )
    elif lang == "ru":
        return (
            "✨ Добро пожаловать в мир умного выполнения кода на Python!\n\n"
            "Я здесь, чтобы запускать ваш код с минимальными усилиями, устанавливать библиотеки, отправлять результаты "
            "и даже показывать статус выполнения кода в реальном времени. 🚀\n"
            "Каждый код получает уникальный «личный код» для порядка и отслеживания. "
            "Вы можете прервать выполнение, просмотреть результаты, перезапустить или удалить файлы кода одним касанием. 🧹\n\n"
            "Начните с кнопок ниже и наслаждайтесь удобным, быстрым и дружелюбным ботом! 😎🤝"
        )
    return (
        "✨ به دنیای اجرای هوشمند کد پایتون خوش اومدی!\n\n"
        "من اینجام تا کد‌هات رو با کمترین دردسر اجرا کنم، کتابخونه نصب کنم، خروجی‌ها رو برات بفرستم، "
        "و حتی وضعیت اجرای زندهٔ کدهات رو لحظه‌ای نشونت بدم. 🚀\n"
        "هر کد یه «کد شخصی» مخصوص خودش داره تا همه‌چیز مرتب و قابل پیگیری باشه. "
        "می‌تونی هر زمان اجرا رو لغو کنی، خروجی رو ببینی، دوباره اجرا کنی یا حتی فایل‌های مربوط به یه کد رو با یه لمس پاک کنی. 🧹\n\n"
        "با دکمه‌های زیر شروع کن و از تجربه‌ی یک ربات مرتب، سریع و خوش‌برخورد لذت ببر! 😎🤝"
    )

def main_menu(lang="fa"):
    if lang == "en":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Submit personal code & file ✅", callback_data="run")],
            [InlineKeyboardButton("Run code ▶️", callback_data="rerun"),
             InlineKeyboardButton("Cancel execution ❌", callback_data="cancel")],
            [InlineKeyboardButton("View output 📄", callback_data="output"),
             InlineKeyboardButton("Active codes ⚡️", callback_data="active_codes")],
            [InlineKeyboardButton("Install library 📦", callback_data="install"),
             InlineKeyboardButton("Terminal 🖥", callback_data="terminal")],
            [InlineKeyboardButton("English 🇬🇧", callback_data="lang:en"),
             InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang:fa"),
             InlineKeyboardButton("中文 🇨🇳", callback_data="lang:zh"),
             InlineKeyboardButton("Русский 🇷🇺", callback_data="lang:ru")]
        ])
    elif lang == "zh":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("提交个人代码和文件 ✅", callback_data="run")],
            [InlineKeyboardButton("运行代码 ▶️", callback_data="rerun"),
             InlineKeyboardButton("取消执行 ❌", callback_data="cancel")],
            [InlineKeyboardButton("查看输出 📄", callback_data="output"),
             InlineKeyboardButton("活跃代码 ⚡️", callback_data="active_codes")],
            [InlineKeyboardButton("安装库 📦", callback_data="install"),
             InlineKeyboardButton("终端 🖥", callback_data="terminal")],
            [InlineKeyboardButton("English 🇬🇧", callback_data="lang:en"),
             InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang:fa"),
             InlineKeyboardButton("中文 🇨🇳", callback_data="lang:zh"),
             InlineKeyboardButton("Русский 🇷🇺", callback_data="lang:ru")]
        ])
    elif lang == "ru":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Отправить личный код и файл ✅", callback_data="run")],
            [InlineKeyboardButton("Запустить код ▶️", callback_data="rerun"),
             InlineKeyboardButton("Отменить выполнение ❌", callback_data="cancel")],
            [InlineKeyboardButton("Просмотреть вывод 📄", callback_data="output"),
             InlineKeyboardButton("Активные коды ⚡️", callback_data="active_codes")],
            [InlineKeyboardButton("Установить библиотеку 📦", callback_data="install"),
             InlineKeyboardButton("Терминал 🖥", callback_data="terminal")],
            [InlineKeyboardButton("English 🇬🇧", callback_data="lang:en"),
             InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang:fa"),
             InlineKeyboardButton("中文 🇨🇳", callback_data="lang:zh"),
             InlineKeyboardButton("Русский 🇷🇺", callback_data="lang:ru")]
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("دادن کد شخصی و ارسال فایل ✅", callback_data="run")],
        [InlineKeyboardButton("اجرای کد ▶️", callback_data="rerun"),
         InlineKeyboardButton("لغو اجرا ❌", callback_data="cancel")],
        [InlineKeyboardButton("دیدن خروجی 📄", callback_data="output"),
         InlineKeyboardButton("کدهای فعال ⚡️", callback_data="active_codes")],
        [InlineKeyboardButton("نصب کتابخانه 📦", callback_data="install"),
         InlineKeyboardButton("ترمینال 🖥", callback_data="terminal")],
        [InlineKeyboardButton("English 🇬🇧", callback_data="lang:en"),
         InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang:fa"),
         InlineKeyboardButton("中文 🇨🇳", callback_data="lang:zh"),
         InlineKeyboardButton("Русский 🇷🇺", callback_data="lang:ru")]
    ])

def back_menu(lang="fa"):
    if lang == "en":
        return InlineKeyboardMarkup([[InlineKeyboardButton("Back ⬅️", callback_data="back")]])
    elif lang == "zh":
        return InlineKeyboardMarkup([[InlineKeyboardButton("返回 ⬅️", callback_data="back")]])
    elif lang == "ru":
        return InlineKeyboardMarkup([[InlineKeyboardButton("Назад ⬅️", callback_data="back")]])
    return InlineKeyboardMarkup([[InlineKeyboardButton("بازگشت ⬅️", callback_data="back")]])

def confirmation_menu(code_id, lang="fa"):
    if lang == "en":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes ✅", callback_data=f"confirm_delete:{code_id}:yes")],
            [InlineKeyboardButton("No ⛔️", callback_data=f"confirm_delete:{code_id}:no")],
            [InlineKeyboardButton("Back ⬅️", callback_data="back")]
        ])
    elif lang == "zh":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("是 ✅", callback_data=f"confirm_delete:{code_id}:yes")],
            [InlineKeyboardButton("否 ⛔️", callback_data=f"confirm_delete:{code_id}:no")],
            [InlineKeyboardButton("返回 ⬅️", callback_data="back")]
        ])
    elif lang == "ru":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Да ✅", callback_data=f"confirm_delete:{code_id}:yes")],
            [InlineKeyboardButton("Нет ⛔️", callback_data=f"confirm_delete:{code_id}:no")],
            [InlineKeyboardButton("Назад ⬅️", callback_data="back")]
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بله ✅", callback_data=f"confirm_delete:{code_id}:yes")],
        [InlineKeyboardButton("خیر ⛔️", callback_data=f"confirm_delete:{code_id}:no")],
        [InlineKeyboardButton("بازگشت ⬅️", callback_data="back")]
    ])

def active_codes_keyboard():
    active_ids = []
    for cid, proc in list(running_processes.items()):
        if is_running(proc):
            active_ids.append(cid)
        else:
            running_processes.pop(cid, None)
            fh = output_handles.pop(cid, None)
            try:
                if fh: fh.close()
            except Exception:
                pass
    if not active_ids:
        return None
    rows = []
    row = []
    for i, cid in enumerate(sorted(active_ids)):
        row.append(InlineKeyboardButton(cid, callback_data=f"active_code:{cid}"))
        if (i + 1) % 3 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("بازگشت ⬅️", callback_data="back")])
    return InlineKeyboardMarkup(rows)

def execute_code(file_path, code_id, chat_id, interactive=False):
    folder = str(code_id)
    os.makedirs(folder, exist_ok=True)
    file_name = os.path.basename(file_path)
    new_path = os.path.join(folder, file_name)
    if os.path.abspath(file_path) != os.path.abspath(new_path):
        try:
            shutil.copy2(file_path, new_path)
        except Exception as e:
            try:
                app.send_message(chat_id, f"Error copying file: {e}", reply_markup=back_menu())
            except Exception:
                pass
            return
    save_file(code_id, new_path, folder)
    files_store[code_id] = new_path
    script_to_run = file_name
    if interactive:
        try:
            proc = subprocess.Popen(
                ["python", "-u", script_to_run],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                cwd=folder,
                text=True,
                bufsize=1
            )
        except Exception as e:
            app.send_message(chat_id, f"Error starting terminal: {e}", reply_markup=back_menu())
            return
        running_processes[code_id] = proc
        interactive_sessions[code_id] = {"chat_id": chat_id, "proc": proc, "awaiting": False, "buffer": ""}
        def reader():
            try:
                for line in iter(proc.stdout.readline, ""):
                    text = line.rstrip("\r\n")
                    if text:
                        try:
                            app.send_message(chat_id, "📥 " + text)
                        except Exception:
                            pass
                    tail = text.rstrip()
                    prompt_like = False
                    if tail:
                        last = tail[-1]
                        if last in [":", "?", "؟", ">"]:
                            prompt_like = True
                    low = tail.lower()
                    if any(k in low for k in ["enter", "password", "passcode", "code", "phone", "login", "otp", "شماره", "کد", "رمز", "گذرواژه"]):
                        prompt_like = True
                    if prompt_like and not interactive_sessions.get(code_id, {}).get("awaiting"):
                        interactive_sessions[code_id]["awaiting"] = True
                        pending_input[chat_id] = code_id
                        try:
                            app.send_message(chat_id, f"✍️ The program is waiting for input. Please send the required value for personal code {code_id}.")
                        except Exception:
                            pass
            except Exception:
                pass
            finally:
                interactive_sessions.pop(code_id, None)
                running_processes.pop(code_id, None)
                if pending_input.get(chat_id) == code_id:
                    pending_input.pop(chat_id, None)
        threading.Thread(target=reader, daemon=True).start()
    else:
        output_file = os.path.join(folder, "output.txt")
        f = open(output_file, "w", encoding="utf-8", buffering=1)
        try:
            proc = subprocess.Popen(
                ["python", script_to_run],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=folder
            )
        except Exception as e:
            f.write(f"\n[Error running code]: {e}\n")
            f.flush()
            f.close()
            return
        running_processes[code_id] = proc
        output_handles[code_id] = f
        def monitor_process():
            try:
                proc.wait()
            finally:
                fh = output_handles.pop(code_id, None)
                try:
                    if fh: fh.close()
                except Exception:
                    pass
                running_processes.pop(code_id, None)
        threading.Thread(target=monitor_process, daemon=True).start()

def stop_process(code_id):
    proc = running_processes.get(code_id)
    if not proc:
        return False
    try:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
    except Exception:
        pass
    finally:
        running_processes.pop(code_id, None)
    return True

def install_library(lib_name, chat_id):
    try:
        proc = subprocess.Popen(
            ["python", "-m", "pip", "install", lib_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        output, _ = proc.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        output = "Installation timed out."
    except Exception as e:
        output = f"Error installing: {e}"
    app.send_message(chat_id, "Installation result:\n" + (output[-3500:] if output else "Completed"), reply_markup=back_menu())

@app.on_message(filters.command("start"))
def start(client, message):
    if message.from_user.id != OWNER_ID:
        return
    lang = user_state.get(message.from_user.id, {}).get("lang", "fa")
    sent = message.reply_text(human_welcome(lang), reply_markup=main_menu(lang))
    ui_state[message.from_user.id] = sent.id

@app.on_callback_query()
def callback_query(client, cq):
    if cq.from_user.id != OWNER_ID:
        return
    user_id = cq.from_user.id
    ui_state[user_id] = cq.message.id
    data = cq.data
    lang = user_state.get(user_id, {}).get("lang", "fa")
    if data.startswith("lang:"):
        new_lang = data.split(":", 1)[1]
        user_state[user_id] = {"lang": new_lang}
        cq.message.edit_text(human_welcome(new_lang), reply_markup=main_menu(new_lang))
    elif data == "run":
        user_state[user_id] = {"state": "await_code", "lang": lang}
        text = "Please send your file or code (.py or .zip)." if lang == "en" else \
               "请发送您的文件或代码（.py 或 .zip）。" if lang == "zh" else \
               "Отправьте ваш файл или код (.py или .zip)." if lang == "ru" else \
               "فایل یا کد خود را ارسال کنید (پسوند .py یا .zip)."
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "install":
        user_state[user_id] = {"state": "await_library", "lang": lang}
        text = "Send the name of the library (e.g., requests):" if lang == "en" else \
               "发送库的名称（例如：requests）：" if lang == "zh" else \
               "Отправьте название библиотеки (например, requests):" if lang == "ru" else \
               "نام کتابخانهٔ موردنظر را بفرستید (مثلاً: requests):"
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "terminal":
        user_state[user_id] = {"state": "await_terminal", "lang": lang}
        text = "Send the personal code of the file to run in terminal:" if lang == "en" else \
               "发送要在终端运行的文件的个人代码：" if lang == "zh" else \
               "Отправьте личный код файла для запуска в терминале:" if lang == "ru" else \
               "کد شخصی فایل را برای اجرای ترمینال ارسال کنید:"
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "cancel":
        user_state[user_id] = {"state": "await_cancel", "lang": lang}
        text = "Send the personal code of the file to stop execution:" if lang == "en" else \
               "发送要停止执行的文件的个人代码：" if lang == "zh" else \
               "Отправьте личный код файла для остановки выполнения:" if lang == "ru" else \
               "کد شخصی فایل را برای توقف اجرا ارسال کنید:"
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "rerun":
        user_state[user_id] = {"state": "await_rerun", "lang": lang}
        text = "Send the personal code of the file to rerun:" if lang == "en" else \
               "发送要重新运行的文件的个人代码：" if lang == "zh" else \
               "Отправьте личный код файла для повторного запуска:" if lang == "ru" else \
               "کد شخصی فایل را برای اجرای دوباره ارسال کنید:"
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "output":
        user_state[user_id] = {"state": "await_output", "lang": lang}
        text = "Send the personal code of the file to get output:" if lang == "en" else \
               "发送要获取输出的文件的个人代码：" if lang == "zh" else \
               "Отправьте личный код файла для получения вывода:" if lang == "ru" else \
               "کد شخصی فایل را برای دریافت خروجی ارسال کنید:"
        cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "active_codes":
        kb = active_codes_keyboard()
        if kb is None:
            text = "No code is currently running." if lang == "en" else \
                   "当前没有代码在运行。" if lang == "zh" else \
                   "В настоящее время ни один код не выполняется." if lang == "ru" else \
                   "در حال حاضر هیچ کدی در حال اجرا نیست."
            cq.message.edit_text(text, reply_markup=back_menu(lang))
        else:
            text = "Running codes (tap a code to get its file):" if lang == "en" else \
                   "正在运行的代码（点击代码获取文件）：" if lang == "zh" else \
                   "Выполняющиеся коды (нажмите на код, чтобы получить файл):" if lang == "ru" else \
                   "کدهای در حال اجرا (برای دریافت فایل روی کد دلخواه لمس کنید):"
            cq.message.edit_text(text, reply_markup=kb)
    elif data.startswith("active_code:"):
        code_id = data.split(":", 1)[1]
        if code_id in running_processes and is_running(running_processes[code_id]):
            cur.execute("SELECT file_path FROM files WHERE code_id = ?", (code_id,))
            row = cur.fetchone()
            if row and os.path.exists(row[0]):
                try:
                    app.send_document(cq.message.chat.id, row[0], caption=f"File for personal code: {code_id}" if lang == "en" else \
                                                             f"个人代码的文件：{code_id}" if lang == "zh" else \
                                                             f"Файл для личного кода: {code_id}" if lang == "ru" else \
                                                             f"فایل مربوط به کد شخصی: {code_id}")
                except Exception:
                    text = "Failed to send file." if lang == "en" else \
                           "发送文件失败。" if lang == "zh" else \
                           "Не удалось отправить файл." if lang == "ru" else \
                           "ارسال فایل با مشکل مواجه شد."
                    app.send_message(cq.message.chat.id, text)
            else:
                text = "File not found." if lang == "en" else \
                       "未找到文件。" if lang == "zh" else \
                       "Файл не найден." if lang == "ru" else \
                       "فایل یافت نشد."
                app.send_message(cq.message.chat.id, text)
            kb = active_codes_keyboard()
            if kb is None:
                text = "No other code is running." if lang == "en" else \
                       "没有其他代码在运行。" if lang == "zh" else \
                       "Другие коды не выполняются." if lang == "ru" else \
                       "هیچ کدی دیگر در حال اجرا نیست."
                cq.message.edit_text(text, reply_markup=back_menu(lang))
            else:
                text = "Running codes:" if lang == "en" else \
                       "正在运行的代码：" if lang == "zh" else \
                       "Выполняющиеся коды:" if lang == "ru" else \
                       "کدهای در حال اجرا:"
                cq.message.edit_text(text, reply_markup=kb)
        else:
            text = "This code is no longer running." if lang == "en" else \
                   "此代码已不再运行。" if lang == "zh" else \
                   "Этот код больше не выполняется." if lang == "ru" else \
                   "این کد دیگر در حال اجرا نیست."
            cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data.startswith("confirm_delete:"):
        _, code_id, decision = data.split(":")
        pending_delete.pop(user_id, None)
        if decision == "yes":
            cur.execute("SELECT folder_path FROM files WHERE code_id = ?", (code_id,))
            row = cur.fetchone()
            if row:
                folder = row[0]
                cleanup_folder(folder)
            files_store.pop(code_id, None)
            remove_file_record(code_id)
            text = "All files for this code have been deleted. ⚠️ Note: This personal code can no longer be used." if lang == "en" else \
                   "此代码的所有文件已删除。⚠️ 注意：此个人代码无法再次使用。" if lang == "zh" else \
                   "Все файлы для этого кода удалены. ⚠️ Примечание: Этот личный код больше нельзя использовать." if lang == "ru" else \
                   "تمام فایل‌های مربوط به این کد حذف شد. ⚠️ توجه: با این کد شخصی دیگر قابل اجرا نیست."
            cq.message.edit_text(text, reply_markup=back_menu(lang))
        else:
            text = "Files were not deleted and can be used for rerun. ✅" if lang == "en" else \
                   "文件未被删除，可用于重新运行。✅" if lang == "zh" else \
                   "Файлы не были удалены и могут быть использованы для повторного запуска. ✅" if lang == "ru" else \
                   "فایل‌ها حذف نشدند و برای اجرای دوباره قابل استفاده هستند. ✅"
            cq.message.edit_text(text, reply_markup=back_menu(lang))
    elif data == "back":
        if user_id in user_state:
            lang = user_state[user_id].get("lang", "fa")
            user_state.pop(user_id, None)
        cq.message.edit_text(human_welcome(lang), reply_markup=main_menu(lang))

@app.on_message(filters.private)
def handle_message(client, message):
    if message.from_user.id != OWNER_ID:
        return
    user_id = message.from_user.id
    state_dict = user_state.get(user_id, {})
    state = state_dict.get("state")
    lang = state_dict.get("lang", "fa")
    if state == "await_terminal":
        code_id = (message.text or "").strip()
        cur.execute("SELECT file_path FROM files WHERE code_id = ?", (code_id,))
        row = cur.fetchone()
        if not row:
            text = "Code not found." if lang == "en" else \
                   "未找到代码。" if lang == "zh" else \
                   "Код не найден." if lang == "ru" else \
                   "کد پیدا نشد."
            message.reply_text(text, reply_markup=back_menu(lang))
        else:
            stop_process(code_id)
            for cid, sess in list(interactive_sessions.items()):
                if sess.get("chat_id") == message.chat.id and cid != code_id:
                    try:
                        stop_process(cid)
                    except Exception:
                        pass
                    interactive_sessions.pop(cid, None)
            threading.Thread(target=execute_code, args=(row[0], code_id, message.chat.id, True), daemon=True).start()
            text = "Terminal activated. Send input here whenever the program asks." if lang == "en" else \
                   "终端已激活。程序需要输入时，请在此发送。" if lang == "zh" else \
                   "Терминал активирован. Отправляйте ввод здесь, когда программа запросит." if lang == "ru" else \
                   "ترمینال فعال شد. هر زمان برنامه ورودی خواست، پاسخ را همینجا ارسال کنید."
            message.reply_text(text, reply_markup=back_menu(lang))
        user_state.pop(user_id, None)
        return
    if state == "await_code":
        if message.document:
            file_name = message.document.file_name or "file"
            file_path = message.download(file_name)
            if file_name.lower().endswith(".zip"):
                uniq = f"extracted_{int(time.time())}_{random.randint(1000,9999)}"
                os.makedirs(uniq, exist_ok=True)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(uniq)
                except Exception as e:
                    text = f"Error extracting zip: {e}" if lang == "en" else \
                           f"解压 zip 文件出错：{e}" if lang == "zh" else \
                           f"Ошибка при распаковке zip: {e}" if lang == "ru" else \
                           f"استخراج zip با خطا مواجه شد: {e}"
                    message.reply_text(text, reply_markup=back_menu(lang))
                    user_state.pop(user_id, None)
                    return
                py_files = []
                for root, _, files in os.walk(uniq):
                    for f in files:
                        if f.lower().endswith(".py"):
                            py_files.append(os.path.join(root, f))
                if not py_files:
                    text = "Zip file contains no Python code." if lang == "en" else \
                           "Zip 文件不包含 Python 代码。" if lang == "zh" else \
                           "Zip-файл не содержит кода на Python." if lang == "ru" else \
                           "فایل zip شامل کد پایتون نبود."
                    message.reply_text(text, reply_markup=back_menu(lang))
                else:
                    codes = []
                    for p in py_files:
                        code_id = generate_code_id()
                        threading.Thread(target=execute_code, args=(p, code_id, message.chat.id), daemon=True).start()
                        codes.append(code_id)
                    text = "Codes are running.\nPersonal codes: " + ", ".join(codes) if lang == "en" else \
                           "代码正在运行。\n个人代码：" + "，".join(codes) if lang == "zh" else \
                           "Коды выполняются.\nЛичные коды: " + ", ".join(codes) if lang == "ru" else \
                           "کدها در حال اجرا هستند.\nکدهای شخصی: " + "، ".join(codes)
                    message.reply_text(text, reply_markup=back_menu(lang))
            else:
                code_id = generate_code_id()
                threading.Thread(target=execute_code, args=(file_path, code_id, message.chat.id), daemon=True).start()
                text = f"Your code is running. Personal code: {code_id}" if lang == "en" else \
                       f"您的代码正在运行。个人代码：{code_id}" if lang == "zh" else \
                       f"Ваш код выполняется. Личный код: {code_id}" if lang == "ru" else \
                       f"کد شما در حال اجراست. کد شخصی: {code_id}"
                message.reply_text(text, reply_markup=back_menu(lang))
        elif message.text:
            code_id = generate_code_id()
            folder = str(code_id)
            os.makedirs(folder, exist_ok=True)
            code_name = os.path.join(folder, f"temp_code_{code_id}.py")
            try:
                with open(code_name, "w", encoding="utf-8") as f:
                    f.write(message.text)
            except Exception as e:
                text = f"Error saving code: {e}" if lang == "en" else \
                       f"保存代码时出错：{e}" if lang == "zh" else \
                       f"Ошибка при сохранении кода: {e}" if lang == "ru" else \
                       f"خطا در ذخیره کد: {e}"
                message.reply_text(text, reply_markup=back_menu(lang))
                user_state.pop(user_id, None)
                return
            threading.Thread(target=execute_code, args=(code_name, code_id, message.chat.id), daemon=True).start()
            text = f"Your code is running. Personal code: {code_id}" if lang == "en" else \
                   f"您的代码正在运行。个人代码：{code_id}" if lang == "zh" else \
                   f"Ваш код выполняется. Личный код: {code_id}" if lang == "ru" else \
                   f"کد شما در حال اجراست. کد شخصی: {code_id}"
            message.reply_text(text, reply_markup=back_menu(lang))
        else:
            text = "Please send a .py/.zip file or code text." if lang == "en" else \
                   "请发送 .py/.zip 文件或代码文本。" if lang == "zh" else \
                   "Отправьте файл .py/.zip или текст кода." if lang == "ru" else \
                   "لطفاً فایل .py/.zip یا متن کد را ارسال کنید."
            message.reply_text(text, reply_markup=back_menu(lang))
        user_state.pop(user_id, None)
        return
    if state == "await_library":
        lib_name = (message.text or "").strip()
        if not lib_name:
            text = "Invalid library name." if lang == "en" else \
                   "库名称无效。" if lang == "zh" else \
                   "Недопустимое название библиотеки." if lang == "ru" else \
                   "نام کتابخانه نامعتبر است."
            message.reply_text(text, reply_markup=back_menu(lang))
        else:
            threading.Thread(target=install_library, args=(lib_name, message.chat.id), daemon=True).start()
        user_state.pop(user_id, None)
        return
    if state == "await_cancel":
        code_id = (message.text or "").strip()
        if not code_id:
            text = "Invalid personal code." if lang == "en" else \
                   "个人代码无效。" if lang == "zh" else \
                   "Недопустимый личный код." if lang == "ru" else \
                   "کد شخصی نامعتبر است."
            message.reply_text(text, reply_markup=back_menu(lang))
            user_state.pop(user_id, None)
            return
        cur.execute("SELECT file_path, folder_path FROM files WHERE code_id = ?", (code_id,))
        row = cur.fetchone()
        if not row:
            text = "Code not found." if lang == "en" else \
                   "未找到代码。" if lang == "zh" else \
                   "Код не найден." if lang == "ru" else \
                   "کد پیدا نشد."
            message.reply_text(text, reply_markup=back_menu(lang))
            user_state.pop(user_id, None)
            return
        stopped = stop_process(code_id)
        pending_delete[user_id] = code_id
        note = ("Code execution stopped." if stopped else "This code was not running or already stopped.") if lang == "en" else \
               ("代码执行已停止。" if stopped else "此代码未在运行或已停止。") if lang == "zh" else \
               ("Выполнение кода остановлено." if stopped else "Этот код не выполнялся или уже остановлен.") if lang == "ru" else \
               ("اجرای کد متوقف شد." if stopped else "این کد در حال اجرا نبود یااز قبل متوقف شده بود.")
        note += "\n\n"
        note += "Would you like to delete all files related to this code?\n" + \
                "⚠️ Note: If deleted, this personal code cannot be used again." if lang == "en" else \
                "您想删除与此代码相关的所有文件吗？\n" + \
                "⚠️ 注意：删除后，此个人代码无法再次使用。" if lang == "zh" else \
                "Хотите удалить все файлы, связанные с этим кодом?\n" + \
                "⚠️ Примечание: После удаления этот личный код нельзя будет использовать снова." if lang == "ru" else \
                "آیا مایلید همهٔ فایل‌های مربوط به این کد حذف شود؟\n" + \
                "⚠️ توجه: در صورت حذف، با همان کد شخصی دیگر نمی‌توانید دوباره اجرا کنید."
        message.reply_text(note, reply_markup=confirmation_menu(code_id, lang))
        user_state.pop(user_id, None)
        return
    if state == "await_rerun":
        code_id = (message.text or "").strip()
        cur.execute("SELECT file_path FROM files WHERE code_id = ?", (code_id,))
        row = cur.fetchone()
        if row and os.path.exists(row[0]):
            if code_id in running_processes and is_running(running_processes[code_id]):
                text = "This code is currently running." if lang == "en" else \
                       "此代码当前正在运行。" if lang == "zh" else \
                       "Этот код уже выполняется." if lang == "ru" else \
                       "این کد هم‌اکنون در حال اجراست."
                message.reply_text(text, reply_markup=back_menu(lang))
            else:
                threading.Thread(target=execute_code, args=(row[0], code_id, message.chat.id), daemon=True).start()
                text = "Code rerun." if lang == "en" else \
                       "代码重新运行。" if lang == "zh" else \
                       "Код перезапущен." if lang == "ru" else \
                       "کد دوباره اجرا شد."
                message.reply_text(text, reply_markup=back_menu(lang))
        else:
            text = "Code or related file not found." if lang == "en" else \
                   "未找到代码或相关文件。" if lang == "zh" else \
                   "Код или связанный файл не найден." if lang == "ru" else \
                   "کد یا فایل مربوطه یافت نشد."
            message.reply_text(text, reply_markup=back_menu(lang))
        user_state.pop(user_id, None)
        return
    if state == "await_output":
        code_id = (message.text or "").strip()
        cur.execute("SELECT folder_path FROM files WHERE code_id = ?", (code_id,))
        row = cur.fetchone()
        if row:
            folder = row[0]
            output_file = os.path.join(folder, "output.txt")
            if os.path.exists(output_file):
                try:
                    app.send_document(message.chat.id, output_file)
                    text = "Output sent." if lang == "en" else \
                           "输出已发送。" if lang == "zh" else \
                           "Вывод отправлен." if lang == "ru" else \
                           "خروجی ارسال شد."
                    message.reply_text(text, reply_markup=back_menu(lang))
                except Exception:
                    text = "Failed to send output." if lang == "en" else \
                           "发送输出失败。" if lang == "zh" else \
                           "Не удалось отправить вывод." if lang == "ru" else \
                           "ارسال خروجی با مشکل مواجه شد."
                    message.reply_text(text, reply_markup=back_menu(lang))
            else:
                text = "Output not found." if lang == "en" else \
                       "未找到输出。" if lang == "zh" else \
                       "Вывод не найден." if lang == "ru" else \
                       "خروجی یافت نشد."
                message.reply_text(text, reply_markup=back_menu(lang))
        else:
            text = "Code not found." if lang == "en" else \
                   "未找到代码。" if lang == "zh" else \
                   "Код не найден." if lang == "ru" else \
                   "کد پیدا نشد."
            message.reply_text(text, reply_markup=back_menu(lang))
        user_state.pop(user_id, None)
        return
    cid = pending_input.get(message.chat.id)
    if cid and message.text:
        sess = interactive_sessions.get(cid)
        if sess and is_running(sess.get("proc")):
            try:
                sess["proc"].stdin.write(message.text + "\n")
                sess["proc"].stdin.flush()
                interactive_sessions[cid]["awaiting"] = False
                pending_input.pop(message.chat.id, None)
                text = "✅ Input sent." if lang == "en" else \
                       "✅ 输入已发送。" if lang == "zh" else \
                       "✅ Ввод отправлен." if lang == "ru" else \
                       "✅ ورودی ارسال شد."
                message.reply_text(text, reply_markup=back_menu(lang))
                return
            except Exception:
                pending_input.pop(message.chat.id, None)
                text = "Failed to send input." if lang == "en" else \
                       "发送输入失败。" if lang == "zh" else \
                       "Не удалось отправить ввод." if lang == "ru" else \
                       "ارسال ورودی ناموفق بود."
                message.reply_text(text, reply_markup=back_menu(lang))
                return
    sent = message.reply_text(human_welcome(lang), reply_markup=main_menu(lang))
    ui_state[user_id] = sent.id

for code_id, file_path, folder in load_files():
    files_store[code_id] = file_path

if __name__ == "__main__":
    app.run()