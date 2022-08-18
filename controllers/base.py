'''Define the Main Controller'''


from controllers.player_controller import PlayerController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.base import View

# from controllers.constants import ADD_NEW_PLAYERS, SELECT_EXISTING_PLAYERS
import controllers.constants as CONSTANTE
# (dans ce cas la ecrire CONSTANTE.ADD_NEW_PLAYER dans la fonction par exemple)


class BaseController:
    def __init__(self):
        '''Has a list of Players and a view.'''
        # models
        self.player_controller = PlayerController(self)
        self.tournament_controller = TournamentController(self)
        self.report_controller = ReportController(self)

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
                self.tournament_controller.tournament_submenu()
            elif option == CONSTANTE.PLAYERS:
                self.player_controller.players_submenu()
            elif option == CONSTANTE.REPORTS:
                self.report_controller.reports_submenu()
            else:
                View.display_unknown_choice()

    def make_a_tournament_team(self, tournament):
        """Add players until players list = 8."""
        pool = 0
        while pool < 8:
            pool = pool + 1
            player = Player.add_a_player()
            tournament.players.append(player)

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
                        View.display_selected_tournament_doc
                        (chosen_tournament_doc)
                        return chosen_tournament_doc['id']
                except IndexError:
                    View.display_select_a_valid_number()

    def sort_players_by_rank(self, tournament):
        """Sort the list of players by rank, return the sorted list."""
        sorted_by_rank = sorted(
            tournament.players,
            key=lambda player: player.rank)
        return sorted_by_rank
