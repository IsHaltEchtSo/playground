from model.numbergame import GuessNumber
from model.janken import Janken
from controller.GameControllerClass import GameController

# init the controller and its games
guess_game = GuessNumber()
janken     = Janken()
controller = GameController()
controller.register_game('number_guess', guess_game)
controller.register_game('janken', janken)