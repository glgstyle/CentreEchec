'''Entry point'''

from controllers.base import BaseController
import os


def main():
    # Try to create Database repertory
    path = 'Database/'
    if not os.path.exists(path):
        os.makedirs(path)
    controller = BaseController()
    controller.program_start()


if __name__ == "__main__":
    main()
