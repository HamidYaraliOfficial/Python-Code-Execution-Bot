# Python Code Execution Bot

## Overview

This is a Telegram bot designed to execute Python code, manage files, install libraries, and provide real-time code execution status. It supports interactive terminal sessions, code rerunning, output retrieval, and file management with a user-friendly interface. The bot is restricted to a single owner for security and uses a SQLite database to track code and files.

Created by: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)

## Features

- **Code Execution**: Run Python (.py) files or code snippets with unique personal codes for tracking.
- **File Management**: Upload and execute .py or .zipබී
- **Library Installation**: Install Python libraries via pip directly through the bot.
- **Interactive Terminal**: Supports real-time input/output for interactive Python scripts.
- **Multilingual Support**: Interface available in Persian, English, Chinese, and Russian.
- **Output Retrieval**: View execution outputs as text files.
- **Process Management**: Cancel or rerun ongoing code executions.
- **Database Storage**: Stores code and file metadata for efficient management.

## Supported Languages

- Persian (فارسی)
- English
- Chinese (中文)
- Russian (Русский)

## Requirements

- Python 3.x
- Pyrogram library
- SQLite3
- Standard Python libraries (os, subprocess, threading, zipfile, random, shutil, string, time)

## Setup

1. Install dependencies:
   ```bash
   pip install pyrogram
   ```
2. Configure your Telegram Bot Token, API ID, API Hash, and Owner ID in the script.
3. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

- Start the bot with the `/start` command in Telegram.
- Use the inline buttons to:
  - Submit Python files or code snippets.
  - Install libraries.
  - Run or cancel code execution.
  - View outputs or active codes.
  - Switch between supported languages.
- Each code execution is assigned a unique personal code for tracking.

## Notes

- The bot is restricted to the owner specified by `OWNER_ID` for security.
- Supports .py and .zip files for code execution.
- Interactive sessions allow real-time input for running scripts.
- Files are stored in a SQLite database (`bot.db`) and can be deleted after execution.
- Ensure proper error handling for file operations and process management.

## License

MIT License

---

# ربات اجرای کد پایتون

## بررسی اجمالی

این یک ربات تلگرامی است که برای اجرای کدهای پایتون، مدیریت فایل‌ها، نصب کتابخانه‌ها و ارائه وضعیت اجرای کد به‌صورت لحظه‌ای طراحی شده است. این ربات از جلسات ترمینال تعاملی، اجرای مجدد کدها، دریافت خروجی و مدیریت فایل‌ها با رابط کاربری ساده پشتیبانی می‌کند. برای امنیت، ربات تنها برای مالک مشخص‌شده قابل استفاده است و از پایگاه داده SQLite برای مدیریت کدها و فایل‌ها استفاده می‌کند.

سازنده: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)

## ویژگی‌ها

- **اجرای کد**: اجرای فایل‌های پایتون (.py) یا کدهای متنی با کدهای شخصی منحصربه‌فرد برای ردیابی.
- **مدیریت فایل**: آپلود و اجرای فایل‌های .py یا .zip.
- **نصب کتابخانه**: نصب کتابخانه‌های پایتون از طریق pip در ربات.
- **ترمینال تعاملی**: پشتیبانی از ورودی/خروجی لحظه‌ای برای اسکریپت‌های تعاملی.
- **پشتیبانی چندزبانه**: رابط کاربری به زبان‌های فارسی، انگلیسی، چینی و روسی.
- **دریافت خروجی**: مشاهده خروجی‌های اجرا به‌صورت فایل متنی.
- **مدیریت فرآیندها**: لغو یا اجرای مجدد کدها.
- **ذخیره‌سازی پایگاه داده**: ذخیره metadata کدها و فایل‌ها برای مدیریت بهتر.

## زبان‌های پشتیبانی‌شده

- فارسی
- انگلیسی
- چینی
- روسی

## پیش‌نیازها

- پایتون نسخه 3.x
- کتابخانه Pyrogram
- SQLite3
- کتابخانه‌های استاندارد پایتون (os، subprocess، threading، zipfile، random، shutil، string، time)

## راه‌اندازی

1. نصب وابستگی‌ها:
   ```bash
   pip install pyrogram
   ```
2. تنظیم توکن ربات تلگرام، API ID، API Hash و Owner ID در اسکریپت.
3. اجرای ربات:
   ```bash
   python bot.py
   ```

## نحوه استفاده

- ربات را با دستور `/start` در تلگرام شروع کنید.
- از دکمه‌های اینلاین برای موارد زیر استفاده کنید:
  - ارسال فایل یا کد پایتون.
  - نصب کتابخانه‌ها.
  - اجرا یا لغو اجرای کدها.
  - مشاهده خروجی‌ها یا کدهای فعال.
  - تغییر زبان رابط کاربری.
- هر اجرای کد یک کد شخصی منحصربه‌فرد برای ردیابی دریافت می‌کند.

## نکات

- ربات برای امنیت فقط برای مالک مشخص‌شده با `OWNER_ID` قابل استفاده است.
- از فایل‌های .py و .zip برای اجرای کدها پشتیبانی می‌کند.
- جلسات تعاملی امکان ورودی لحظه‌ای برای اسکریپت‌های در حال اجرا را فراهم می‌کنند.
- فایل‌ها در پایگاه داده SQLite (`bot.db`) ذخیره شده و پس از اجرا قابل حذف هستند.
- از مدیریت خطاهای مناسب برای عملیات فایل و فرآیندها اطمینان حاصل کنید.

## مجوز

MIT License

---

# Python 代码执行机器人

## 概述

这是一个专为执行 Python 代码、文件管理、库安装以及提供实时代码执行状态的 Telegram 机器人。它支持交互式终端会话、重新运行代码、获取输出以及具有用户友好界面的文件管理。为确保安全，机器人仅限特定所有者使用，并使用 SQLite 数据库来跟踪代码和文件。

作者：[HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)

## 功能

- **代码执行**：运行 Python (.py) 文件或代码片段，并为每次执行分配唯一的个人代码以便跟踪。
- **文件管理**：上传并执行 .py 或 .zip 文件。
- **库安装**：通过 pip 直接在机器人中安装 Python 库。
- **交互式终端**：支持交互式 Python 脚本的实时输入/输出。
- **多语言支持**：界面支持波斯语、英语、汉语和俄语。
- **输出获取**：以文本文件形式查看执行输出。
- **进程管理**：取消或重新运行正在执行的代码。
- **数据库存储**：存储代码和文件的元数据以便高效管理。

## 支持的语言

- 波斯语
- 英语
- 汉语
- 俄语

## 要求

- Python 3.x
- Pyrogram 库
- SQLite3
- 标准 Python 库 (os、subprocess、threading、zipfile、random、shutil、string、time)

## 设置

1. 安装依赖项：
   ```bash
   pip install pyrogram
   ```
2. 在脚本中配置 Telegram 机器人令牌、API ID、API Hash 和所有者 ID。
3. 运行机器人：
   ```bash
   python bot.py
   ```

## 使用方法

- 在 Telegram 中使用 `/start` 命令启动机器人。
- 使用内联按钮进行以下操作：
  - 提交 Python 文件或代码片段。
  - 安装库。
  - 运行或取消代码执行。
  - 查看输出或活跃代码。
  - 切换支持的语言。
- 每次代码执行都会分配一个唯一的个人代码以便跟踪。

## 注意事项

- 为确保安全，机器人仅限由 `OWNER_ID` 指定的所有者使用。
- 支持 .py 和 .zip 文件的代码执行。
- 交互式会话允许实时输入正在运行的脚本。
- 文件存储在 SQLite 数据库 (`bot.db`) 中，执行后可删除。
- 确保对文件操作和进程管理进行适当的错误处理。

## 许可证

MIT License