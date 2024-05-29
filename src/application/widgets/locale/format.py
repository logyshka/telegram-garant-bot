from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka.integrations.aiogram import FromDishka

from src.domain.protocols import LocaleManager
from src.impl.di.inject.widget import inject_widget


class _FormatDataStub:
    def __init__(self, name="", data=None):
        self.name = name
        self.data = data or {}

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        if not self.name:
            return _FormatDataStub(item)
        return _FormatDataStub(f"{self.name}[{item}]")

    def __getattr__(self, item):
        return _FormatDataStub(f"{self.name}.{item}")

    def __format__(self, format_spec):
        if format_spec:
            res = f"{self.name}:{format_spec}"
        else:
            res = self.name
        return f"{{{res}}}"


class LocaleFormat(Text):
    def __init__(self, text_id: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text_id = text_id

    @inject_widget
    async def _render_text(
            self, data: Dict, manager: DialogManager, locale_manager: FromDishka[LocaleManager]
    ) -> str:
        text = await locale_manager.get_text(text_id=self.text_id, user_id=manager.event.from_user.id)
        if manager.is_preview():
            return text.format_map(_FormatDataStub(data=data))
        return text.format_map(data)
