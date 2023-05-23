from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const

from routers.dialogs.common_components.buttons import NAVIGATION_BAR
from routers.states import AdminSG

admin_hello_window = Window(
    # Format("Привет, ваша роль — {role}!"),
    Const("Админочка"),
    NAVIGATION_BAR,
    state=AdminSG.start,
)

windows = [admin_hello_window]
dialog = Dialog(*windows)

__all__ = ["dialog"]
