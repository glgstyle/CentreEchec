'''Define the Main Controller'''


from models.tournament import Tournament
from views.base import View

# from controllers.constants import ADD_NEW_PLAYERS, SELECT_EXISTING_PLAYERS
import controllers.constants as CONSTANTE
# (dans ce cas la ecrire CONSTANTE.ADD_NEW_PLAYER dans la fonction par exemple)


class ReportController:
    def __init__(self,base_controller):
        '''Has a list of Players and a view.'''
        # models
        self.base_controller = base_controller
        self.tournament = Tournament()
        self.tournament.players = []
        self.tournament.rounds = []

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
                id = self.base_controller.choose_an_existing_tournament()
                tournament_players = Tournament.find_players_in_tournament(id)
                View.display_title_list_of_players_by_alphabetic_order()
                sorted_by_name = sorted(
                    tournament_players, key=lambda player: player.name)
                View.display_tournament_players_by_alphabetical_order(
                    sorted_by_name)
            elif option == CONSTANTE.LIST_OF_TOURNAMENT_PLAYERS_BY_RANK:
                id = self.base_controller.choose_an_existing_tournament()
                self.find_players_by_rank_with_tournament_id(id)
            elif option == CONSTANTE.LIST_OF_ALL_PLAYERS_FROM_ALL_TOURNAMENTS:
                tournament_ids = self.find_all_players_in_all_tournaments()
                View.display_all_players_in_all_tournaments(tournament_ids)
            elif option == CONSTANTE.LIST_OF_ALL_ROUNDS_IN_A_TOURNAMENT:
                id = self.base_controller.choose_an_existing_tournament()
                tournament = Tournament.search_tournament_by_id(id)
                View.display_tournament_rounds_in_report(tournament)
            elif option == CONSTANTE.LIST_OF_ALL_MATCHS_IN_A_TOURNAMENT:
                id = self.base_controller.choose_an_existing_tournament()
                tournament = Tournament.search_tournament_by_id(id)
                View.display_tournament_matchs_in_report(tournament)
            elif option == CONSTANTE.RETURN_TO_THE_MAIN_MENU:
                self.base_controller.main_menu()

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
    
