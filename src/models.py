from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class GroupType(Enum):
    CARD = "card"
    FLAT = "flat"


@dataclass
class Option:
    key: str
    label: str
    tooltip: str = ""
    type: str = "bool"
    default: Any = False
    env_key: str | None = None
    env_value: str | None = None
    prefix: str | None = None
    mutually_exclusive_with: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    condition: Callable[[dict[str, Any]], bool] | None = None
    children: list[Option | Group] = field(default_factory=list)
    exclusive_children: bool = False
    cmdlineappend: bool = False
    placeholder: str = ""
    items: list[str] = field(default_factory=list)
    editable: bool = False
    min_val: int = 0
    max_val: int = 100
    step: int = 1
    scale: float = 1.0


@dataclass
class Group:
    name: str
    label: str
    type: GroupType = GroupType.FLAT
    children: list[Option | Group] = field(default_factory=list)
    exclusive_children: bool = False
