'''Define the Main Controller'''
from os import name
from time import strptime
from typing import List
from datetime import datetime
import random
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

    def make_a_tournament_team(self):
        """Add players until players list = 8, return the list of players."""
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = Player.add_a_player()
            self.players.append(player)
    
    def create_a_tournament(self):
        """Set up a new tournament"""
        print("--------Création d'un tournoi--------")
        self.tournament.name = input("Veuillez créer un nom pour ce tournoi : ")
        self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        # As long as the date format is incorrect request the date again, then reformat the date before inserting it 
        while True:
            try: 
                self.tournament.date = datetime.strptime(self.tournament.date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                self.tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        self.tournament.place = input("Veuillez saisir le lieu du tournoi :")
        try:
            self.tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            self.tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {self.tournament.numbers_of_turns} ")
        self.make_a_tournament_team()
        
    def display_team(self, team):
        """Print the competitor list in shuffle order(already done in function make_players_pairs)"""
        for player in team:
            print(player.name, player.firstname)

    def make_players_pairs(self):
        """Make teams of two, return the list of players."""
        # while there is players to put in teams and teams to create, return a list of random players
        random.shuffle(self.players)
        # each pair of player in a variable
        first_team = self.players[0:2]
        second_team = self.players[2:4]
        third_team = self.players[4:6]
        fourth_team = self.players[6:8]
        # the list of pairs of players
        self.list_of_teams = [first_team , second_team , third_team , fourth_team]
        print(f"Les bibômes sont les suivants :\n\nEquipe A :")
        self.display_team(self.list_of_teams[0])
        print(f"\nEquipe B :")
        self.display_team(self.list_of_teams[1])
        print(f"\nEquipe C :")
        self.display_team(self.list_of_teams[2])
        print(f"\nEquipe D :")
        self.display_team(self.list_of_teams[3])
        return self.players
    
    def match_record(self):
        """Record the players in a match and return them"""
        players_in_match = []
        for player in self.players:
            players_in_match.append([player.firstname , player.name, player.points])
        return players_in_match

    def results_of_match(self):
        """Input the players results in the list, insert the pair of players and their reuslts in match """
        self.match.player_match_result = self.input_results()
        self.match.pair_of_players = self.match_record()

    def is_the_match_finished(self):
        """Ask to press enter when the match is finished and record the end time"""
        input("Appuyez sur entrée lorsque le match est terminé.")
        return self.end_time()

    def start_time(self):
        """Define the time when start the match."""
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de démarrage : {current_time}")
        return current_time
    
    def end_time(self):
        """Define the time when end the match."""
        now = datetime.now()
        actual_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de fin : {actual_time}")
        return actual_time

    def name_a_round(self):
        """Copy the number of turns in tournament to get an iteration of round, then return the name of rounds."""
        round_number = self.tournament.numbers_of_turns
        round_name = []
        for i in range(round_number):
            round_name.append(f"Round {i+1}")
        return round_name

    def start_a_round(self):
        """Start to give a name to the round then until there is no more round, start a new match."""
        round_name = self.name_a_round()
        while self.tournament.numbers_of_turns > 0:
            self.tournament.numbers_of_turns = self.tournament.numbers_of_turns -1  
        #for each round, create pairs of players, append start, end time and players pairs with their score in a round 
        for i in round_name:
            print(i)
            self.make_players_pairs()
            input("Appuyez sur entrée pour démarrer le match")
            start_time = self.start_time()
            self.round.append(i)
            self.round.append(start_time)
            end_time = self.is_the_match_finished()
            self.round.append(end_time)
            self.results_of_match()
            self.round.append(self.match.pair_of_players)
        print(f"**********Voici les infos des rounds{self.round}")
            
    def start_a_tournament(self):
        """Starting processus of tournament, create a tournament with players... and a round with them."""
        self.create_a_tournament()
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
        print("*****Match terminé, vosici les scores :*****")
        for player in self.players:
            print(player.name, player.firstname, player.points)
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


controller = Controller()
controller.start_a_tournament()
controller.update_the_score()
