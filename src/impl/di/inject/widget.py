from typing import Callable

from dishka.integrations.base import wrap_injection

CONTAINER_NAME = "dishka_container"


def widget_getter(*args, **kwargs):
    middleware_data = args[0][1].get('middleware_data')
    if not middleware_data:
        middleware_data = args[0][1]['data']['middleware_data']
    return middleware_data[CONTAINER_NAME]


def inject_widget(func: Callable) -> Callable:
    return wrap_injection(
        func=func,
        container_getter=widget_getter,
        is_async=True,
        remove_depends=True,
    )

