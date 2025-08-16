import os
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from handlers.menu import menu, menu_callback_handler
from system.admin import admin_menu, admin_callback_handler

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# --- No-op handlers to swallow anything we don't explicitly handle ---
async def ignore_everything(update, context):
    # Intentionally do nothing (prevents accidental auto-replies)
    return

async def ignore_unknown_command(update, context):
    # Silently ignore unknown commands to avoid "unnecessary" replies.
    return

def main():
    app = Application.builder().token(TOKEN).build()

    # Only these commands are allowed to respond
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("admin", admin_menu))

    # Callback queries: split user vs admin by prefix
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern=r"^(?!admin_)"))
    app.add_handler(CallbackQueryHandler(admin_callback_handler, pattern=r"^admin_"))

    # -------- STRICT MODE --------
    # 1) Ignore ALL text that isn't a command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ignore_everything), group=100)
    # 2) Ignore *every other* update type we don't need (stickers, photos, etc.)
    app.add_handler(MessageHandler(~filters.COMMAND & ~filters.TEXT, ignore_everything), group=101)
    # 3) Silently drop unknown commands so the bot doesn't chat back unnecessarily
    app.add_handler(MessageHandler(filters.COMMAND, ignore_unknown_command), group=102)

    print("🤖 Bot is running... Use /menu to start.")
    app.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,  # don't process old backlog
        stop_signals=None,          # improve shutdown reliability in some hosts
    )

if __name__ == "__main__":
    main()
