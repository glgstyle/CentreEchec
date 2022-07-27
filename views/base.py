'''Base view'''

#from models.player import Player
#from models.round import Round
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
#from simple_term_menu import TerminalMenu
from models.tournament import Tournament
import json
from tinydb import TinyDB, Query

from models import tournament

console = Console()
class View:
    '''Chess game.'''
    
    def __init__(self):
        '''Define the view.'''

    def display_create_a_tournament(tournament):
        """Display the datas to enter for the tournament."""
        # customisation of console outputs: color and style
        custom_theme = Theme({"success" : "green", "error" : "bold red"})
        console = Console(theme=custom_theme)
        # make frame around text for better view
        vertical     = '\u2551'
        horizontal   = '\u2550'
        top_left     = '\u2554'
        top_right    = '\u2557'
        bottom_left  = '\u255a'
        bottom_right = '\u255d'
        text = "Création d'un tournoi"
        # top border
        console.print(f"\t{top_left}{horizontal*(len(text)+4)}{top_right}", style="success")
        # text
        console.print(f"\t{vertical}  {text}  {vertical}", style="success")
        # bottom border
        console.print(f"\t{bottom_left}{horizontal*(len(text)+4)}{bottom_right}", style="success")
        # input informations of tournament
        tournament.name = input("Veuillez créer un nom pour ce tournoi : ")
        tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        # as long as the date format is incorrect request the date again, then reformat the date before inserting it 
        while True:
            try: 
                tournament.date = datetime.strptime(tournament.date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        tournament.place = input("Veuillez saisir le lieu du tournoi :")
        tournament.comment = input("Saisissez un commentaire ici si vous le souhaitez sinon appuyez sur entrée : ")
        tournament.time_control = input("Veuillez saisir le controle du temps (bullet, blitz ou rapid) : ")
        try:
            tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {tournament.numbers_of_turns} ")
    
    def display_add_players_or_not():
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Ajouter de nouveaux joueurs")
        print("2 - Sélectionner des joueurs dans la base de données")
        print("3 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_team(team):
        """Return the competitor list converted in string in shuffle order(already done in function make_players_pairs)"""
        str = ""
        for player in team:
            str = str + f"{player.name} {player.firstname}"+ "\n"
        return str
    
    def display_all_teams_in_first_round(list_of_teams):
        print(f"ômes sont les suivants :\n")
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
        print(f"Les bibômes sont les suivants :\n")
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
        """Ask to press enter when the match is finished and record the end time"""
        input("Appuyez sur entrée lorsque le match est terminé.")
        return View.end_time()

    def display_score_after_match(tournament):
        """Display players score by doing the sum of player points after match"""
        print("\n****** Voici les scores des joueurs : ******\n")
        #For each player in the list, display the firstname, the name and the match_results in player list with the score updated
        table = Table(title="Scores")
        console = Console()
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Points")
        table.add_column("Score", style="magenta")
        for player in tournament.players:
            table.add_row(f"{player.firstname} {player.name}",f"{player.points}",f"{player.score}")
        console.print(table)
        
    def display_round_name(round):
        console = Console()
        i = round
        console.print("\n" + i + "\n", style="blue", justify="left")

    def display_infos_rounds(rounds):
        """Display the round informations in a table at the end of tournament."""
        table = Table(title="Récapitulatif du tournoi par round")
        console = Console()
        table.add_column("Round", style="cyan", no_wrap=True)
        table.add_column("Heure de début", style="yellow")
        table.add_column("Heure de fin", style="magenta")
        table.add_column("Adversaires", style="blue")
        for round in rounds:
            competitors =[]
            for p in round.players:
                competitors.append(f"{p[0]} - contre - {p[1]}")
            table.add_row(f"{round.name}", f"{round.start_time}", f"{round.end_time}", f"{competitors}")
        console.print(table)

    def display_value_error(points):
        print(f"({points}) n'est pas un score valide veuillez rentrer un chiffre ou un nombre ") 

    # mainMenu
    def menuTitle():
        console.print(" ____           _              _____     _                   ", style = "purple")
        console.print("/ ___|___ _ __ | |_ _ __ ___  | ____|___| |__   ___  ___ ___ ", style = "purple")
        console.print("| |   / _ \  _ \| __|  __/ _ \ |  _| / __| '_ \ / _ \/ __/ __|", style = "purple")
        console.print("| |__|  __/ | | | |_| | |  __/ | |__| (__| | | |  __/ (__\__ \"", style = "purple")
        console.print("\____\___|_| |_|\__|_|  \___| |_____\___|_| |_|\___|\___|___/", style = "purple")

    def display_main_menu():
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Tournois")
        print("2 - Joueurs")
        print("3 - Rapports")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_tournament_submenu():
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Créer un nouveau tournoi")#avec des joueurs existant ou créer de nouveaux joueurs
        print("2 - Choisir un tournoi existant")#lister les tournois avec l'id + le lieu de la bdd et l'uuid, pouvoir rentrer le numéro du tournoi à consulter et à utiliser si on veut y mettre des joueurs
        print("3 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_joueurs_submenu():
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Ajouter un nouveau joueur")
        print("2 - Voir la liste des joueurs")
        print("3 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_rapports_submenu():
        print("----------------------------")
        print("Sélectionnez une option")
        print("1 - Liste de tous les joueurs par ordre alphabétique")
        print("2 - Liste de tous les joueurs par classement")
        print("3 - Liste de tous les joueurs d'un tournoi par ordre alphabétique")
        print("4 - Liste de tous les joueurs d'un tournoi par classement")
        print("5 - Liste de tous les joueurs de tous les tournois")
        print("6 - Liste de tous les tours d'un tournoi")
        print("7 - Liste de tous les matchs d'un tournoi")
        print("8 - >> Retour")
        print("----------------------------")
        option = input("Veuillez saisir votre choix :")
        return option

    def display_players_by_alphabetical_order():
        """Display a report of players by alphabetical order."""
        #player = Query()
        db = TinyDB('Database/playersDb.json')
        players_table = db.table('serialized_players') 
        # sort players by name in database
        players = sorted(players_table.all(), key=lambda k: k['name'])
        #print(players)
        for player in players:
            print(player)


    def display_players_by_rank():
        """Display a report of players by rank."""
        #player = Query()
        db = TinyDB('Database/playersDb.json')
        players_table = db.table('serialized_players') 
        # sort players by rank in database
        players = sorted(players_table.all(), key=lambda k: k['rank'])
        for player in players:
            print(player)    
    
    def display_players_by_rank_with_tournament_id(sorted_by_rank):
        for player in sorted_by_rank:
            print(player.name, player.firstname,"---> " "classement : ",player.rank)
    
    def display_all_tournaments():
        db = TinyDB('DAtabase/tournamentDb.json') 
        tournament = db.table('tournament')
        #print(tournament.all())
        tournaments = sorted(tournament.all(), key=lambda k: k['date'])
        for tournament in tournaments:
            print(tournament, "\n")
        return tournaments

    def display_select_players():
        selection = input("Sélectionnez les joueurs dans la liste :")
        return selection

    def display_select_tournament():
        result = input("Sélectionnez le tournoi dans la liste :")
        return result
    
    def display_tournament_well_recorded():
        console = Console()
        console.print("Le tournoi à bien été enregistré !", style="purple")
    
    def display_player_added():
        console = Console()
        console.print("Le joueur à bien été ajouté", style="purple")
        answer = input("Souhaitez-vous en ajouter un autre (O/N) ?")
        return answer

    def display_tournaments_players_by_alphabetic_order():
        print("***********Voici la liste des joueurs du tournoi par ordre alphabétique :")
        


