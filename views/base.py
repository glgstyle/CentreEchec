'''Base view'''

#from controllers import base
from models import player
from models.player import Player

class View:
    '''Chess game.'''

    def __init__(self):
        '''Define the view.'''

    def prompt_for_player(self):
        '''Ask for name.'''
        name = player.__name__(input("Veuillez le nom de famille du joueur"))
        #name = input("Veuillez le nom de famille du joueur")
        if not name: #or firstname or date_of_birth or sexe :
            return None
        return name # firstname, date_of_birth, sexe
