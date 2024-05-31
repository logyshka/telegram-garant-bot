from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from src.application import states
from src.application.widgets.locale import LocaleConst

dialog = Dialog(
    Window(
        Const('Главное меню'),
        Cancel(LocaleConst('close')),
        state=states.user.MenuSG.main
    )
)
