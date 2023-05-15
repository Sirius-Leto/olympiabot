import json

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Multi

from routers.states import HelpSG
from .common_components.buttons import EXIT_OR_START_BUTTON, BACK_BUTTON
from config import settings

CONTACT_ADMIN = "https://t.me/dantetemplar"

help_window = Window(
    Const(f"Вы можете обратиться за помощью к администратору бота по адресу: {CONTACT_ADMIN}", ),
    SwitchTo(Const("FAQ"), id="faq", state=HelpSG.faq),
    EXIT_OR_START_BUTTON,
    state=HelpSG.help_,
)

faq_instances = json.load(open(settings.STATIC_DIR / "faq.json", "r", encoding="utf-8"))
faq_questions = [Const(f"{faq['question']}\n{faq['answer']}") for faq in faq_instances["questions"]]

faq_window = Window(
    Const("*FAQ 📖 Часто задаваемые вопросы*\n————————————————————————————\n"),

    Multi(*faq_questions, sep="\n\n"),
    BACK_BUTTON, EXIT_OR_START_BUTTON,
    state=HelpSG.faq,
    parse_mode="MarkdownV2",
)

dialog = Dialog(help_window, faq_window)

__all__ = ["dialog"]
