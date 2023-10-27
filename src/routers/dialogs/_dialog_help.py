import json

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Multi

from routers.states import UserSG
from .common_components.buttons import EXIT_OR_START_BUTTON, BACK_BUTTON
from config import settings

CONTACT_ADMIN = "https://t.me/ysaprunov"

help_window = Window(
    Const(f"Вы можете обратиться за помощью к администратору бота по адресу: {CONTACT_ADMIN}", ),
    SwitchTo(Const("FAQ"), id="faq", state=UserSG.Help.faq),
    EXIT_OR_START_BUTTON,
    state=UserSG.Help.start,
)

faq_instances = json.load(open("src/static/faq.json", "r", encoding="utf-8"))
faq_questions = [Const(f"{faq['question']}\n{faq['answer']}") for faq in faq_instances["questions"]]

faq_window = Window(
    Const("*FAQ 📖 Часто задаваемые вопросы*\n————————————————————————————\n"),

    Multi(*faq_questions, sep="\n\n"),
    BACK_BUTTON, EXIT_OR_START_BUTTON,
    state=UserSG.Help.faq,
    parse_mode="MarkdownV2",
)

windows = [help_window, faq_window]

dialog = Dialog(*windows)

__all__ = ["dialog"]
