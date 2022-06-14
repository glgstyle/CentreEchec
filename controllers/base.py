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
        self.team_of_players = 0
        self.match = Match
        self.round = []
        #self.results = []
        
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
        #Check if value is F or M
        """"while True:
            player.sexe = input("Veuillez entrer son sexe(F/M) : ")
            upper_sexe = player.sexe.upper()
            print(upper_sexe)
            try:
                if not upper_sexe == "F" or not upper_sexe == "M":
                    print(f"voici ce qui n'est pas bon : {upper_sexe}")
                    raise NameError
            except NameError:
                print(f"{upper_sexe} n'est pas pas une valeur valide, veuillez entrer F pour féminin et M pour masculin")
            else:
                break"""

        return(player.firstname, player.name, player.sexe,player.date_of_birth.date())

    def make_a_tournament_team(self):
        """Add players until players list = 8, return the list of players."""
        #while len([self.players]) < 2:  
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = self.add_a_player()
            self.players.append(player)
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
        team = self.make_a_tournament_team()
        tournament_infos.append(team)
        return tournament_infos

    def make_players_pairs(self):
        """Make teams of two, return the list of pairs."""
        tournaments_players = self.players
        number_of_players = len(tournaments_players)
        number_of_teams = 4
        while number_of_players > 0 and number_of_teams > 0:
            # while there is players to put in teams and teams to create, return a list of random players
            self.team_of_players = random.sample(tournaments_players, number_of_players)
            # then decrement the number of teams
            number_of_teams -= 1
        # each pair of player in a variable
        first_team = self.team_of_players[0:2]
        second_team = self.team_of_players[2:4]
        third_team = self.team_of_players[4:6]
        fourth_team = self.team_of_players[6:8]
        # the list of pairs of players
        #pairs_of_players = Match.pair_of_players
        pairs_of_players = first_team, second_team, third_team, fourth_team
        print(f"Les bibômes sont les suivants : \n équipe A :{first_team},\n équipe B :{second_team},\n équipe C :{third_team},\n équipe D :{fourth_team}")
        return pairs_of_players
    
    def start_a_match(self):
        """Create a list to insert the match informations, create a pair of players, when the match ended the ended time is displayed, input the players results in the list, insert the pair of players and their reuslts in match infos"""
        match_infos = []
        pair = self.make_players_pairs()
        self.is_the_match_finished()
        result = self.input_results()
        match_infos.append(pair)
        match_infos.append(result)
        print(f"Match infos : {match_infos}")
        return match_infos

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
        print(f"Ce qui est dans round{round_name}")
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
        self.start_a_round()

    def input_results(self):
        """Input the result of the match, return the player infos with the score inserted."""
        points = Player.points
        #score = Player.score
        # create a variable to insert the player infos with points get per match to each iteration without modify init variable
        players_infos = []
        for player in self.players:
            name = player[1]
            firstname = player[0]
            # As long as the score is incorrect request the score again, then insert it in the player list
            while True:  
                points = input(f"Veuillez entrer le score de joueur {firstname} {name} : ")
                try:        
                    points = float(points)
                    # define the exact place where are inserted the points  
                    liste = (*player, points)    
                    break
                except ValueError:
                    print(f"({points}) n'est pas un score valide veuillez rentrer un chiffre ou un nombre ")  
            players_infos.append(liste)
        self.players = players_infos
        print(f"match terminé, voici les scores : {self.players}")
        return self.players
       
    def update_the_score(self):
        """Calculate players score after tournament, remove each match score from player_list and replace by players infos + final score"""
        # create a variable to insert the player infos with final score
        players_infos = []
        score = Player.score
        print("****** Voici les scores du tournoi : ******")
        #For each player in the list, take the firstname, the name and the match_results in player list
        for player in self.players:
            name = player[1]
            firstname = player[0]
            matchs_results = player[4:]
            score = 0
            #for each match result add the points to the final score 
            for i in matchs_results:
                score += i
                #copy the infos of list players before the match points
                liste = (*player[:4],score)
            #display the firstname and name with the total score
            players_infos.append(liste)
            print(f"{firstname} {name} :{score} points")
            #liste = (*player, score)
        self.players = players_infos
        print(self.players)


controller = Controller()
#tournament = controller.create_a_tournament()
#controller.create_a_tournament()
#controller.make_a_tournament_team()
#tournament = controller.select_random_players()
#controller.make_pair_of_players()
#controller.make_players_pairs()
#controller.input_results()
#controller.get_players_infos()
#controller.start_a_match()
controller.start_a_tournament()
controller.update_the_score()
