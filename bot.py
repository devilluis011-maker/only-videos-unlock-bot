
import os
import asyncio
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
MINI_APP_URL = os.environ["MINI_APP_URL"]
VIDEO_FILE_ID = os.environ.get("VIDEO_FILE_ID", "")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "🔓 Unlock Videos",
            web_app=WebAppInfo(url=MINI_APP_URL),
        )
    ]]

    await update.message.reply_text(
        "🎬 Only Videos Unlock\n\n"
        "ভিডিও আনলক করতে নিচের বাটনে চাপো।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not VIDEO_FILE_ID:
        await query.message.reply_text(
            "ভিডিও এখনো সেট করা হয়নি। অ্যাডমিনকে জানাও।"
        )
        return

    sent = await context.bot.send_video(
        chat_id=query.from_user.id,
        video=VIDEO_FILE_ID,
        caption="🎬 তোমার ভিডিও! ১০ মিনিট পর মুছে যাবে।",
    )

    async def delete_later():
        await asyncio.sleep(600)
        try:
            await context.bot.delete_message(
                chat_id=sent.chat_id,
                message_id=sent.message_id,
            )
        except Exception:
            logging.exception("ভিডিও মেসেজ ডিলিট করা যায়নি")

    asyncio.create_task(delete_later())


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("▶ Watch", callback_data="send_video")
    ]]

    await update.message.reply_text(
        "ভিডিও পাঠানোর জন্য Watch চাপো।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(
        CallbackQueryHandler(send_video, pattern="^send_video$")
    )

    app.run_polling()


if __name__ == "__main__":
    main()
