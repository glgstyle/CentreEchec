'''Base view'''

from models.player import Player
from models.round import Round
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.table import Table


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
        tournament.comment = input("Saisissez un commentiare ici si vous le souhaitez sinon appuyez sur entrée : ")
        tournament.time_control = input("Veuillez saisir le controle du temps (bullet, blitz ou rapid) : ")
        try:
            tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {tournament.numbers_of_turns} ")
    
    def display_team(team):
        """Return the competitor list converted in string in shuffle order(already done in function make_players_pairs)"""
        str = ""
        for player in team:
            str = str + f"{player.name} {player.firstname}"+ "\n"
        return str

    def start_time(round):
        """Define the time when start the match."""
        now = datetime.now()
        round.start_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de démarrage : {round.start_time}")
        return round.start_time
    
    def end_time(round):
        """Define the time when end the match."""
        now = datetime.now()
        round.end_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"Heure de fin : {round.end_time}")
        return round.end_time
    
    def is_the_match_finished(round):
        """Ask to press enter when the match is finished and record the end time"""
        input("Appuyez sur entrée lorsque le match est terminé.")
        return View.end_time(round)

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

