from aiogram import Bot
from dishka import Provider, provide, Scope

from src.data.config import *
from src.domain.common.currency_limits import CurrencyLimits
from src.domain.enums import Currency
from src.domain.protocols import (
    ConfigManager,
    LocaleManager,
    RoleManager,
    SponsorManager,
    PaymentManager,
    UserManager, BanManager
)
from src.impl.protocols import (
    DefaultRoleManagerFactory,
    FileConfigManagerFactory,
    DefaultLocaleManageFactory,
    DefaultSponsorManagerFactory,
    DefaultPaymentManagerFactory,
    DefaultUserManagerFactory,
    CryptoBotPayment, DefaultBanManagerFactory,
)


class DefaultProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_role_manager(self) -> RoleManager:
        factory = DefaultRoleManagerFactory(
            owner_ids=OWNER_IDS
        )
        return await factory.create_role_manager()

    @provide
    async def get_config_manager(self) -> ConfigManager:
        factory = FileConfigManagerFactory(
            path=CONFIG_MANAGER_FILE
        )
        return await factory.create_config_manager()

    @provide
    async def get_locale_manager(self) -> LocaleManager:
        factory = DefaultLocaleManageFactory(
            locales_dir=LOCALES_DIR,
            default_locale_name=DEFAULT_LOCALE_NAME
        )
        return await factory.create_locale_manager()

    @provide
    async def get_sponsor_manager(self) -> SponsorManager:
        factory = DefaultSponsorManagerFactory(
            bot=Bot(token=BOT_TOKEN)
        )
        return await factory.create_sponsor_manager()

    @provide
    async def get_payment_manager(self) -> PaymentManager:
        config_manager = await self.get_config_manager()
        payment_manager = DefaultPaymentManagerFactory(
            payments=[CryptoBotPayment, ],
            limits=[
                CurrencyLimits(Currency.USDT)
            ],
            config_manager=config_manager
        )
        return await payment_manager.create_payment_manager()

    @provide
    async def get_user_manager(self) -> UserManager:
        factory = DefaultUserManagerFactory()
        return await factory.create_user_manager()

    @provide
    async def get_ban_manager(self) -> BanManager:
        factory = DefaultBanManagerFactory()
        return await factory.create_ban_manager()
