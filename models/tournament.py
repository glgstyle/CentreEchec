''''Define the tournament.'''


from models.player import Player

class Tournament:
    """A tournament"""

    def __init__(self, name="", date="", place="", comment="", numbers_of_turns=4):
        """Has a name, a date, a place, a number of turns, turns, a pool of players,  time control, comments"""
        self.name = name
        self.date = date
        self.place = place
        self.comments = comment
        self.numbers_of_turns = numbers_of_turns
    

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date
        
    @property
    def place(self):
        return self._place

    @property
    def comment(self):
        return self._comment

    @property
    def numbers_of_turns(self):
        return self._numbers_of_turns
    
    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @date.setter
    def date(self, date):
        self._date = date

    @place.setter
    def place(self, place):
        self._place = place

    @comment.setter
    def comment(self, comment):
        self._comment = comment    

    @numbers_of_turns.setter
    def numbers_of_turns(self, numbers_of_turns):
        self._numbers_of_turns = numbers_of_turns   

    """def create_a_tournament(self):
        tournament = []
        print("--------Création d'un tournoi--------")
        self.name = input("Veuillez créer un nom pour ce tournoi : ")
        tournament.append(self.name)
        self.date = input("Veuillez saisir la date du tournoi :")
        tournament.append(self.date)
        self.place = input("Veuillez saisir le lieu du tournoi :")
        tournament.append(self.place)
        self._numbers_of_turns = input("Veuillez saisir le nombre de tours (par défaut 4) ")
        players = Player.make_a_team_pool()
        tournament.append(players)
        
        print(tournament)"""


#tournoi = Tournament().create_a_tournament()




