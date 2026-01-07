📄 PDF & Word Converter Telegram Bot
A Python-based Telegram bot that allows users to seamlessly convert PDF files to Word (DOCX) and Word files to PDF. It features an interactive menu with buttons to choose the conversion mode.

✨ Features
Dual Conversion: Convert PDF to DOCX and DOCX to PDF.

Interactive UI: Uses Inline Keyboard buttons for a better user experience.

Fast Processing: Files are processed and sent back instantly.

Auto-Cleanup: Temporary files are deleted from the server/PC after conversion to protect privacy and save space.

🚀 Getting Started
1. Prerequisites
Python 3.8+ installed.

Microsoft Word (Required for Word to PDF conversion on Windows/macOS).

Telegram Bot Token: Get one from @BotFather.

2. Installation
Clone this repository or download the source code, then install the required libraries:

Bash

pip install python-telegram-bot pdf2docx docx2pdf
3. Configuration
Open the bot.py (or structure.py) file.

Find the TOKEN variable.

Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual API token.

4. Running the Bot
Execute the script from your terminal:

Bash

python bot.py
🛠 How to Use
Open your bot in Telegram and press /start.

Select the conversion mode from the buttons:

PDF ➡️ Word

Word ➡️ PDF

Upload the document you wish to convert.

Wait a few seconds, and the bot will send you the converted file!

📦 Libraries Used
python-telegram-bot - The framework for the Telegram interface.

pdf2docx - Handles the extraction of layout and text from PDF to Word.

docx2pdf - Automates Microsoft Word to export DOCX as PDF.

⚠️ Important Notes
OCR: This bot does not support OCR. If the PDF is a scanned image, the Word output will contain images rather than editable text.

Word to PDF Requirement: The docx2pdf library requires Microsoft Word to be installed on the machine running the script. It will not work on headless Linux servers without extra configuration (like LibreOffice).

📜 License
This project is open-source. Feel free to modify and distribute as needed.
