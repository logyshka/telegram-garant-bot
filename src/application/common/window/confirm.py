from typing import Optional

from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, Cancel
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.utils import GetterVariant

from src.application.widgets.locale import LocaleConst


def create_confirm_window(
        text: Text,
        state: State,
        on_confirm: OnClick,
        on_cancel: Optional[OnClick] = None,
        getter: Optional[GetterVariant] = None
) -> Window:
    return Window(
        text,
        Row(
            Button(LocaleConst('yes'), id='yes', on_click=on_confirm),
            Cancel(LocaleConst('no'), id='no', on_click=on_cancel)
        ),
        state=state,
        getter=getter
    )
