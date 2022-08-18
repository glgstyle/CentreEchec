'''Entry point'''

from controllers.base import BaseController


def main():
    controller = BaseController()
    controller.program_start()


if __name__ == "__main__":

    main()
