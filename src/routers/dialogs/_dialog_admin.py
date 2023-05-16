from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from routers.dialogs.common_components.buttons import NAVIGATION_BAR
from routers.states import AdminSG

admin_hello_window = Window(
    Format("Привет, ваша роль — {role}!"),
    NAVIGATION_BAR,
    state=AdminSG.start,
    getter=lambda data: data["role"]
)

windows = [admin_hello_window]
dialog = Dialog(*windows)

__all__ = ["dialog"]
