from ._dialog_hello import dialog as dialog_hello
from ._dialog_help import dialog as dialog_help
from ._dialog_olympiad_interests import dialog as olympiad_interest_dialog

dialogs = [dialog_hello, dialog_help, olympiad_interest_dialog]

__all__ = ["dialogs"]
