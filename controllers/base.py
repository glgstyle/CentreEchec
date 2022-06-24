'''Define the Main Controller'''
from os import name
from time import strptime
from typing import List
from datetime import datetime
import random
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View
from operator import itemgetter, attrgetter


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

    def sort_players_by_rank(self):
        """Print the list of players sorted by rank, return the sorted list"""
        sorted_by_rank = sorted(self.players, key=lambda player: player.rank)
        print(sorted_by_rank)
        return sorted_by_rank

    """def make_players_pairs(self):
        #Make teams of two, return the list of players.
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
        return self.players"""
    def make_players_pairs(self):
        """Divide sorted players in two half, the best player of upper half play against the best player of lower half etc..."""
        sorted_players_by_rank = self.sort_players_by_rank()
        half = len(sorted_players_by_rank) / 2
        half = int(half)
        upper_half = sorted_players_by_rank[0:half] 
        lower_half = sorted_players_by_rank[half:len(sorted_players_by_rank)]
        print(upper_half)
        print(lower_half)
        first_team = upper_half[0], lower_half[0]
        second_team = upper_half[1], lower_half[1]
        third_team = upper_half[2], lower_half[2]
        fourth_team = upper_half[3], lower_half[3]
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

    def make_players_pairs_by_score_or_rank(self):
        """Make players pairs by score or rank after the first round"""
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        team1 = sorted_by_score_or_rank[0:2]
        team2 = sorted_by_score_or_rank[2:4]
        team3 = sorted_by_score_or_rank[4:6]
        team4 = sorted_by_score_or_rank[6:8]
        # the list of pairs of players
        self.teams = [team1 , team2 , team3 , team4]
        print(f"Les bibômes sont les suivants :\n\nEquipe A :")
        self.display_team(self.teams[0])
        print(f"\nEquipe B :")
        self.display_team(self.teams[1])
        print(f"\nEquipe C :")
        self.display_team(self.teams[2])
        print(f"\nEquipe D :")
        self.display_team(self.teams[3])

    def sort_players_by_score_then_rank(self):
        """Sorted the list of players by score first and if score is equal, sort them by rank"""
        #-x.score is the reverse order because we need the most important score first and the first of rank, second after etc....
        sorted_by_score_then_rank = sorted(self.players, key=lambda x: (-x.score, x.rank))
        return sorted_by_score_then_rank

    def match_record(self):
        """Record the players in a match and return them"""
        players_in_match = []
        for player in self.players:
            #players_in_match.append([player.firstname , player.name, player.points])
            players_in_match.append(player)
        return players_in_match

    def results_of_match(self):
        """Input the players results in the list, insert the pair of players and their reuslts in match """
        self.match.player_match_result = self.input_results()
        """for player in self.match.player_match_result:
            print(f"//les points {player.points}")
        print(f"//////player match result{self.match.player_match_result}")"""
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
        round_name = []
        for i in range(self.tournament.numbers_of_turns):
            round_name.append(f"Round {i+1}")
        return round_name

    def start_a_round(self):
        """Start to give a name to the round then until there is no more round, start a new match."""
        self.rounds = []
        list_name_round = self.name_a_round()
        #for each round, create pairs of players, append start, end time and players pairs with their score in a round 
        for i in list_name_round[0:1]:
            round = Round()
            round.name = i
            print(i)
            #***
            self.make_players_pairs()
            input("Appuyez sur entrée pour démarrer le match")
            round.start_time = self.start_time()
            round.end_time = self.is_the_match_finished()
            round.results = self.results_of_match()
            round.players = self.match.pair_of_players
            self.update_the_score()
            self.rounds.append(round)
        for i in list_name_round[1:len(list_name_round)]:
            round = Round()
            round.name = i
            print(i)
            #***
            #self.sort_players_by_score_then_rank()
            self.make_players_pairs_by_score_or_rank()
            input("Appuyez sur entrée pour démarrer le match")
            round.start_time = self.start_time()
            round.end_time = self.is_the_match_finished()
            round.results = self.results_of_match()
            round.players = self.match.pair_of_players
            self.update_the_score()
            self.rounds.append(round)
        View.display_infos_rounds(self.rounds)   

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
        """Calculate players score by doing the sum of player points"""
        print("****** Voici les scores des joueurs : ******")
        #For each player in the list, take the firstname, the name and the match_results in player list
        for player in self.players:
            player.score = 0
            #for each match add the points to the final score 
            for points in player.points:
                player.score += points
            #display the player with his score
            print(f"{player.firstname} {player.name} :{player.score} points")

