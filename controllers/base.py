'''Define the Main Controller'''
from time import strptime
from typing import List

from models.player import Player
#from views.base import View
from models.tournament import Tournament
from datetime import datetime
import random

class Controller:
    def __init__(self):
        '''Has a list of Players and a view.'''
        #models
        self.players = []
        self.tournament = Tournament
        #view
        #self.view = view

    def add_a_player(self):
        player = Player()
        # As long as the name is incorrect request the name again, then insert it in the player list
        while True:          
            player.name = input("Veuillez entrer le nom du joueur : ")
            try:
                if player.name == "":
                    raise TypeError
            except TypeError:
                print("Veuillez rentrer un nom valide")
            else:
                break

        # As long as the firstname is incorrect request the firstname again, then insert it in the player list
        while True:
            player.firstname = input("Veuillez entrer le prénom du joueur : ")
            try:
                if player.firstname == "":
                    raise TypeError
            except TypeError:
                print("Veuillez rentrer un prénom valide")
            else:
                break
        # As long as the date is incorrect request the date again, then reformat the date before inserting it in the player list
        player.date_of_birth = input("Veuillez entrer sa date de naissance : ")
        while True:
            try: 
                player.date_of_birth = datetime.strptime(player.date_of_birth, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                player.date_of_birth = input("Veuillez saisir la date de naissance(jj/mm/aaaa) :")
        player.sexe = input("Veuillez entrer son sexe(F/M) : ")
        """Player.sexe = Player.sexe.upper()
        print(Player.sexe)
        while True:
            try:
                if not Player.sexe == "F" or not Player.sexe =="M":
                    raise NameError
            except NameError:
                print("Veuillez entrer F pour féminin et M pour masculin")
                Player.sexe = input("Veuillez entrer son sexe(F/M) : ")
            else:
                break"""            
        return(player.firstname, player.name, player.date_of_birth.date(), player.sexe)

    def make_a_team_pool(self):
        """Add players until players list = 8, return the list of players."""
        #while len([self.players]) < 2:  
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = self.add_a_player()
            self.players.append([player])
        """for p in self.players:
            print(p)
            print(p.name, p.firstname, p.date_of_birth, p.sexe)"""
        return self.players
    
    def create_a_tournament(self):
        tournament_infos = []
        """Set up a new tournament, return the tournament details and players list."""
        print("--------Création d'un tournoi--------")
        self.tournament.name = input("Veuillez créer un nom pour ce tournoi : ")
        tournament_infos.append(self.tournament.name)
        self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        # As long as the date format is incorrect request the date again, then reformat the date before inserting it 
        while True:
            try: 
                self.tournament.date = datetime.strptime(self.tournament.date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        tournament_infos.append(self.tournament.date)
        self.tournament.place = input("Veuillez saisir le lieu du tournoi :")
        try:
            self.tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            self.tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {self.tournament.numbers_of_turns} ")
        tournament_infos.append(self.tournament.numbers_of_turns)
        team = self.make_a_team_pool()
        tournament_infos.append(team)
        return tournament_infos

    def make_pair_of_players(self):
        pairs_of_players = []
        tournament = self.create_a_tournament()
        tournaments_players = tournament[3]
        print(f"voici la liste de nos joueurs :{tournaments_players}")
        
        for player in tournaments_players:
            p = random.choice(player)
            pairs_of_players.append(p)
            print(f"ce joueur vient d'etre ajouté au tableau des paires{pairs_of_players}")
        """    tournaments_players.remove(p)
            print(f"Voici la nouvelle liste de joueurs avec le dernier joueur supprimé{tournaments_players}")"""


    
controller = Controller()
#tournament = controller.create_a_tournament()
tournament = controller.make_pair_of_players()
