import pygame

from godspeed.states.enums import States
from godspeed.states.world import World
from godspeed.states.main_menu import MainMenu
from godspeed.states.death_screen import DeathScreen

from pglib.common import EventInfo


class StateManager:
    """
    A class that manages - creates, updates and draws 
    all game states present in the game. 
    """
    
    def __init__(self, starting_state: States) -> None:
        self.states = [MainMenu, World, DeathScreen]
        self.current_state = starting_state
        self.state = self.states[self.current_state.value]

        # Some data stored by each state that is meant to be 
        # accessed by other states
        self.shared_data = {}
    
    def handle_state_switching(self) -> None:
        self.shared_data[self.state.next_state] = self.state.shared_data.copy()
        self.current_state = self.state.next_state 
        self.state = self.states[self.current_state.value]

    def update(self, event_info: EventInfo) -> None:
        self.state.update(event_info)
    
    def draw(self, screen: pygame.Surface) -> None:
        self.state.draw(screen)
        





