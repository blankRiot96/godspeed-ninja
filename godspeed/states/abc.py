from abc import ABC
from typing import Optional

from godspeed.states.enums import States


class GameState(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.active = True
        self.next_state: Optional[States] = None
        self.shared_data = {}
        self.receive_data = {}
