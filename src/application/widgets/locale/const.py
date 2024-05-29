from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka.integrations.aiogram import FromDishka

from src.domain.protocols import LocaleManager
from src.impl.di.inject.widget import inject_widget


class LocaleConst(Text):
    def __init__(self, text_id: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text_id = text_id

    @inject_widget
    async def _render_text(
            self, data: Dict, manager: DialogManager, locale_manager: FromDishka[LocaleManager]
    ) -> str:
        return await locale_manager.get_text(text_id=self.text_id, user_id=manager.event.from_user.id)
