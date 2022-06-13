from random import randint
from typing import Any, Dict
from model.abstractclass import Game


class GameController:
    games: Dict[str, Game] = {}
    state: str
    selected_game: Game = Any
    is_running: bool = True

    def clear_selected_game(self):
        """makes the controller go virgin again"""
        self.selected_game = None

    def register_game(self, name:str, game: Game) -> None:
        """registers a game to play on the controller"""
        self.games[name] = game

    def set_state_by_user(self) -> None:
        """
        1) Start Guess Game \n
        2) Start Game of Janken \n
        3) Quit controller
        """
        print("\nGAME MENU:\n1) Start Guess Game\n2) Start Game of Janken\n3) Quit")
        self.state = input('ENTER: ')

        if self.state == '1':
            self.selected_game = self.games['number_guess']

        if self.state == '2':
            self.selected_game = self.games['janken']

        if self.state == '3':
            self.is_running = False