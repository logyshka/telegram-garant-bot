from typing import Dict

from aiogram import Bot
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD, default_env
from dishka.integrations.aiogram import FromDishka
from jinja2 import Environment

from src.domain.protocols import LocaleManager
from src.impl.di.inject.widget import inject_widget


class LocaleJinja(Text):
    def __init__(self, text_id: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text_id = text_id

    @inject_widget
    async def _render_text(
            self, data: Dict, manager: DialogManager, locale_manager: FromDishka[LocaleManager]
    ) -> str:
        template_text = await locale_manager.get_text(text_id=self.text_id, user_id=manager.event.from_user.id)

        if JINJA_ENV_FIELD in manager.dialog_data:
            env = manager.dialog_data[JINJA_ENV_FIELD]
        else:
            bot: Bot = manager.middleware_data.get("bot")
            env: Environment = getattr(bot, JINJA_ENV_FIELD, default_env)

        template = env.get_template(template_text)

        if env.is_async:
            return await template.render_async(data)
        else:
            return template.render(data)
