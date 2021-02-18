from typing import NamedTuple, List, Dict, Any
from dataclasses import dataclass, astuple

import random


@dataclass(frozen=True)
class Card:
    name: str = "Empty"

    @property
    def stats(self) -> str:
        return ""

    @property
    def display_name(self) -> str:
        return self.name.upper()

    @property
    def display_text(self) -> str:
        return f"{self.display_name} {self.stats} {self.emoji}".strip()

    @property
    def emoji(self) -> str:
        return "  "

    @property
    def image(self) -> List[str]:
        return [
            "┌─────────┐",
            f"│ {self.display_name.ljust(8)}|",
            "│         │",
            f"│   {self.emoji}    │",
            "│         │",
            f"| {self.stats.rjust(7)} |",
            "└─────────┘",
        ]


@dataclass(frozen=True)
class Champ(Card):
    power: int = 2
    name: str = "Champ"

    @property
    def stats(self) -> str:
        return str(self.power)

    @property
    def emoji(self) -> str:
        return "😈"


@dataclass(frozen=True)
class Punch(Card):
    power: int = 0
    punch_name: str = ""
    name: str = "Punch"

    @property
    def stats(self) -> str:
        return str(self.power) if self.power > 0 else ""

    @property
    def display_name(self) -> str:
        return self.punch_name.upper()

    @property
    def emoji(self) -> str:
        return "🥊"


@dataclass(frozen=True)
class Block(Card):
    protection: int = 2
    power_limit: int = 15
    name: str = "Block"

    @property
    def stats(self) -> str:
        return str(self.protection) + " \ " + str(self.power_limit)

    @property
    def emoji(self) -> str:
        return "🙅"


@dataclass(frozen=True)
class Health(Card):
    health: int = 2
    name: str = "Health"

    @property
    def stats(self) -> str:
        return str(self.health)

    @property
    def emoji(self) -> str:
        return "💊"


@dataclass(frozen=True)
class Player(Card):
    health: int = 21
    name: str = "Player"

    @property
    def stats(self) -> str:
        return str(self.health)

    @property
    def emoji(self) -> str:
        _emoji = "🙂"
        emoji_thresholds = [
            ("🤠", 35),
            ("😤", 25),
            ("🙂", 21),
            ("😕", 18),
            ("🙁", 14),
            ("😬", 11),
            ("😣", 7),
            ("😖", 4),
            ("🥴", 1),
            ("😵", 0),
        ]
        for e, threshold in emoji_thresholds:
            if self.health >= threshold:
                _emoji = e
                break
        return _emoji
