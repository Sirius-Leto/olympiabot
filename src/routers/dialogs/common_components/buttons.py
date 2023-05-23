from aiogram_dialog.widgets.kbd import Back, Next, Start, Group, Row, Button
from aiogram_dialog.widgets.text import Const, Case

from .callbacks import *
from .emojis import *
from ...states import UserSG

HELP_BUTTON = Start(Const("Помощь " + QUESTION_EMOJI), id="help", state=UserSG.Help.start)
BACK_BUTTON = Back(Const("Назад  " + BACK_EMOJI), id="back", when=has_back_state)
NEXT_BUTTON = Next(Const("Далее  " + NEXT_EMOJI), id="next", when=has_next_state)
EXIT_BUTTON = Button(Const("Выйти  " + EXIT_EMOJI), id="pop_stack", on_click=callback_exit_button, when=has_stack_above)

EXIT_OR_START_BUTTON = Button(Case(
    {
        True: Const("Выйти  " + EXIT_EMOJI),
        False: Const("Перейти к началу  " + START_EMOJI)
    },
    selector=lambda data, widget, manager: len(manager.current_stack().intents) > 1
),
    id="pop_or_start_stack",
    on_click=callback_exit_or_start_button
)

NAVIGATION_BAR = Group(Row(BACK_BUTTON), EXIT_BUTTON)
