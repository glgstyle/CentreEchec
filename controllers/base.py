'''Define the Main Controller'''

from unicodedata import name
from xml.dom.minidom import Identified
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View
from rich.table import Table
from rich.console import Console
from tinydb import TinyDB, Query, JSONStorage
from tinydb_serialization import SerializationMiddleware
import uuid


class Controller:
    def __init__(self):
        '''Has a list of Players and a view.'''
        #models
        self.tournament = Tournament()
        self.tournament.players = []
        #self.players = [] #relier au tournoi et les rounds au tournoi, (essayer de faire des menus), faire des fonctions uniques pour les vues (dans View)
        self.match = Match()
        self.round = Round()
        self.tournament.rounds = []
        
    def make_a_tournament_team(self):
        """Add players until players list = 8, return the list of players."""
        Player.clean_table()
        pool = 0
        while pool < 8:  
            pool = pool + 1
            player = Player.add_a_player()
            self.tournament.players.append(player)
            #Player.insert_player_in_database(player)
    
    def create_a_tournament(self):
        """Set up a new tournament."""
        View.display_create_a_tournament(self.tournament)
        self.tournament.id = uuid.uuid4().hex
        option = View.display_add_players_or_not()
        if option == "1":
            self.make_a_tournament_team()
            View.display_tournament_record()
        elif option == "2":
            View.display_players_by_alphabetical_order()
            ids = self.select_players()
            #print(ids)
            #self.tournament.players.append(id)
            for i in ids:
                p = Player.search_player_by_id(i)
                self.tournament.players.append(p)
            # insert in database
        self.tournament.insert_tournament_in_database()

    def select_players(self):
        #View.display_players_by_alphabetical_order()
        choices = []
        list_of_players = 0
        while list_of_players < 8:
            list_of_players += 1
            id = View.display_select_players()
            choices.append(id)
        return choices

    def sort_players_by_rank(self):
        """Sort the list of players by rank, return the sorted list."""
        print(self.tournament.players)
        sorted_by_rank = sorted(self.tournament.players, key=lambda player: player.rank)
        return sorted_by_rank

    def make_players_pairs(self):
        """Divide sorted players in two half, the best player of upper half play against the best player of lower half etc...Return the list of teams."""
        sorted_players_by_rank = self.sort_players_by_rank()
        print(sorted_players_by_rank)
        half = len(sorted_players_by_rank) / 2
        half = int(half)
        upper_half = sorted_players_by_rank[0:half] 
        lower_half = sorted_players_by_rank[half:len(sorted_players_by_rank)]
        first_team = upper_half[0], lower_half[0]
        second_team = upper_half[1], lower_half[1]
        third_team = upper_half[2], lower_half[2]
        fourth_team = upper_half[3], lower_half[3]
        # the list of pairs of players
        self.list_of_teams = [(first_team) , (second_team) , (third_team) , (fourth_team)]
        print("**********",self.list_of_teams)
        #self.match.pair_of_players = (self.list_of_teams[0]), (self.list_of_teams[1]), (self.list_of_teams[2]), (self.list_of_teams[3])
        for team in self.list_of_teams:
            self.match.pair_of_players.append(team)
        #self.match.pair_of_players.append(self.list_of_teams[0])
        """self.match.pair_of_players.append(self.list_of_teams[1])
        self.match.pair_of_players.append(self.list_of_teams[2])
        self.match.pair_of_players.append(self.list_of_teams[3])"""
        #print("******self.round.matchs :", self.round.matchs)
        View.display_all_teams_in_first_round(list_of_teams=self.list_of_teams)
        return self.list_of_teams
    
    def find_all_players_in_rounds(self):
        """Look for all teams of players by round and list them together..."""
        players_in_rounds=[]
        for round in self.tournament.rounds:
            players_in_rounds.append(round.players)
        return players_in_rounds

    def make_players_pairs_by_score_or_rank(self):
        """Make players pairs by score or rank after the first round by checking if they have already played together."""
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        players_in_rounds = self.find_all_players_in_rounds()
        players= sorted_by_score_or_rank
        teams=[]
        # while there is players, remove the first and the second player of the list
        while(len(players)>0):
            a=players.pop(0)
            b=players.pop(0)
            #for lists of teams in rounds and for team in list of teams, check if they have already play together
            for competitors in players_in_rounds:
                for competitor in competitors:
                    #if they have play together, put back b in list and take the first of the list as b, then rearrange the list as it was initially(put c in first index)
                    if(competitor[0]==a and competitor[1]==b or competitor[0]==b and competitor[1]==a):
                        players.append(b)
                        b=players.pop(0)
                        if len(players) > 0:
                            c=players.pop()
                            players.insert(0, c)
            teams.append([a,b])
        View.display_all_teams_after_first_round(teams)
        return teams

    def sort_players_by_score_then_rank(self):
        """Sorted the list of players by score first and if score is equal, sort them by rank."""
        #-x.score is the reverse order because we need the most important score first and the first of rank, second after etc....
        sorted_by_score_then_rank = sorted(self.tournament.players, key=lambda x: (-x.score, x.rank))
        return sorted_by_score_then_rank

    def match_record(self):
        """Record the players in a match and return them."""
        players_in_match = []
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        for player in sorted_by_score_or_rank:
            players_in_match.append(player)
        return players_in_match

    def results_of_match(self):
        """Input the players results in the list, insert the pair of players and their results in match."""
        self.match.player_result = self.input_results()
        self.match_record()
        #self.match.pair_of_players
        print("******self.match.pair_of_players", self.match.pair_of_players)
        #self.match.pair_of_players = self.list_of_teams
        
    def name_a_round(self):
        """Copy the number of turns in tournament to get an iteration of round, then return the name of rounds."""
        round_name = []
        for i in range(self.tournament.numbers_of_turns):
            round_name.append(f"Round {i+1}")
        return round_name

    def start_a_round(self):
        """Start to give a name to the round then until there is no more round, start a new match."""
        console = Console()
        #self.rounds = []
        list_name_round = self.name_a_round()
        #for each round, create pairs of players, append start, end time and players pairs with their score in a round 
        for i in list_name_round[0:1]:
            round = Round()
            round.name = i
            View.display_round_name(round=i)
            round.players = self.make_players_pairs()
            print("*******round.players", round.players[0])
            console.input("\n[bold red]Appuyez sur entrée pour démarrer le match[/]")
            round.start_time = View.start_time()
            round.end_time = View.is_the_match_finished()
            self.results_of_match()
            #round.matchs.append(self.results_of_match())
            self.update_the_score()
            self.tournament.rounds.append(round)
            Tournament.update_rounds_in_tournament_database(id=self.tournament.id, rounds=self.tournament.rounds)
        for i in list_name_round[1:len(list_name_round)]:
            round = Round()
            round.name = i
            View.display_round_name(round=i)
            round.players = self.make_players_pairs_by_score_or_rank()
            console.input("\n[bold red]Appuyez sur entrée pour démarrer le match[/]")
            round.start_time = View.start_time()
            round.end_time = View.is_the_match_finished()
            self.results_of_match()
            self.update_the_score()
            self.tournament.rounds.append(round)
            Tournament.update_rounds_in_tournament_database(id=self.tournament.id, rounds=self.tournament.rounds)
        self.update_player_rank()
        View.display_infos_rounds(self.tournament.rounds)   

    def program_start(self):
        """Show the title program, open the mainmenu with options to select."""
        View.menuTitle()
        self.main_menu()
    
    def main_menu(self):
        while True:
            option = View.display_main_menu()
            if option == "1":
                self.tournament_submenu()
                break
            elif option == "2":
                self.players_submenu()
                break
            elif option == "3":
                self.rapports_submenu()
                break

    def tournament_submenu(self): 
        while True:
            option = View.display_tournament_submenu()
            if option == "1":
                self.start_a_tournament()
                option
            elif option == "2":
                self.replay_tournament_by_id()
                self.start_a_round()
                option
            elif option == "3":
                self.main_menu()
                option

    def choose_an_existing_tournament(self):
        """Return the tournament object"""
        View.display_all_tournaments()
        choice = View.display_select_tournament()
        return choice
    
    def replay_tournament_by_id(self):
        """Replay an existing tournament with the same players."""
        id = self.choose_an_existing_tournament()
        self.tournament.id = id
        tournament = Tournament.search_tournament_by_id(id)
        ids = tournament.players
        for i in ids:
            print(i)
            player = Player.search_player_by_id(i)
            print(player)
            self.tournament.players.append(player)

    def players_submenu(self):
        while True:
            option = View.display_joueurs_submenu()
            if option == "1":
                Player.add_a_player()
                response = View.display_player_added()
                if response == "O" or response == "o":
                    Player.add_a_player()
                    response = View.display_player_added()
                else :
                    option
            elif option == "2":
                View.display_players_by_alphabetical_order()
                option
            elif option == "3":
                self.main_menu()
                break

    def rapports_submenu(self):
        while True:
            option = View.display_rapports_submenu()
            if option == "1":
                View.display_players_by_alphabetical_order()
                option
            elif option == "2":
                View.display_players_by_rank()
                option
            elif option == "3":
                id = Controller.choose_an_existing_tournament(self)
                tournament_players = Controller.find_players_in_tournament(id)
                View.display_tournaments_players_by_alphabetic_order()
                sorted_by_name = sorted(tournament_players, key=lambda player: player.name)
                print(sorted_by_name)
                #for player in tournament_players():
                    #print(player)
                option
            elif option == "4":
                View.display_all_tournaments()
                id = View.display_select_tournament()
                Controller.find_players_by_rank_with_tournament_id(id)
                option
            elif option == "5":
                self.find_all_players_in_all_tournaments()
                option
            elif option == "6":
                pass
                option
            elif option == "7":
                pass
                option
            elif option == "8":
                self.main_menu()
                

    def find_players_in_tournament(id):
        """Search all the players with the tournament id."""
        tournament = Tournament.search_tournament_by_id(id)
        ids = tournament.players
        list_of_players = []
        for i in ids:
            player = Player.search_player_by_id(i)
            #print(player)
            list_of_players.append(player)
        return list_of_players

    def find_players_by_rank_with_tournament_id(id):
        Tournament.search_tournament_by_id(id)
        tournament_players = Controller.find_players_in_tournament(id)
        sorted_by_rank = sorted(tournament_players, key=lambda player: player.rank)
        View.display_players_by_rank_with_tournament_id(sorted_by_rank)
    
    def find_all_players_in_all_tournaments(self):
        tournaments = View.display_all_tournaments()
        tournaments_ids = []
        for tournament in tournaments :
            tournaments_ids.append(tournament['id'])
        for id in tournaments_ids:
            all_players = Controller.find_players_in_tournament(id)
            print(all_players)

    def start_a_tournament(self):
        """Starting processus of tournament, create a tournament with players... and a round with them."""
        self.create_a_tournament()
        #self.start_a_round()

    def get_round_points(self):
        "Return the player points by round."
        for player in self.round.players:
            points = player.points
            return points

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
                        View.display_value_error(points)
                Player.update_player_points_in_database(player.id, player.points)
        self.get_round_points() 
        return self.tournament.players
       
    def update_the_score(self):
        """Calculate players score by doing the sum of player points"""
        for player in self.tournament.players:
            player.score = 0
            #for each match add the points to the final score 
            for points in player.points:
                player.score += points
                # update the score in serialized players
                Player.update_player_score_in_database(player.id, player.score)
        #display the player with his score
        View.display_score_after_match(tournament=self.tournament)

    def update_player_rank(self):
        """Update the rank of player at the end of tournament."""
        sorted_by_score = self.sort_players_by_score_then_rank()
        self.tournament.players = sorted_by_score
        rank = 0
        #for each player in the sorted list by score give a rank from first +1 by incrementation
        for player in sorted_by_score:
            rank += 1
            player.rank = rank
            Player.update_rank_in_database(player.id, player.rank)
        return self.tournament.players
            

