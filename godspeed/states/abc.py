from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pygame
from pglib.common import EventInfo

from godspeed.states.enums import States


@dataclass(slots=True)
class GameState(ABC):
    shared_data: Optional[dict] = None
    alive: bool = True
    next_state: Optional[States] = None 

    def __post_init__(self) -> None:
        self.shared_data = {}

    @abstractmethod
    def update(self, event_info: EventInfo) -> None:
        raise NotImplementedError()

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError()
