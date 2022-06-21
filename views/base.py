'''Base view'''

#from controllers import base
from models import player
from models.player import Player
from models.round import Round

class View:
    '''Chess game.'''

    def __init__(self):
        '''Define the view.'''

    def display_infos_rounds(rounds):
        #print(round.start_time)
        print(f"**********Voici les infos des rounds{rounds}")
        for round in rounds:
            print(f"Dans le round : {round.name}")
            print(f"qui s'est joué le {round.start_time}")
            print(f"et s'est terminé le {round.end_time}")
            print(f"avec les joueurs suivants : {round.players}")
            print(f"Voici les résultats : {round.results}")