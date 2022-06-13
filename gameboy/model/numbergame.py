from random import randint
from .abstractclass import Game

class GuessNumber(Game):
    magic_number: int = randint(1,19)
    guess_count: int = 0
    is_running: bool = True

    def run(self):
        """starts the game loop"""
        while self.is_running:
            number = input('\nu know da magic namba? ')
            self.guess_count += 1

            try:
                number = int(number)

            except ValueError:
                print('please enter a valid number')
                continue

            # secret game loop backdoor
            if number == 666:
                self.is_running = False
                break

            # game finished
            if number == self.magic_number:
                print(f"you only needed {self.guess_count} guesses!")
                print(f"congratulations! the magic number was {self.magic_number}")
                self.guess_count = 0
                keep_plaing = input("\n-> do you want to keep playing? [y/any]")

                if (keep_plaing != 'y'):
                    self.is_running = False

            # give hint
            if number > self.magic_number:
                print(f"-> the magic number is smaller than {number}")

            # give hint
            if number < self.magic_number:
                print(f"-> the magic number is bigger than {number}")