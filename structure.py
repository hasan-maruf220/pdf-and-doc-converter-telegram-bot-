import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from pdf2docx import Converter
from docx2pdf import convert

# --- Configuration ---
TOKEN = 'ADD_YOUR_BOT_TOKEN'  # <--- PASTE YOUR TOKEN HERE

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message with buttons to choose mode"""
    
    # Create two buttons
    keyboard = [
        [InlineKeyboardButton("PDF ➡️ Word (DOCX)", callback_data='mode_pdf_to_word')],
        [InlineKeyboardButton("Word (DOCX) ➡️ PDF", callback_data='mode_word_to_pdf')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\nPlease choose what you want to do:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# --- Button Handler ---
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the button click and sets the user's mode"""
    query = update.callback_query
    await query.answer() # Acknowledge the click so the loading circle stops

    choice = query.data
    
    # Save the user's choice in their personal data storage
    context.user_data['mode'] = choice

    if choice == 'mode_pdf_to_word':
        await query.edit_message_text("📎 Now send me a PDF file.")
    elif choice == 'mode_word_to_pdf':
        await query.edit_message_text("📎 Now send me a DOCX file.")

# --- File Processing ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Decides which conversion to run based on the user's selected mode"""
    
    # 1. Check if user selected a mode
    mode = context.user_data.get('mode')
    
    if not mode:
        await update.message.reply_text("⚠️ Please select a mode first by typing /start")
        return

    document = update.message.document
    file_id = document.file_id
    status_msg = await update.message.reply_text("⏳ Processing Your File ... please wait.")

    try:
        # --- MODE 1: PDF TO WORD ---
        if mode == 'mode_pdf_to_word':
            if document.mime_type != 'application/pdf':
                await status_msg.edit_text("❌ Error: You are in 'PDF to Word' mode. Please send a PDF file.")
                return

            # Download
            input_path = f"{file_id}.pdf"
            output_path = f"{file_id}.docx"
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(input_path)

            # Convert
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()

            # Send back
            await update.message.reply_document(
                document=open(output_path, 'rb'),
                filename=f"{document.file_name}.docx",
                caption="Here is your Word file! have fun 😉👌"
            )

        # --- MODE 2: WORD TO PDF ---
        elif mode == 'mode_word_to_pdf':
            # Note: mime type for docx can vary, usually checking extension is safer for simple bots
            file_name = document.file_name.lower()
            if not file_name.endswith('.docx') and not file_name.endswith('.doc'):
                await status_msg.edit_text("❌ Error: You are in 'Word to PDF' mode. Please send a Word (.docx) file.")
                return

            # Download
            input_path = f"{file_id}.docx"
            output_path = f"{file_id}.pdf"
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(input_path)

            # Convert (Requires MS Word installed)
            # We use absolute path because docx2pdf sometimes requires it
            abs_input = os.path.abspath(input_path)
            abs_output = os.path.abspath(output_path)
            convert(abs_input, abs_output)

            # Send back
            await update.message.reply_document(
                document=open(output_path, 'rb'),
                filename=f"{document.file_name}.pdf",
                caption="Here is your PDF file! Enjoy 😉👌"
            )

    except Exception as e:
        await update.message.reply_text(f"⚠️ An error occurred: {e}")

    finally:
        # Cleanup files
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        
        # Delete status message
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=status_msg.message_id)
        except:
            pass

# --- Main Application ---
def main():
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click)) # Handles button clicks
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document)) # Handles files

    print("Polling...")
    app.run_polling()

if __name__ == '__main__':
    main()