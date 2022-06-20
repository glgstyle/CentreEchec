'''Define the Main Controller'''
from os import name
from time import strptime
from typing import List
from datetime import datetime
import random
import math

from models.player import Player
#from views.base import View
from models.tournament import Tournament
from models.match import Match
from models.round import Round


class Controller:
    def __init__(self):
        '''Has a list of Players and a view.'''
        #models
        self.players = []
        self.tournament = Tournament
        self.match = Match()
        self.round = []
        #self.results = []
        
        #view
        #self.view = view

    def make_a_tournament_team(self):
        """Add players until players list = 8, return the list of players."""
        #player = Player()
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = Player.add_a_player()
            print(f"ici les points {player.points}")
            self.players.append(player)
        """for p in self.players:
            #print(p)
            print(p.name, p.firstname, p.date_of_birth, p.sexe)"""
    
    def create_a_tournament(self):
        #tournament_infos = []
        """Set up a new tournament, return the tournament details and players list."""
        print("--------Création d'un tournoi--------")
        self.tournament.name = input("Veuillez créer un nom pour ce tournoi : ")
        #tournament_infos.append(self.tournament.name)
        self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        # As long as the date format is incorrect request the date again, then reformat the date before inserting it 
        while True:
            try: 
                self.tournament.date = datetime.strptime(self.tournament.date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        #tournament_infos.append(self.tournament.date)
        self.tournament.place = input("Veuillez saisir le lieu du tournoi :")
        try:
            self.tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            self.tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {self.tournament.numbers_of_turns} ")
        #tournament_infos.append(self.tournament.numbers_of_turns)
        self.make_a_tournament_team()
        #tournament_infos.append(team)
        
    def display_team(self, team):
        for player in team:
            print(player.name, player.firstname)

    def make_players_pairs(self):
        """Make teams of two, return the list of pairs."""
        #print(self.players)
        # while there is players to put in teams and teams to create, return a list of random players
        random.shuffle(self.players)
        print(f"*********Team of players = {self.players}")
        # each pair of player in a variable
        first_team = self.players[0:2]
        second_team = self.players[2:4]
        third_team = self.players[4:6]
        fourth_team = self.players[6:8]
        # the list of pairs of players
        self.list_of_teams = [first_team , second_team , third_team , fourth_team]
        print(self.list_of_teams)
        #i = 0 
        #for team in self.list_of_teams:
            #i += 1
            #print("team",i)
            #for player in team:
                #print(player.name, player.firstname)

        print(f"Les bibômes sont les suivants :\n\nEquipe A :")
        self.display_team(self.list_of_teams[0])
        print(f"\nEquipe B :")
        self.display_team(self.list_of_teams[1])
        print(f"\nEquipe C :")
        self.display_team(self.list_of_teams[2])
        print(f"\nEquipe D :")
        self.display_team(self.list_of_teams[3])
        
        return self.players
    
    def start_a_match(self):
        """Create a list to insert the match informations, create a pair of players, when the match ended the ended time is displayed, input the players results in the list, insert the pair of players and their reuslts in match infos"""
        self.match.pair_of_players = self.make_players_pairs()
        self.is_the_match_finished()
        self.match.player_match_result = self.input_results()
        print(f"Match infos les scores: {self.match.player_match_result}")
        return self.match


    def is_the_match_finished(self):
        input("Appuyez sur entrée lorsque le match est terminé.")
        self.end_time()
    

    def start_time(self):
        """Define the time when start the match."""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Heure de démarrage : {current_time}")
        return current_time
    
    def end_time(self):
        """Define the time when end the match."""
        now = datetime.now()
        actual_time = now.strftime("%H:%M:%S")
        print(f"Heure de fin : {actual_time}")

    def name_a_round(self):
        """Copy the number of turns in tournament to get an iteration of round, then return the name of rounds."""
        round_number = self.tournament.numbers_of_turns
        round_name = []
        for i in range(round_number):
            round_name.append(f"Round {i+1}")
        return round_name

    def start_a_round(self):
        """Start to give a name to the round then until ther is no more round, start a new match."""
        round_name = self.name_a_round()
        while self.tournament.numbers_of_turns > 0:
            self.tournament.numbers_of_turns = self.tournament.numbers_of_turns -1
        #print(f"Ce qui est dans round{round_name}")
        for i in round_name:
            print(i)
            input("Appuyez sur entrée pour démarrer le match")
            start_time = self.start_time()
            match = self.start_a_match()
            self.round.append(i)
            self.round.append(start_time)
            self.round.append(match)
        #break
        print(f"Voici les infos du self.round{self.round}")

            
    def start_a_tournament(self):
        """Starting processus of tournament, create a tournament with players... and a round with them."""
        self.create_a_tournament()
        #print(self.players)
        self.start_a_round()

    def input_results(self):
        """Input the result of the match, return the player infos with the score inserted."""
        for pair in self.list_of_teams:
            for player in pair:
                # As long as the score is incorrect request the score again, then insert it in the player list
                while True:  
                    points = input(f"Veuillez entrer le score de joueur {player.firstname} {player.name} : ")
                    try:        
                        points = float(points)
                        # Copy the existing player points and add the new points  
                        player.points = [*player.points , points]
                        break
                    except ValueError:
                        print(f"({points}) n'est pas un score valide veuillez rentrer un chiffre ou un nombre ")  
        for player in self.players:
            print(player.name, player.firstname, player.points)
        #print("match terminé, voici les scores :")
        """player_pair = []
        for pair in self.match.pair_of_players : 
            print(pair)
            for p in pair:
                player_pair.append(p[0] + " " + p[1])
                #player_pair.append(p[1])
        print(player_pair)
        #print(f"Dans le match opposant {player_pair[0]} contre {player_pair[1]}: {player_pair[0]} a obtenu le score de {match_points[0]} et {player_pair[1]} a obtenu le score de {match_points[1]}")
            
        
        for player in self.players:
            print(f"Dans le match qui a opposé {player[1]} {player[0]} contre rien" )
            for player in list(pair):
                print(f"***ici le player:{player}")
                print(f"{player[1]} {player[0]} à obtenu le score de :{players_points}")
                
            #for points in self.match.player_match_result:"""
                    
        return self.players
       
    def update_the_score(self):
        """Calculate players score after tournament by doing the sum of player points"""
        print("****** Voici les scores du tournoi : ******")
        #For each player in the list, take the firstname, the name and the match_results in player list
        for player in self.players:
            player.score = 0
            #for each match add the points to the final score 
            for points in player.points:
                player.score += points
            #display the player with his score
            print(f"{player.firstname} {player.name} :{player.score} points")
        print(self.players)


controller = Controller()
controller.start_a_tournament()
controller.update_the_score()
