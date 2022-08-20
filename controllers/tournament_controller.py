'''Define the Main Controller'''


from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View
from rich.console import Console

# from controllers.constants import ADD_NEW_PLAYERS, SELECT_EXISTING_PLAYERS
import controllers.constants as CONSTANTE
# (dans ce cas la ecrire CONSTANTE.ADD_NEW_PLAYER dans la fonction par exemple)


class TournamentController:
    def __init__(self, base_controller):
        '''Has a list of Players and a view.'''
        # models
        self.base_controller = base_controller
        self.tournament = Tournament()
        self.tournament.players = []
        self.match = Match()
        self.round = Round()
        self.tournament.rounds = []

    def tournament_submenu(self):
        """Tournament menu propose different option about tournaments."""
        while True:
            View.display_title_of_tournament_submenu()
            option = View.display_tournament_submenu()
            if option == CONSTANTE.CREATE_NEW_TOURNAMENT:
                self.start_a_tournament()
            elif option == CONSTANTE.CHOOSE_EXISTING_TOURNAMENT:
                id = self.base_controller.choose_an_existing_tournament()
                self.continue_to_play_tournament_by_id(id)
            elif option == CONSTANTE.MAIN_MENU:
                self.base_controller.main_menu()

    def create_a_tournament(self):
        """Set up a new tournament."""
        View.display_create_a_tournament(self.tournament)
        # self.tournament.id = uuid.uuid4().hex
        while True:
            option = View.display_add_players_or_not()
            try:
                if option == CONSTANTE.ADD_NEW_PLAYERS:
                    self.base_controller.make_a_tournament_team(self.tournament)
                    # insert in database
                    self.tournament.insert_tournament_in_database()
                    View.display_tournament_well_recorded()
                    break
                elif option == CONSTANTE.SELECT_EXISTING_PLAYERS:
                    players = (View.
                               display_list_of_players_by_alphabetical_order())
                    self.tournament.players = self.select_players(players)
                    # insert in database
                    self.tournament.insert_tournament_in_database()
                    break
                else:
                    raise ValueError
            except ValueError:
                View.display_create_a_tournament_option_error()

    def select_players(self, players):
        """Select existing players to add in a new tournament."""
        choices = []
        list_of_players = 0
        while list_of_players < 8:
            if players is not None:
                choice = View.display_select_player()
            else:
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

    def sort_players_by_score_then_rank(self):
        """Sorted the list of players by score first and if score is equal,
         sort them by rank."""
        # remove what there is after the eigth player in the list otherwise
        # ther is a duplicate list with 16 players
        #del self.tournament.players[8:]
        # -x.score is the reverse order because we need the most important
        # score first and t1he first of rank, second after etc....
        sorted_by_score_then_rank = sorted(
            self.tournament.players, key=lambda x: (-x.score, x.rank))
        return sorted_by_score_then_rank

    def name_a_round(self):
        """Copy the number of turns in tournament to get an iteration of round,
         then return the name of rounds."""
        round_name = []
        for i in range(self.tournament.numbers_of_turns):
            round_name.append(f"Round {i+1}")
        return round_name

    def make_players_pairs(self):
        """Divide sorted players in two half, the best player of upper half play
        against the best player of lower half etc..Return the list of teams."""
        sorted_players_by_rank = self.base_controller.sort_players_by_rank(self.tournament)
        half = len(sorted_players_by_rank) / 2
        half = int(half)
        upper_half = sorted_players_by_rank[0:half]
        lower_half = sorted_players_by_rank[half:len(sorted_players_by_rank)]
        first_team = upper_half[0], lower_half[0]
        second_team = upper_half[1], lower_half[1]
        third_team = upper_half[2], lower_half[2]
        fourth_team = upper_half[3], lower_half[3]
        # the list of pairs of players
        list_of_teams = [
            (first_team),
            (second_team),
            (third_team),
            (fourth_team)]
        View.display_all_teams_in_first_round(list_of_teams)
        return list_of_teams

    def make_players_pairs_by_score_or_rank(self):
        """Make players pairs by score or rank after the first round
        by checking if they have already played together."""
        players = self.sort_players_by_score_then_rank()
        competitors = self.sort_players_by_score_then_rank()
        match_pairs = self.search_players_already_played_together()
        print("competitors", competitors)
        list_of_teams = []
        # while there is players, remove the first and the second player of the
        # list
        while(len(players) > 0):
            a = players.pop(0)
            print("a", a)
            b = players.pop(0)
            print("b", b)
            the_pair = [a.id, b.id]
            reversed_pair = [b.id, a.id]
            # if they have played together, put back b in list and take
            # the first of the list as b, then rearrange the list as it
            # was initially(put c in first index)
            """if(competitors[0] == a and competitors[1] == b
                or competitors[0] == b and competitors[1] == a):
                players.append(b)
                b = players.pop(0)
                if len(players) > 0:
                    c = players.pop()
                    players.insert(0, c)"""
            """for i in match_pairs:
                print(i)
                if i == the_pair or i == reversed_pair:
                    print(i, "exists")"""
            print("the pair",the_pair)
            print("match_pairs", match_pairs)
            if(the_pair in match_pairs or reversed_pair in match_pairs):
                players.append(b)
                b = players.pop(0)
                if len(players) > 0:
                    c = players.pop()
                    players.insert(0, c)
                print(True)
            else:
                print("la paire", [a, b])
            list_of_teams.append([a, b])
        View.display_all_teams_after_first_round(list_of_teams)
        return list_of_teams

    def search_players_already_played_together(self):
        tournament_pairs = []
        for round in self.tournament.rounds:
            # print("round.matchs", round.matchs)
            for match in round.matchs:
                # print("match",match.pair_of_players)
                tournament_pairs.append([match.pair_of_players[0].id, match.pair_of_players[1].id])
                
        print(tournament_pairs)
        return tournament_pairs

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

    def go_in_round(self):
        result = Tournament.search_length_field_round(self.tournament.id)
        i = result+1
        while i <= self.tournament.numbers_of_turns:
            self.start_a_round(i)
            i = i + 1

    def input_results(self, pair):
        """Input the result of the match, return the player infos with the score
        inserted."""
        result = []
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
        round.matchs = []
        i = 1
        # print(round.pairs_of_players)
        for pair in round.pairs_of_players:
            View.display_match_score_to_input(match_number=i)
            i = i + 1
            match = Match()
            match.pair_of_players = list(pair)
            # print("///pair",pair)
            while True:
                match.player_result = self.input_results(pair)
                try:
                    if match.player_result[0] + match.player_result[1] != 1:
                        raise ValueError
                    else:
                        round.matchs.append(match)
                        # print(round.matchs)
                        break
                except ValueError:
                    View.display_score_value_error()
            # lst_tuple = [x for x in zip(*[iter(round.matchs)])]
            # print(lst_tuple)
        # round.matchs = lst_tuple

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
            # Player.update_rank_in_database(player.id, player.rank)
        return self.tournament.players
