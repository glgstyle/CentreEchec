'''Base view'''


from models.player import Player
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from models.tournament import Tournament
from tinydb import TinyDB

console = Console()


class View:
    '''Chess game.'''

    def __init__(self):
        '''Define the view.'''

    def display_create_a_tournament(tournament):
        """Display the datas to enter for the tournament."""
        # customisation of console outputs: color and style
        custom_theme = Theme({"success": "green", "error": "bold red"})
        console = Console(theme=custom_theme)
        # make frame around text for better view
        vertical = '\u2551'
        horizontal = '\u2550'
        top_left = '\u2554'
        top_right = '\u2557'
        bottom_left = '\u255a'
        bottom_right = '\u255d'
        text = "Création d'un tournoi"
        # top border
        console.print(f"\t{top_left}{horizontal*(len(text)+4)}"
                      f"{top_right}", style="success")
        # text
        console.print(f"\t{vertical}  {text}  {vertical}", style="success")
        # bottom border
        console.print(f"\t{bottom_left}{horizontal*(len(text)+4)}"
                      f"{bottom_right}", style="success")
        # input informations of tournament
        tournament.name = input("Veuillez donner un nom pour ce tournoi : ")
        tournament.date = input("Veuillez saisir la date "
                                "du tournoi(jj/mm/aaaa) :")
        # as long as the date format is incorrect request the date again,
        # then reformat the date before inserting it
        while True:
            try:
                tournament.date = datetime.strptime(tournament.date,
                                                    "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                tournament.date = input("Veuillez saisir la date du "
                                        "tournoi(jj/mm/aaaa) :")
        # check if tournament.place is a number or is empty
        while True:
            tournament.place = input("Veuillez saisir le lieu du tournoi :")
            try:
                if tournament.place == "":
                    raise ValueError
                elif tournament.place.isdigit():
                    raise TypeError
                else:
                    break
            except ValueError:
                print("Le lieu doit etre renseigné.")
            except TypeError:
                print("Le lieu ne peut pas être un chiffre ou un nombre")

        tournament.comment = input("Saisissez un commentaire ici si vous le "
                                   "souhaitez sinon appuyez sur entrée : ")
        # check if time_control is bullet, blitz or rapid (can't be something
        # else)
        while True:
            tournament.time_control = input("Veuillez saisir le controle du "
                                            "temps (bullet, blitz ou rapid) "
                                            ": ").capitalize()
            try:
                if (tournament.time_control == "Blitz" or
                    tournament.time_control == "Bullet" or
                        tournament.time_control == "Rapid"):
                    break
                else:
                    raise NameError
            except NameError:
                print(tournament.time_control, "n'est pas reconnu, "
                      "les valeurs acceptées sont bullet, blitz ou rapid")
        try:
            tournament.numbers_of_turns = int(input("Saisissez le nombre "
                                                    "de tours (appuyez sur "
                                                    "entrée = par défaut 4) "
                                                    ) or "4")
        except ValueError:
            tournament.numbers_of_turns = 4
            print("Le nombre de tours est incorrect, utilisation de la valeur "
                  f"par défaut : {tournament.numbers_of_turns} ")

    def display_add_players_or_not():
        """Display the player menu."""
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Ajouter de nouveaux joueurs")
        print("2 - Sélectionner des joueurs dans la base de données")
        print("3 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_team(team):
        """Return the competitor list converted in string in shuffle
           order(already done in function make_players_pairs)."""
        str = ""
        for player in team:
            str = str + f"{player.name} {player.firstname}" + "\n"
        return str

    def display_all_teams_in_first_round(list_of_teams):
        """Display the pairs of players in first round."""
        print("les binômes sont les suivants :\n")
        # display the teams in table
        table = Table()
        console = Console()
        table.add_column("Equipe", style="cyan", no_wrap=True)
        table.add_column("Nom des joueurs de l'équipe", style="magenta")
        table.add_row("A", View.display_team(list_of_teams[0]))
        table.add_row("B", View.display_team(list_of_teams[1]))
        table.add_row("C", View.display_team(list_of_teams[2]))
        table.add_row("D", View.display_team(list_of_teams[3]))
        console.print(table)

    def display_all_teams_after_first_round(teams):
        """Display the pairs of players after the first round."""
        print("Les bibômes sont les suivants :\n")
        # display the teams in a table
        table = Table()
        console = Console()
        table.add_column("Equipe", style="cyan", no_wrap=True)
        table.add_column("Nom des joueurs de l'équipe", style="magenta")
        table.add_row("A", View.display_team(teams[0]))
        table.add_row("B", View.display_team(teams[1]))
        table.add_row("C", View.display_team(teams[2]))
        table.add_row("D", View.display_team(teams[3]))
        console.print(table)

    def start_time():
        """Define the time when start the match."""
        now = datetime.now()
        start_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de démarrage : {start_time}")
        return start_time

    def end_time():
        """Define the time when end the match."""
        now = datetime.now()
        end_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de fin : {end_time}")
        return end_time

    def is_the_match_finished():
        """Ask to press enter when the match is finished
           and record the end time."""
        input("Appuyez sur entrée lorsque le match est terminé.")
        return View.end_time()

    def display_score_after_match(tournament):
        """Display players score by doing the sum of
           player points after match."""
        print("\n****** Voici les scores des joueurs : ******\n")
        # For each player in the list, display the firstname, the name
        # and the match_results in player list with the score updated
        table = Table(title="Scores")
        console = Console()
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Points")
        table.add_column("Score", style="magenta")
        for player in tournament.players:
            table.add_row(f"{player.firstname} {player.name}",
                          f"{player.points}", f"{player.score}")
        console.print(table)

    def display_round_name(round):
        """Display the name of round when a round start."""
        console = Console()
        i = round
        console.print("\n" + i + "\n", style="blue", justify="left")

    def display_infos_rounds(rounds):
        """Display the round informations in a table
           at the end of tournament."""
        table = Table(title="Récapitulatif du tournoi par round")
        console = Console()
        table.add_column("Round", style="cyan", no_wrap=True)
        table.add_column("Heure de début", style="yellow")
        table.add_column("Heure de fin", style="magenta")
        table.add_column("Adversaires", style="blue")
        for round in rounds:
            # show player names
            table.add_row(f"{round.name}", f"{round.start_time}",
                          f"{round.end_time}")
            for match in round.matchs:
                player1 = match.pair_of_players[0]
                player2 = match.pair_of_players[1]
                score1 = match.player_result[0]
                score2 = match.player_result[1]
                myPlayers = (player1.firstname + " " +
                             player1.name + " " + str(score1) +
                             " " + "contre" + " " + player2.firstname
                             + " " + player2.name + " " + str(score2))
                table.add_row("", "", "", myPlayers)
            table.add_row("")
        console.print(table)

    def display_value_error(points):
        """Display the value error about points."""
        print(f"({points}) n'est pas un score valide veuillez "
              "rentrer un chiffre ou un nombre ")

    # mainMenu
    def menuTitle():
        """Display the title "Centre echecs" when starts the program."""
        p = console.print
        p(" ____           _              _____     _                   ",
          style="purple")
        p("/ ___|___ _ __ | |_ _ __ ___  | ____|___| |__   ___  ___ ___ ",
          style="purple")
        p("| |   / _ \\  _ \\| __|  __/ _ \\ |  _| / __|  _ \\ / _ \\/ __/ "
          "__|", style="purple")
        p("| |__|  __/ | | | |_| | |  __/ | |__| (__| | | |  __/ (__\\__ \\",
          style="purple")
        p("\\____\\___|_| |_|\\__|_|  \\___| |_____\\___|_| |_|\\___|\\___|"
          "___/", style="purple")

    def display_main_menu():
        """Display the Main menu options."""
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Tournois")
        print("2 - Joueurs")
        print("3 - Rapports")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_title_of_tournament_submenu():
        """Display the title "tournament" in tournament
           submenu."""
        p = console.print
        p(" _____                            _",
          style="purple")
        p("|_   _|__  _   _ _ __ _ __   ___ (_)___",
          style="purple")
        p("  | |/ _ \\| | | |  __|  _ \\ / _ \\| / __|",
          style="purple")
        p('  | | (_) | |_| | |  | | | | (_) | \\__ \'',
          style="purple")
        p("  |_|\\___/ \\__,_|_|  |_| |_|\\___/|_|___/",
          style="purple")

    def display_tournament_submenu():
        """Display the tournament submenu options."""
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Créer un nouveau tournoi")
        print("2 - Choisir un tournoi existant")
        print("3 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_title_of_players_submenu():
        """Display the title "players" in players
           submenu."""
        p = console.print
        p("     _  ",
          style="purple")
        p("    | | ___  _   _  ___ _   _ _ __ ___ ",
          style="purple")
        p(" _  | |/ _ \\| | | |/ _ \\ | | |  __/ __|",
          style="purple")
        p('| |_| | (_) | |_| |  __/ |_| | |  \\__ \'',
          style="purple")
        p(" \\___/ \\___/ \\__,_|\\___|\\__,_|_|  |___/",
          style="purple")

    def display_joueurs_submenu():
        """Display the players submenu options."""
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Ajouter un nouveau joueur")
        print("2 - Ajouter une équipe de joueurs")
        print("3 - Modifier le rang d'un joueur")
        print("4 - Voir la liste des joueurs")
        print("5 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_title_report_submenu():
        """Display the title "report" in report
           submenu."""
        p = console.print
        p("____                              _       ",
          style="purple")
        p("|  _ \\ __ _ _ __  _ __   ___  _ __| |_ ___ ",
          style="purple")
        p("| |_) / _  |  _ \\|  _ \\ / _ \\|  __| __/ __|",
          style="purple")
        p('|  _ < (_| | |_) | |_) | (_) | |  | |_\\__ \'',
          style="purple")
        p("|_| \\_\\__,_| .__/| .__/ \\___/|_|   \\__|___/",
          style="purple")
        p("           |_|   |_|                    ",
          style="purple")

    def display_reports_submenu():
        """Display the report submenu options."""
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Liste de tous les joueurs par ordre alphabétique")
        print("2 - Liste de tous les joueurs par classement")
        print("3 - Liste de tous les joueurs d'un tournoi "
              "par ordre alphabétique")
        print("4 - Liste de tous les joueurs d'un tournoi par classement")
        print("5 - Liste de tous les joueurs de tous les tournois")
        print("6 - Liste de tous les tours d'un tournoi")
        print("7 - Liste de tous les matchs d'un tournoi")
        print("8 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_list_of_players_by_alphabetical_order():
        """Display a report of players by alphabetical order,
           return the list or print error if no players found."""
        players_doc = Player.list_of_players_by_alphabetical_order()
        # print("***len player:_doc,", len(players_doc))
        # check if there is players in database or not
        i = 0
        if len(players_doc) != 0:
            print("\nListe de tous les joueurs par ordre alphabétique :\n")
            list_of_players = []
            for player in players_doc:
                p = Player()
                p.name = player['name']
                p.firstname = player['firstname']
                p.id = player['id']
                i += 1
                print(i, p.name, p.firstname)
                list_of_players.append(p)
            return list_of_players
        else:
            print("Il n' a pas de joueurs dans la base de données."
                  " Veuillez en ajouter.")
            return None

    def display_list_of_players_by_rank():
        """Display a report of players by rank."""
        players_doc = Player.list_of_players_by_rank()
        # check if there is players in database or not
        i = 0
        if len(players_doc) != 0:
            print("\nListe de tous les joueurs par classement :\n")
            list_of_players = []
            for player in players_doc:
                p = Player()
                p.rank = player['rank']
                p.id = player['id']
                p.name = player['name']
                p.firstname = player['firstname']
                i += 1
                print(i, " ", "Rang", p.rank, ": ", p.name, p.firstname)
                list_of_players.append(p)
            return list_of_players
        else:
            print("Il n' a pas de joueurs dans la base de données."
                  " Veuillez en ajouter.")
            return None

    def display_players_by_rank_in_tournament(sorted_by_rank):
        """Display the players sorted by rank in a tournament."""
        for player in sorted_by_rank:
            print("Rang ", player.rank, " : ", player.name, player.firstname)

    def display_all_tournaments():
        """"Display the tournaments from database by adding
            a number(i) to allow an easy selection."""
        db = TinyDB('Database/tournamentDb.json')
        tournament = db.table('tournament')
        tournaments = sorted(tournament.all(), key=lambda k: k['date'])
        i = 1
        for t in tournaments:
            # to convert the datetime isoformat
            dt = datetime.fromisoformat(t['date'].split(":")[1])
            # give the format we want to the date
            dt = dt.strftime("%d/%m/%Y")
            print(i, dt, t['name'], "\n")
            i += 1
        return tournaments

    def display_select_player():
        """Display the input to select a player in list,
            return the selected player."""
        selection = int(input("Sélectionnez le (ou les) joueur(s)"
                              " dans la liste :"))
        return selection

    def display_select_tournament():
        """Display the input to select a tournament in list."""
        result = int(input("Sélectionnez le tournoi dans la liste :"))
        return result

    def display_tournament_well_recorded():
        """Display a confirmation for tournament well recorded."""
        console = Console()
        console.print("Le tournoi à bien été enregistré !", style="purple")

    def display_player_added():
        """Display a confirmation for player well added,
           return the answer about adding one more player."""
        console = Console()
        console.print("Le joueur à bien été ajouté", style="purple")
        answer = input("Souhaitez-vous en ajouter un autre (O/N) ?")
        return answer

    def display_team_of_players_added():
        """Display a confirmation for team of players well added."""
        console = Console()
        console.print("Les joueurs ont bien été ajoutés", style="purple")

    def display_title_list_of_players_by_alphabetic_order():
        """Display the title list of players by alphabetical order."""
        print("\nListe des joueurs du tournoi par ordre alphabétique :\n")

    def display_tournament_players_by_alphabetical_order(sorted_by_name):
        """Display the players in tournament by alphabetical order."""
        for player in sorted_by_name:
            print(player.name, player.firstname)

    def display_should_we_start_the_game():
        """"Display the input to choose if we start the game or not?
            return the answer."""
        answer = input("Souhaitez vous commencer le tournoi (O/N) ?")
        return answer

    def display_all_players_in_all_tournaments(tournaments_ids):
        """Display all players in all tournaments from the list of
           tournaments ids."""
        for id in tournaments_ids:
            all_players = Tournament.find_players_in_tournament(id)
            for player in all_players:
                print(player.name, player.firstname)

    def display_tournament_rounds_in_report(tournament):
        """Display a report of all rounds informations in tournament
           from a selected tournament."""
        for round in tournament.rounds:
            print("\n", round.name)
            print(round.start_time)
            print(round.end_time)
            for match in round.matchs:
                print(match)

    def display_tournament_matchs_in_report(tournament):
        """Display a report of all matchs from a selected
           tournament."""
        for round in tournament.rounds:
            for match in round.matchs:
                print(match)

    def display_match_score_to_input(match_number):
        """Show the match number when input the pairs_of_players score."""
        print("Score du match ", match_number)

    def display_unknown_choice():
        """Display this choice is unknnown."""
        print("Ce choix est inconnu.")

    def display_no_tournament_in_database():
        """Display there is no tournament in database."""
        print("Il n'y a pas de tournois dans la base de données.")

    def display_selected_tournament_doc(chosen_tournament_doc):
        """Display the date and name of tournament doc selected."""
        # to convert the datetime isoformat
        tournament_date = (datetime.fromisoformat
                           (chosen_tournament_doc['date'].split(":")[1]))
        # give the format we want to the date
        tournament_date = tournament_date.strftime("%d/%m/%Y")
        console.print("Le tournoi choisi est le tournoi ",
                      chosen_tournament_doc['name'],
                      " qui s'est joué le ",
                      tournament_date, style="purple")

    def display_select_a_valid_number():
        """Display the number selected is not in the list."""
        console.print("\nVeuillez choisir un numero dans la liste\n",
                      style="red")

    def display_tournament_is_finished():
        """Display the tournament is finished."""
        print("le tournoi est déjà terminé, voici les résultats :")

    def display_invalid_point():
        """Display the point awarded is not allowed."""
        console.print("Le point attribué ne correspond pas."
                      "Veuillez entre 0, 0.5 ou 1.", style="red")

    def display_player_already_selected():
        """Display the player has been already selected."""
        print("Ce joueur a déjà été selectionné, "
              "veuillez en choisir un autre")

    def display_player_not_in_list(choiced_player):
        """Display the player selected is not in the list."""
        print(choiced_player, "n'est pas dans la liste des joueurs."
              "Veuillez saisir un chiffre correspondant au "
              "joueur dans la liste.")

    def display_score_value_error():
        print("Le score indiqué ne correspond pas aux règles, "
              "pour rappel: 0 -> 1, 0.5 -> 0.5, 1 -> 0 .")

    def display_create_a_tournament_option_error():
        console.print("Veuillez saisir une option (1 ou 2).", style="red")

    def display_invalid_input(response):
        print(response, "n'est pas une entrée valide, veuillez recommencer.")

    def display_input_the_new_rank(player):
        rank = console.input(f"[purple]Veuillez entrer le nouveau rang de"
                             f" {player} :")
        return rank

    def display_rank_well_updated(player, rank):
        console.print(f"Le nouveau rang de {player} après mise à jour est"
                      f" de : {rank}")
