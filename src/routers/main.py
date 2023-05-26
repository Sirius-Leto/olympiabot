from aiogram import Router, Dispatcher
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from data.repositories.roles import RoleRepository, UserRole
from routers.dialogs import dialogs
from routers.states import UserSG, AdminSG

main_router = Router()
main_router.include_routers(*dialogs)


@main_router.message(Command("start"))
async def _(_message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserSG.start, mode=StartMode.RESET_STACK)


@main_router.message(Command("help"))
async def _(_message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserSG.Help.start, mode=StartMode.RESET_STACK)


@main_router.message(Command("admin"))
async def _(message: Message, dialog_manager: DialogManager, roles_repository: RoleRepository):
    tg_id = message.from_user.id
    role = await roles_repository.get_role(tg_id)
    if role >= UserRole.MODERATOR:
        await message.answer(f"Ваша роль: {role}")
        await dialog_manager.start(AdminSG.start, mode=StartMode.RESET_STACK, data={"role": role})
    else:
        await message.answer("У вас нет доступа к админ-панели")


def register_stop_handler(dispatcher: Dispatcher):
    @dispatcher.message(Command("stop", "stop_polling"))
    async def _(message: Message, roles_repository: RoleRepository):
        tg_id = message.from_user.id
        role = await roles_repository.get_role(tg_id)

        if role >= UserRole.SUPERUSER:
            await message.answer("Бот остановлен")
            await dispatcher.storage.close()
            await dispatcher.stop_polling()


@main_router.errors(ExceptionTypeFilter(UnknownIntent))
async def _(error: ErrorEvent):
    if isinstance(error.exception, KeyError):
        if error.exception.args[0] != "aiogd_context":
            raise

    event_type = error.update.event_type
    if event_type == "callback_query":
        await error.update.callback_query.answer(
            "Пожалуйста, начните сначала (/start). Выбранный контекст был сброшен. ")
