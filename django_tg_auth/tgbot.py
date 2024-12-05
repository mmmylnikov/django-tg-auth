#!/usr/bin/env python

"""
Simple Bot to reply to Telegram messages
for authentication user on Django application.
"""
import logging
import os

import django
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.settings import DJANGO_HOST, DJANGO_TELEGRAM_SECRET  # noqa: E402
from tgauth.utils import TgDataCheckString  # noqa: E402


load_dotenv(override=True)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

AUTH = "auth"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user:
        return
    if not update.message:
        return
    text = "".join([
        'Visit our website and click "Sign in using Telegram bot":\n\n',
        DJANGO_HOST,
    ])
    await update.message.reply_text(text)


async def deep_linked_auth(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.message:
        return
    elif not update.message.from_user:
        await update.message.reply_text(
            "Only Telegram users can use this command"
        )
        return
    elif not update.message.from_user.username:
        await update.message.reply_text(
            "You must have a Telegram username."
        )
        return
    elif not update.message.from_user.first_name:
        await update.message.reply_text(
            "You must have your real name in the telegram. Please fill it out."
        )
        return
    elif not update.message.from_user.last_name:
        await update.message.reply_text(
            "".join(
                [
                    "You must have your real last name in the telegram. ",
                    "Please fill it out.",
                ]
            )
        )
        return
    text = "Great! To log in, click the button below"
    tg_check_object = TgDataCheckString.from_now_date(
        id=str(update.message.from_user.id),
        username=update.message.from_user.username,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
        photo_url='',
    )
    url = tg_check_object.auth_url()
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Continue here!", url=url)
    )
    await update.message.reply_text(text, reply_markup=keyboard)


def main() -> None:
    """Start the bot."""

    if not DJANGO_TELEGRAM_SECRET:
        raise Exception("DJANGO_TELEGRAM_SECRET is not set")

    application = Application.builder().token(DJANGO_TELEGRAM_SECRET).build()

    application.add_handler(
        CommandHandler("start", deep_linked_auth, filters.Regex(AUTH))
    )
    application.add_handler(CommandHandler("start", start))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
