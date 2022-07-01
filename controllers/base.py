'''Define the Main Controller'''
#from os import name
#from time import strptime
#from typing import List
#from datetime import datetime
#import random
#from models import tournament
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View
#from operator import itemgetter, attrgetter
#import json

class Controller:
    def __init__(self):
        '''Has a list of Players and a view.'''
        #models
        self.players = []
        self.tournament = Tournament
        self.match = Match()
        #self.round = []

    def make_a_tournament_team(self):
        """Add players until players list = 8, return the list of players."""
        Player.clean_table()
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = Player.add_a_player()
            self.players.append(player)
            Player.insert_player_in_database(player)
    
    def create_a_tournament(self):
        """Set up a new tournament"""
        View.display_create_a_tournament(self.tournament)
        self.make_a_tournament_team()
        Tournament.insert_tournament_in_database(self.tournament)

    def sort_players_by_rank(self):
        """Sort the list of players sorted by rank, return the sorted list"""
        sorted_by_rank = sorted(self.players, key=lambda player: player.rank)
        return sorted_by_rank

    def make_players_pairs(self):
        """Divide sorted players in two half, the best player of upper half play against the best player of lower half etc..."""
        sorted_players_by_rank = self.sort_players_by_rank()
        half = len(sorted_players_by_rank) / 2
        half = int(half)
        upper_half = sorted_players_by_rank[0:half] 
        lower_half = sorted_players_by_rank[half:len(sorted_players_by_rank)]
        first_team = upper_half[0], lower_half[0]
        second_team = upper_half[1], lower_half[1]
        third_team = upper_half[2], lower_half[2]
        fourth_team = upper_half[3], lower_half[3]
        # the list of pairs of players
        self.list_of_teams = [first_team , second_team , third_team , fourth_team]
        print(f"Les bibômes sont les suivants :\n\nEquipe A :")
        View.display_team(self.list_of_teams[0])
        print(f"\nEquipe B :")
        View.display_team(self.list_of_teams[1])
        print(f"\nEquipe C :")
        View.display_team(self.list_of_teams[2])
        print(f"\nEquipe D :")
        View.display_team(self.list_of_teams[3])
        return self.list_of_teams
    
    def find_all_players_in_rounds(self):
        """Look for all teams of players by round and list them together"""
        players_in_rounds=[]
        for round in self.rounds:
            #print(f"les joueurs du round : {round.players}")
            players_in_rounds.append(round.players)
        #print(f"players in rounds : {players_in_rounds}")  
        return players_in_rounds

    def make_players_pairs_by_score_or_rank(self):
        """Make players pairs by score or rank after the first round by checking if they have already played together"""
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        players_in_rounds = self.find_all_players_in_rounds()
        players= sorted_by_score_or_rank
        #print(f"players : {players}")
        teams=[]
        #While there is players, remove the first and the second player of the list
        while(len(players)>0):
            a=players.pop(0)
            b=players.pop(0)
            #for lists of teams in rounds and for team in list of teams, check if they have already play together
            for competitors in players_in_rounds:
                for competitor in competitors:
                    #if they have play together, put back b in list and take the first of the list as b, then rearrange the list as it was initially(put c in first index)
                    if(competitor[0]==a and competitor[1]==b or competitor[0]==b and competitor[1]==a):
                        #print(a,b, "------deja joué ensemble")
                        players.append(b)
                        #print(f"------on remet {b} dans liste",players)
                        b=players.pop(0)
                        #print(f"-----on prend {b} le premier de ",players )
                        if len(players) > 0:
                            c=players.pop()
                            players.insert(0, c)
                        #print("------on trie de nouveau ",players)  
            print("team", a,b)
            teams.append([a,b])
        print(f"Les bibômes sont les suivants :\n\nEquipe A :")
        View.display_team(teams[0])
        print(f"\nEquipe B :")
        View.display_team(teams[1])
        print(f"\nEquipe C :")
        View.display_team(teams[2])
        print(f"\nEquipe D :")
        View.display_team(teams[3])
        return teams

    def sort_players_by_score_then_rank(self):
        """Sorted the list of players by score first and if score is equal, sort them by rank"""
        #-x.score is the reverse order because we need the most important score first and the first of rank, second after etc....
        sorted_by_score_then_rank = sorted(self.players, key=lambda x: (-x.score, x.rank))
        return sorted_by_score_then_rank

    def match_record(self):
        """Record the players in a match and return them"""
        players_in_match = []
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        for player in sorted_by_score_or_rank:
            players_in_match.append(player)
        return players_in_match

    def results_of_match(self):
        """Input the players results in the list, insert the pair of players and their reuslts in match """
        self.match.player_match_result = self.input_results()
        self.match.pair_of_players = self.match_record()

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
            round.start_time = View.start_time(round)
            round.end_time = View.is_the_match_finished(round)
            round.results = self.results_of_match()
            round.players = self.list_of_teams
            self.update_the_score()
            self.rounds.append(round)
        for i in list_name_round[1:len(list_name_round)]:
            round = Round()
            round.name = i
            print(i)
            round.players = self.make_players_pairs_by_score_or_rank()
            input("Appuyez sur entrée pour démarrer le match")
            round.start_time = View.start_time(round)
            round.end_time = View.is_the_match_finished(round)
            round.results = self.results_of_match()
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
        View.display_match_score(self) 
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