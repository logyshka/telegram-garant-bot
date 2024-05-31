from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select, Group, Button
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst, LocaleJinja
from src.domain.enums import LocaleName
from src.domain.protocols import LocaleManager
from src.impl.di.inject import inject_on_click, inject_getter
from src.utils.strenum import get_enum_by_name


@inject_on_click
async def select_locale(
        call: CallbackQuery,
        _widget: Select,
        _dialog_manager: DialogManager,
        locale_name: str,
        locale_manager: FromDishka[LocaleManager],
):
    locale_name = get_enum_by_name(name=locale_name, enum=LocaleName)
    user_id = call.from_user.id
    await locale_manager.change_user_locale_name(
        user_id=user_id,
        locale_name=locale_name
    )
    text = await locale_manager.get_text(
        text_id='locale-change-success',
        user_id=user_id
    )
    await call.answer(text=text, show_alert=True)


async def close(
        _call: CallbackQuery,
        _widget: Button,
        dialog_manager: DialogManager
):
    if dialog_manager.start_data:
        await dialog_manager.start(
            state=states.user.MenuSG.main,
            mode=StartMode.RESET_STACK
        )
    else:
        await dialog_manager.done()


@inject_getter
async def locale_getter(
        locale_manager: FromDishka[LocaleManager],
        dialog_manager: DialogManager,
        **_kwargs,
):
    locale_name = await locale_manager.get_user_locale_name(user_id=dialog_manager.event.from_user.id)
    locales = [
        locale for locale in locale_manager.locales
        if locale.name != locale_name
    ]
    return {
        'locales': locales,
        'current_locale_name': locale_name
    }


dialog = Dialog(
    Window(
        LocaleJinja('locale-menu'),
        Group(
            Select(
                Format('{item.name}'),
                items='locales',
                item_id_getter=lambda locale: locale.name.name,
                id='select_locale',
                on_click=select_locale
            ),
            width=2
        ),
        Button(
            LocaleConst('close'),
            id='close',
            on_click=close
        ),
        state=states.user.LocaleSG.locale,
        getter=locale_getter
    )
)
