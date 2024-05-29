from typing import Callable

from dishka.integrations.base import wrap_injection

CONTAINER_NAME = "dishka_container"


def inject_on_dialog_event(func: Callable) -> Callable:
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[1].middleware_data[CONTAINER_NAME],
        is_async=True,
        remove_depends=True,
    )
