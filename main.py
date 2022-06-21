'''Entry point'''

from controllers.base import Controller
from models.player import Player

def main():
    controller = Controller()
    controller.start_a_tournament()
    controller.update_the_score()

if __name__ == "__main__":
    main()

