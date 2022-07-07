'''Entry point'''

from controllers.base import Controller


def main():
    controller = Controller()
    controller.start_a_tournament()

if __name__ == "__main__":
    main()
