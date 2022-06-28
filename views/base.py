'''Base view'''

#from controllers import base
from models import player
from models.player import Player
from models.round import Round
from datetime import datetime

class View:
    '''Chess game.'''

    def __init__(self):
        '''Define the view.'''

    def display_create_a_tournament(tournament):
        """Display the datas to enter for the tournament."""
        print("--------Création d'un tournoi--------")
        tournament.name = input("Veuillez créer un nom pour ce tournoi : ")
        tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        # As long as the date format is incorrect request the date again, then reformat the date before inserting it 
        while True:
            try: 
                tournament.date = datetime.strptime(tournament.date, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                tournament.date = input("Veuillez saisir la date du tournoi(jj/mm/aaaa) :")
        tournament.place = input("Veuillez saisir le lieu du tournoi :")
        try:
            tournament.numbers_of_turns = int(input(
            "Veuillez saisir le nombre de tours (appuyez sur entrée = par défaut 4) ") or "4")
        except ValueError:
            tournament.numbers_of_turns = 4
            print(f"Le nombre de tours est incorrect, utilisation de la valeur par défaut : {tournament.numbers_of_turns} ")
    
    def display_team(team):
        """Print the competitor list in shuffle order(already done in function make_players_pairs)"""
        for player in team:
            print(player.name, player.firstname)

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
        """Dispaly the round informations at the end of tournament"""
        #print(round.start_time)
        print(f"**********Voici les infos des rounds{rounds}")
        for round in rounds:
            print(f"Dans le round : {round.name}")
            print(f"qui s'est joué le {round.start_time}")
            print(f"et s'est terminé le {round.end_time}")
            #print(f"qui a opposé {round.players}")
            #for round in rounds:
        #i=0
        #while i < len(round.players):
            print(f"qui a opposé :")
            for p in round.players:
                print(f"{p[0]} - contre - {p[1]}")
            #i+=2

    def display_match_score(round):
        print("*****Match terminé, voici les scores :*****")
        for player in round.players:
            print(player.name, player.firstname, player.points)

