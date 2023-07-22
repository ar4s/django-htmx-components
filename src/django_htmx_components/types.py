from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Trigger:
    event: Optional[str] = None
    after_settle: Optional[dict] = None
    after_swap: Optional[dict] = None
    full_refresh: Optional[bool] = False


@dataclass(frozen=True)
class ComponentContext:
    params: dict
    trigger: Optional[Trigger] = None


@dataclass(frozen=True)
class RenderedComponent:
    content: str
    meta: Optional[Trigger]

