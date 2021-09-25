from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Stack:
    index: int
    prev: Optional[Stack] = None


s = Stack(index=0)

reveal_type(s)
reveal_type(s.index)
