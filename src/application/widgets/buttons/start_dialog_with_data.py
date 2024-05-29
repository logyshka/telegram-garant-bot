from typing import List
from typing import Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.kbd.state import EventProcessorButton
from aiogram_dialog.widgets.text import Text


class StartWithDialogData(EventProcessorButton):
    def __init__(
            self,
            text: Text,
            id: str,
            state: State,
            dialog_data_keys: List[str],
            on_click: Optional[OnClick] = None,
            mode: StartMode = StartMode.NORMAL,
            when: WhenCondition = None,
    ):
        super().__init__(
            text=text, on_click=self._on_click,
            id=id, when=when,
        )
        self.text = text
        self.dialog_data_keys = dialog_data_keys
        self.user_on_click = on_click
        self.state = state
        self.mode = mode

    async def _on_click(
            self,
            callback: CallbackQuery,
            button: Button,
            manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)
        start_data = {key: manager.dialog_data.get(key) for key in self.dialog_data_keys}
        await manager.start(
            state=self.state,
            data=start_data,
            mode=self.mode
        )
