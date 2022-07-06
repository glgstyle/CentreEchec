# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from controllers.base import Controller



class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def initUi(self):
        # creation du bouton
        self.bouton = QPushButton("mon bouton avec une gestion d'appui")

        # on connecte le signal "clicked" a la methode appui_bouton
        self.bouton.clicked.connect(self.click_on_button())

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def click_on_button(self):
        print("ok")
        self.controller = Controller()
        self.controller.start_a_tournament()
        
#fen = Fenetre()
#fen.show()

        

#if __name__ == "__main__":
    def window():
        app = QApplication([])
        widget = Widget()
        widget.show()
        sys.exit(app.exec_())
