from __future__ import annotations

from src.models import Group, Option


def build_prompt(state: dict[str, object], groups: list[Group]) -> str:
    parts: list[str] = []
    prefixes: list[str] = []

    for group in groups:
        _process_group(group, state, parts, prefixes)

    result_parts = prefixes + parts + ["%command%"]
    return " ".join(result_parts)


def _process_group(
    group: Group,
    state: dict[str, object],
    parts: list[str],
    prefixes: list[str],
) -> None:
    active_exclusive: list[str] = []

    for child in group.children:
        if isinstance(child, Option):
            _process_option(
                child, state, parts, prefixes,
                active_exclusive if group.exclusive_children else [],
            )
        elif isinstance(child, Group):
            _process_group(child, state, parts, prefixes)


def _process_option(
    option: Option,
    state: dict[str, object],
    parts: list[str],
    prefixes: list[str],
    active_exclusive: list[str] | None = None,
) -> None:
    value = state.get(option.key, option.default)

    if option.condition and not option.condition(state):
        return

    if option.requires:
        req_met = all(state.get(req, False) for req in option.requires)
        if not req_met:
            return

    if active_exclusive is not None:
        will_emit = False
        if isinstance(value, bool) and value:
            will_emit = True
        elif isinstance(value, (int, float)) and value != option.default:
            will_emit = True
        elif isinstance(value, str) and value:
            will_emit = True

        if will_emit:
            if len(active_exclusive) > 0:
                return
            active_exclusive.append(option.key)

    if isinstance(value, bool):
        if value:
            if option.prefix:
                prefixes.append(option.prefix)
            elif option.env_key:
                parts.append(f"{option.env_key}=1")
    elif isinstance(value, (int, float)):
        if value != option.default:
            if option.env_key:
                parts.append(f"{option.env_key}={int(value) if value == int(value) else value}")
    elif isinstance(value, str):
        if value:
            if option.cmdlineappend:
                for arg in value.split(","):
                    arg = arg.strip()
                    if arg:
                        parts.append(f"cmdlineappend:{arg}")
            elif option.env_key:
                parts.append(f"{option.env_key}={value}")

    if option.children and value:
        child_exclusive: list[str] = []
        for child in option.children:
            if isinstance(child, Option):
                _process_option(
                    child, state, parts, prefixes,
                    child_exclusive if option.exclusive_children else None,
                )
