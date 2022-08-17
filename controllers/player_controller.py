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


class PlayerController:
    def __init__(self, base_controller):
        '''Has a list of Players and a view.'''
        # models
        self.base_controller = base_controller
        self.tournament = Tournament()
        self.tournament.players = []
        self.match = Match()
        self.round = Round()
        self.tournament.rounds = []

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
                    else:
                        View.display_invalid_input(response)
                        View.display_player_added()
                elif option == CONSTANTE.ADD_A_TEAM_OF_PLAYERS:
                    self.base_controller.make_a_tournament_team()
                    View.display_team_of_players_added()
                elif option == CONSTANTE.MODIFY_PLAYER_RANK:
                    players = View.display_list_of_players_by_rank()
                    player = self.select_a_player(players)
                    rank = View.display_input_the_new_rank(player)
                    Player.update_rank_in_database(player.id, rank)
                    View.display_rank_well_updated(player, rank)
                elif option == CONSTANTE.SEE_THE_LIST_OF_PLAYERS:
                    View.display_list_of_players_by_alphabetical_order()
                elif option == CONSTANTE.RETURN:
                    self.base_controller.main_menu()

    def select_a_player(self, players):
        """Select a player from a list."""
        if players is not None:
            choice = View.display_select_player()
        else:
            self.players_submenu()
        try:
            if choice <= len(players):
                joueur_choisi = players[choice - 1]
            else:
                View.display_select_a_valid_number()
        except ValueError:
            View.display_player_not_in_list(choice)
        return joueur_choisi

