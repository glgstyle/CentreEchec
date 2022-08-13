'''Define the Main Controller'''


from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View
from rich.console import Console
import uuid
# from controllers.constants import ADD_NEW_PLAYERS, SELECT_EXISTING_PLAYERS
import controllers.constants as CONSTANTE
# (dans ce cas la ecrire CONSTANTE.ADD_NEW_PLAYER dans la fonction par exemple)


class Controller:
    def __init__(self):
        '''Has a list of Players and a view.'''
        # models
        self.tournament = Tournament()
        self.tournament.players = []
        self.match = Match()
        self.round = Round()
        self.tournament.rounds = []

    def make_a_tournament_team(self):
        """Add players until players list = 8."""
        pool = 0
        while pool < 8:
            pool = pool + 1
            player = Player.add_a_player()
            self.tournament.players.append(player)

    def create_a_tournament(self):
        """Set up a new tournament."""
        View.display_create_a_tournament(self.tournament)
        self.tournament.id = uuid.uuid4().hex
        while True:
            option = View.display_add_players_or_not()
            try:
                if option == CONSTANTE.ADD_NEW_PLAYERS:
                    self.make_a_tournament_team()
                    # insert in database
                    self.tournament.insert_tournament_in_database()
                    View.display_tournament_well_recorded()
                    break
                elif option == CONSTANTE.SELECT_EXISTING_PLAYERS:
                    players = View.display_list_of_players_by_alphabetical_order()
                    self.tournament.players = self.select_players(players)
                    # insert in database
                    self.tournament.insert_tournament_in_database()
                    break
                else: 
                    raise ValueError        
            except ValueError:
                View.display_create_a_tournament_option_error()

    def select_a_player(self, players):
        """Select a player from a list."""
        if players != None : 
            choice = View.display_select_player()
        else :
            self.players_submenu()
        try:
            if choice <= len(players):
                joueur_choisi = players[choice - 1]
            else:
                View.display_select_a_valid_number()
        except ValueError:
                View.display_player_not_in_list(choice)
        return joueur_choisi

    def select_players(self, players):
        """Select existing players to add in a new tournament."""
        choices = []
        list_of_players = 0
        while list_of_players < 8:
            if players != None : 
                choice = View.display_select_player()
            else :
                self.players_submenu()
            try:
                if choice <= len(players):
                    joueur_choisi = players[choice - 1]
                    # We can not add 2 times the same player id
                    if joueur_choisi not in choices:
                        list_of_players += 1
                        choices.append(joueur_choisi)
                    else:
                        View.display_player_already_selected()
                else:
                    View.display_select_a_valid_number()
            except ValueError:
                View.display_player_not_in_list(choice)
        return choices

    def sort_players_by_rank(self):
        """Sort the list of players by rank, return the sorted list."""
        sorted_by_rank = sorted(
            self.tournament.players,
            key=lambda player: player.rank)
        return sorted_by_rank

    def make_players_pairs(self):
        """Divide sorted players in two half, the best player of upper half play
        against the best player of lower half etc..Return the list of teams."""
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
        self.list_of_teams = [
            (first_team),
            (second_team),
            (third_team),
            (fourth_team)]
        self.match.pair_of_players.clear()
        for team in self.list_of_teams:
            self.match.pair_of_players.append(team)
        View.display_all_teams_in_first_round(self.match.pair_of_players)
        return self.match.pair_of_players

    def make_players_pairs_by_score_or_rank(self):
        """Make players pairs by score or rank after the first round
        by checking if they have already played together."""
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        competitors = self.sort_players_by_score_then_rank()
        players = sorted_by_score_or_rank
        self.list_of_teams = []
        # while there is players, remove the first and the second player of the
        # list
        while(len(players) > 0):
            a = players.pop(0)
            b = players.pop(0)
            # if they have play together, put back b in list and take
            # the first of the list as b, then rearrange the list as it
            # was initially(put c in first index)
            if(competitors[0] == a and competitors[1] == b
                or competitors[0] == b and competitors[1] == a):
                players.append(b)
                b = players.pop(0)
                if len(players) > 0:
                    c = players.pop()
                    players.insert(0, c)
            self.list_of_teams.append([a, b])
        self.match.pair_of_players.clear()
        for team in self.list_of_teams:
            self.match.pair_of_players.append(team)
        View.display_all_teams_after_first_round(self.match.pair_of_players)
        return self.match.pair_of_players

    def sort_players_by_score_then_rank(self):
        """Sorted the list of players by score first and if score is equal,
         sort them by rank."""
        # remove what there is after the eigth player in the list otherwise
        # ther is a duplicate list with 16 players
        del self.tournament.players[8:]
        # -x.score is the reverse order because we need the most important
        # score first and t1he first of rank, second after etc....
        sorted_by_score_then_rank = sorted(
            self.tournament.players, key=lambda x: (-x.score, x.rank))
        return sorted_by_score_then_rank

    def match_record(self):
        """Record the players in a match and return them."""
        players_in_match = []
        sorted_by_score_or_rank = self.sort_players_by_score_then_rank()
        for player in sorted_by_score_or_rank:
            players_in_match.append(player)
        return players_in_match

    def results_of_match(self, round):
        """Input the players results in the list, insert the pair of players
        and their results in match."""
        round.matchs=[]
        i=1
        print(round.pairs_of_players)
        for pair in round.pairs_of_players:
            View.display_match_score_to_input(match_number=i)
            i=i+1
            match =Match()
            match.pair_of_players=pair
            #print("///pair",pair)
            while True:
                match.player_result = self.input_results(pair)
                try:
                    if match.player_result[0] + match.player_result[1] != 1:
                        raise ValueError
                        """if match.player_result[0] == 0 and match.player_result[1] == 0:
                            raise ValueError
                        elif match.player_result[0] == 0.5 and match.player_result[1] != 0.5:
                            raise ValueError
                        elif match.player_result[0] == 1 and match.player_result[1] != 0:
                            raise ValueError"""
                    else :
                        round.matchs.append(match)
                        break
                except ValueError:
                    View.display_score_value_error()

    def name_a_round(self):
        """Copy the number of turns in tournament to get an iteration of round,
         then return the name of rounds."""
        round_name = []
        for i in range(self.tournament.numbers_of_turns):
            round_name.append(f"Round {i+1}")
        return round_name

    def go_in_round(self):
        result = Tournament.search_length_field_round(self.tournament.id)
        i = result+1
        while i <= self.tournament.numbers_of_turns:
            self.start_a_round(i)
            i=i+1

    def start_a_round(self, current_round_number=1):
        """Start to give a name to the round then until there is no more round,
         start a new match."""
        console = Console()
        list_name_round = self.name_a_round()
        # for each round, create pairs of players, append start, end time and
        # players pairs with their score in a round
        # if this is the first round:
        round = Round()
        round.name = list_name_round[current_round_number-1]
        View.display_round_name(round.name)
        if current_round_number == 1:
            round.pairs_of_players = self.make_players_pairs()
        else:
            round.pairs_of_players = self.make_players_pairs_by_score_or_rank()
        console.input(
            "\n[bold red]Appuyez sur entrée pour démarrer le match[/]")
        round.start_time = View.start_time()
        round.end_time = View.is_the_match_finished()
        self.results_of_match(round)
        self.update_the_score()
        self.tournament.rounds.append(round)
        Tournament.update_rounds_in_tournament_database(
            id=self.tournament.id, rounds=self.tournament.rounds)
        self.update_player_rank()
        View.display_infos_rounds(self.tournament.rounds)
        Player.remove_player_points_in_database()

    def program_start(self):
        """Show the title program, open the mainmenu with options to select."""
        View.menuTitle()
        self.main_menu()

    def main_menu(self):
        """The main menu propose differents options:
            tournament, players or report submenu."""
        while True:
            option = View.display_main_menu()
            if option == CONSTANTE.TOURNAMENT:
                self.tournament_submenu()
            elif option == CONSTANTE.PLAYERS:
                self.players_submenu()
            elif option == CONSTANTE.REPORTS:
                self.reports_submenu()
            else:
                View.display_unknown_choice()

    def tournament_submenu(self):
        """Tournament menu propose different option about tournaments."""
        while True:
            View.display_title_of_tournament_submenu()
            option = View.display_tournament_submenu()
            if option == CONSTANTE.CREATE_NEW_TOURNAMENT:
                self.start_a_tournament()
            elif option == CONSTANTE.CHOOSE_EXISTING_TOURNAMENT:
                id = self.choose_an_existing_tournament()
                self.continue_to_play_tournament_by_id(id)
            elif option == CONSTANTE.MAIN_MENU:
                self.main_menu()

    def choose_an_existing_tournament(self):
        """Display existing tournaments, allow to select one
            and return the tournament_doc id."""
        while True:   
            try:
                tournaments_doc = View.display_all_tournaments()
                if not tournaments_doc:
                    raise UnboundLocalError
            except UnboundLocalError:
                View.display_no_tournament_in_database()
                self.main_menu()
            else:
                choice = View.display_select_tournament()
                try: 
                    chosen_tournament_doc = tournaments_doc[choice - 1]
                    # check if choice is in len of tournament doc
                    if choice <= len(tournaments_doc):
                        View.display_selected_tournament_doc(chosen_tournament_doc)
                        return chosen_tournament_doc['id']
                except IndexError:
                    View.display_select_a_valid_number()

    def continue_to_play_tournament_by_id(self, id):
        """Continue to play an existing tournament by giving an id."""
        self.tournament = Tournament.search_tournament_by_id(id)
        nb_of_rounds = Tournament.search_length_field_round(id)
        # continue to play if tournament doesn't contains 4 rounds
        if nb_of_rounds != self.tournament.numbers_of_turns:
            self.go_in_round()
            Tournament.update_rounds_in_tournament_database(
                self.tournament.id, self.tournament.rounds)
        # else show results of tournament (don't replay)
        else:
            View.display_tournament_is_finished()
            View.display_infos_rounds(self.tournament.rounds)

    def players_submenu(self):
        """Players menu propose to add or display players."""
        View.display_title_of_players_submenu()
        while True:
            option = View.display_joueurs_submenu()
            if option == CONSTANTE.ADD_A_NEW_PLAYER:
                Player.add_a_player()
                response = View.display_player_added()
                if response.upper() == "O":
                    Player.add_a_player()
                    response = View.display_player_added()
                if response.upper() == "N":
                    View.display_main_menu()
                else :
                    View.display_invalid_input(response)
                    View.display_player_added()
            elif option == CONSTANTE.ADD_A_TEAM_OF_PLAYERS:
                self.make_a_tournament_team()
                View.display_team_of_players_added()
            elif option == CONSTANTE.MODIFY_PLAYER_RANK:
                players = View.display_list_of_players_by_alphabetical_order()
                player = self.select_a_player(players)
                rank = View.display_input_the_new_rank(player)
                Player.update_rank_in_database(player.id, rank)
            elif option == CONSTANTE.SEE_THE_LIST_OF_PLAYERS:
                View.display_list_of_players_by_alphabetical_order()
            elif option == CONSTANTE.RETURN:
                self.main_menu()

    def reports_submenu(self):
        """Report menu propose a list of differents reports from database."""
        View.display_title_report_submenu()
        while True:
            option = View.display_reports_submenu()
            if option == CONSTANTE.LIST_OF_ALL_PLAYERS_BY_ALPHABETICAL_ORDER:
                View.display_list_of_players_by_alphabetical_order()
            elif option == CONSTANTE.LIST_OF_ALL_PLAYERS_BY_RANK:
                View.display_list_of_players_by_rank()
            elif option == CONSTANTE.TOURNAMENT_PLAYERS_BY_ALPHABETICAL_ORDER:
                id = Controller.choose_an_existing_tournament(self)
                tournament_players = Tournament.find_players_in_tournament(id)
                View.display_title_list_of_players_by_alphabetic_order()
                sorted_by_name = sorted(
                    tournament_players, key=lambda player: player.name)
                View.display_tournament_players_by_alphabetical_order(
                    sorted_by_name)
            elif option == CONSTANTE.LIST_OF_TOURNAMENT_PLAYERS_BY_RANK:
                id = Controller.choose_an_existing_tournament(self)
                Controller.find_players_by_rank_with_tournament_id(id)
            elif option == CONSTANTE.LIST_OF_ALL_PLAYERS_FROM_ALL_TOURNAMENTS:
                tournament_ids = self.find_all_players_in_all_tournaments()
                View.display_all_players_in_all_tournaments(tournament_ids)
            elif option == CONSTANTE.LIST_OF_ALL_ROUNDS_IN_A_TOURNAMENT:
                #View.display_all_tournaments()
                id = Controller.choose_an_existing_tournament(self)
                tournament = Tournament.search_tournament_by_id(id)
                View.display_tournament_rounds_in_report(tournament)
            elif option == CONSTANTE.LIST_OF_ALL_MATCHS_IN_A_TOURNAMENT:
                #View.display_all_tournaments()
                id = Controller.choose_an_existing_tournament(self)
                tournament = Tournament.search_tournament_by_id(id)
                View.display_tournament_matchs_in_report(tournament)
            elif option == CONSTANTE.RETURN_TO_THE_MAIN_MENU:
                self.main_menu()

    def find_players_by_rank_with_tournament_id(id):
        """Allow to find the list of players from a tournament id."""
        tournament = Tournament.search_tournament_by_id(id)
        sorted_by_rank = sorted(
            tournament.players,
            key=lambda player: player.rank)
        View.display_players_by_rank_in_tournament(sorted_by_rank)

    def find_all_players_in_all_tournaments(self):
        """Allow to find all players from all tournaments."""
        tournaments = View.display_all_tournaments()
        tournaments_ids = []
        for tournament in tournaments:
            tournaments_ids.append(tournament['id'])
        return tournaments_ids

    def start_a_tournament(self):
        """Starting processus of tournament, create a tournament with players...
         and a round with them."""
        self.create_a_tournament()
        # ask if we start a round, if yes : start the first round and then go
        # in second round
        response = View.display_should_we_start_the_game()
        if response.upper() == "O":
            for i in range(0, self.tournament.numbers_of_turns):
                self.start_a_round((i+1))

    def input_results(self, pair):
        """Input the result of the match, return the player infos with the score
        inserted."""
        result=[]
        for player in pair:
                # As long as the score is incorrect request the score again,
                # then insert it in the player list
                while True:
                    points = input("Veuillez entrer le score de "
                                   f"{player.firstname} {player.name} : ")
                    try:
                        points = float(points)
                        if points != 0.0 and points != 0.5 and points != 1.0:
                            View.display_invalid_point()
                        else:
                            # Copy the existing player points and add the new
                            # points
                            player.points = [*player.points, points]
                            result.append(points)
                            break
                    except ValueError:
                        View.display_value_error(points)
                Player.update_player_points_in_database(
                    player.id, player.points)
        return result 

    def update_the_score(self):
        """Calculate players score by doing the sum of player points."""
        for player in self.tournament.players:
            player.score = 0
            # for each match add the points to the final score
            for points in player.points:
                player.score += points
                # update the score in serialized players
                Player.update_player_score_in_database(player.id, player.score)
        # display the player with his score
        View.display_score_after_match(tournament=self.tournament)

    def update_player_rank(self):
        """Update the rank of player at the end of tournament."""
        sorted_by_score = self.sort_players_by_score_then_rank()
        self.tournament.players = sorted_by_score
        rank = 0
        # for each player in the sorted list by score give a rank from first +1
        # by incrementation
        for player in sorted_by_score:
            rank += 1
            player.rank = rank
            #Player.update_rank_in_database(player.id, player.rank)
        return self.tournament.players
