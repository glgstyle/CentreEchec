'''Entry point'''


from controllers.base import Controller
#from models.player import Player
from ControlPanelCentreEchec.widget import Widget
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
import sys



def main():
    controller = Controller()
    controller.start_a_tournament()


if __name__ == "__main__":
    #Widget.window()
    main()
