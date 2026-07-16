from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PromptState:
    bool_options: dict[str, bool] = field(default_factory=dict)
    text_options: dict[str, str] = field(default_factory=dict)
    slider_options: dict[str, float] = field(default_factory=dict)


def build_prompt(state: PromptState, options: dict, exclusive_groups: list) -> str:
    parts: list[str] = []
    disabled_vars: set[str] = set()

    active_booleans = {name for name, val in state.bool_options.items() if val}

    for group in exclusive_groups:
        active_in_group = [name for name in group.options if name in active_booleans]
        if len(active_in_group) > 1:
            for name in active_in_group[1:]:
                active_booleans.discard(name)

    for name in active_booleans:
        opt = options.get(name)
        if opt is None:
            continue
        for req in opt.requires:
            if req not in active_booleans:
                disabled_vars.add(opt.env_var)
                break
        if opt.env_var in disabled_vars:
            continue
        value = "1"
        parts.append(f"{opt.env_var}={value}")

    for name, value in state.text_options.items():
        if not value.strip():
            continue
        opt = options.get(name)
        if opt is None:
            continue
        if opt.requires:
            req_met = any(r in active_booleans for r in opt.requires)
            if not req_met:
                continue
        if opt.env_var == "cmdlineappend":
            for part in value.split(","):
                part = part.strip()
                if part:
                    parts.append(f"cmdlineappend:{part}")
        else:
            parts.append(f"{opt.env_var}={value}")

    for name, value in state.slider_options.items():
        opt = options.get(name)
        if opt is None:
            continue
        if opt.requires:
            req_met = any(r in active_booleans for r in opt.requires)
            if not req_met:
                continue
        if value == opt.default_value:
            continue
        parts.append(f"{opt.env_var}={int(value) if value == int(value) else value}")

    parts.append("%command%")
    return " ".join(parts)
