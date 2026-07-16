from __future__ import annotations

from src.models import Group, Option
from src.plugins import (
    get_display_options,
    get_sync_options,
    get_rendering_options,
    get_upscaling_options,
    get_input_options,
    get_misc_options,
)


def load_plugins() -> list[Group]:
    groups: list[Group] = []
    groups.extend(get_display_options())  # type: ignore
    groups.extend(get_sync_options())  # type: ignore
    groups.extend(get_rendering_options())  # type: ignore
    groups.extend(get_upscaling_options())  # type: ignore
    groups.extend(get_input_options())  # type: ignore
    groups.extend(get_misc_options())  # type: ignore
    return groups


def flatten_options(groups: list[Group]) -> list[Option]:
    result: list[Option] = []
    for group in groups:
        for child in group.children:
            if isinstance(child, Option):
                result.append(child)
                result.extend(child.children)
    return result
