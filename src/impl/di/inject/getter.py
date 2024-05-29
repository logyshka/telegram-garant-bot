from typing import Callable

from dishka.integrations.base import wrap_injection

CONTAINER_NAME = "dishka_container"


def inject_getter(func: Callable) -> Callable:
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p[CONTAINER_NAME],
        is_async=True,
        remove_depends=True,
    )
