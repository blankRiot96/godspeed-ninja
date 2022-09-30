from typing import Any

import pygame
from pglib.common import EventInfo

from godspeed.states.death_screen import DeathScreen
from godspeed.states.enums import States
from godspeed.states.main_menu import MainMenu
from godspeed.states.world import World


class StateManager:
    """
    A class that manages - creates, updates and draws
    all game states present in the game.
    """

    def __init__(self, starting_state: States) -> None:
        self.states = [MainMenu, World, DeathScreen]
        self.current_state = starting_state
        self.state = self.get_state_instance()

        # Some data stored by each state that is meant to be
        # accessed by other states
        self.shared_data = {}

    def get_state_instance(self) -> Any:
        state_type = self.states[self.current_state.value - 1]

        return state_type()

    def handle_state_switching(self) -> None:
        self.shared_data[self.current_state] = self.state.shared_data.copy()
        self.current_state = self.state.next_state
        self.state = self.get_state_instance()
        self.state.receive_data = self.shared_data

    def update(self, event_info: EventInfo) -> None:
        self.state.update(event_info)

        if not self.state.active:
            self.handle_state_switching()

    def draw(self, screen: pygame.Surface) -> None:
        self.state.draw(screen)
