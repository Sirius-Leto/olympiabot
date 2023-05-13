from aiogram_dialog import Dialog
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Row
from aiogram_dialog.widgets.text import Const, List, Multi

from .common_components.buttons import NAVIGATION_BAR, BACK_BUTTON, EXIT_BUTTON
from routers.states import HelpSG

import json

CONTACT_ADMIN = "https://t.me/dantetemplar"

help_window = Window(
    Const(f"Вы можете обратиться за помощью к администратору бота по адресу: {CONTACT_ADMIN}", ),
    SwitchTo(Const("FAQ"), id="faq", state=HelpSG.faq),
    EXIT_BUTTON,
    state=HelpSG.help_,
)

faq_instances = json.load(open("routers/dialogs/faq.json", "r", encoding="utf-8"))
faq_questions = [Const(f"{faq['question']}\n{faq['answer']}") for faq in faq_instances["questions"]]

faq_window = Window(
    Const("*FAQ 📖 Часто задаваемые вопросы*\n————————————————————————————\n"),

    Multi(*faq_questions, sep="\n\n"),
    NAVIGATION_BAR,
    state=HelpSG.faq,
    parse_mode="MarkdownV2",
)

help_dialog = Dialog(help_window, faq_window)

__all__ = ["help_dialog"]
