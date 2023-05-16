from ._dialog_hello import dialog as dialog_hello
from ._dialog_help import dialog as dialog_help
from ._dialog_olympiad_interests import dialog as dialog_olympiad_interests
from ._dialog_admin import dialog as dialog_admin

dialogs = [dialog_hello, dialog_help, dialog_olympiad_interests, dialog_admin]

__all__ = ["dialogs"]
