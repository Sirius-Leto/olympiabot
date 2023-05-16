from aiogram_dialog.widgets.kbd import Back, Next, Start, Group, Row, Button
from aiogram_dialog.widgets.text import Const, Case

from .callbacks import (callback_exit_or_start_button, callback_exit_button, has_stack_above, has_back_state,
                        has_next_state)

from ...states import MainSG

HELP_BUTTON = Start(Const("Помощь ❓"), id="help", state=MainSG.Help.start)
BACK_BUTTON = Back(Const("Назад  ⬅️"), id="back", when=has_back_state)
NEXT_BUTTON = Next(Const("Далее  ➡️"), id="next", when=has_next_state)
EXIT_BUTTON = Button(Const("Выйти  🚪"), id="pop_stack", on_click=callback_exit_button, when=has_stack_above)

EXIT_OR_START_BUTTON = Button(Case(
    {
        True: Const("Выйти  🚪"),
        False: Const("Начать  🚪")
    },
    selector=lambda data, widget, manager: len(manager.current_stack().intents) > 1
),
    id="pop_or_start_stack",
    on_click=callback_exit_or_start_button
)

NAVIGATION_BAR = Group(Row(BACK_BUTTON), EXIT_BUTTON)
