'''The player.'''

from datetime import datetime
from tinydb import JSONStorage, Storage, TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
import uuid


class Player:
    '''Player.'''


    def __init__(self, name="", firstname="", date_of_birth="", sexe="", points=[], score=0, rank=0):
        '''A player has a name, a firstname, a date of birth and a sexe.'''
        self.name = name
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.sexe = sexe
        self.score = score
        self.points = points
        self.rank = rank

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def firstname(self):
        return self._firstname
        
    @property
    def date_of_birth(self):
        return self._date_of_birth

    @property
    def sexe(self):
        return self._sexe
    
    @property
    def score(self):
        return self._score

    @property
    def points(self):
        return self._points
        
    @property
    def rank(self):
        return self._rank

    # Setters
    @name.setter
    def name(self, name):
        self._name = name

    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        self._date_of_birth = date_of_birth

    @sexe.setter
    def sexe(self, sexe):
        self._sexe = sexe    

    @score.setter
    def score(self, score):
        self._score = score

    @points.setter
    def points(self, points):
        self._points = points
    
    @rank.setter
    def rank(self, rank):
        self._rank = rank

    #retourne au moins le firstname et non pas player.object
    def __str__(self):
        return str(self.firstname + " " +self.name)

    #retourne le player si il est dans une liste
    def __repr__(self):
        return self.__str__()

    def clean_table():
        """Define the path, the name of table and clean it before inserting datas."""
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('Database/playersDb.json', storage=serialization, indent=4)
        players_table = db.table('serialized_players') 
        players_table.truncate()	# clear the table first

    def insert_player_in_database(self):
        """Define the path of database, the name of table, and the datas to insert in the players table."""
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(),'TinyDate')
        db = TinyDB('Database/playersDb.json', storage=serialization, indent=4)
        players_table = db.table('serialized_players') 
        # utiliser un uid -> id unique pour stocker chaque entrée
        id = uuid.uuid4().hex
        players_table.insert({'id' :id, 'name' :self.name, 'firstname' :self.firstname, 'date_of_birth' :self.date_of_birth, 'sexe' :self.sexe, 'score' :self.score, 'points' :self.points, 'rank' :self.rank})

    def add_a_player():
        player = Player()
        # As long as the name is incorrect request the name again, then insert it in the player list
        while True:          
            player.name = input("Veuillez entrer le nom du joueur : ")
            try:
                if player.name == "":
                    raise TypeError
            except TypeError:
                print("Veuillez rentrer un nom valide")
            else:
                break

        # As long as the firstname is incorrect request the firstname again, then insert it in the player list
        while True:
            player.firstname = input("Veuillez entrer le prénom du joueur : ")
            try:
                if player.firstname == "":
                    raise TypeError
            except TypeError:
                print("Veuillez rentrer un prénom valide")
            else:
                break
        # As long as the date is incorrect request the date again, then reformat the date before inserting it in the player list
        player.date_of_birth = input("Veuillez entrer sa date de naissance : ")
        while True:
            try: 
                player.date_of_birth = datetime.strptime(player.date_of_birth, "%d/%m/%Y")
                break
            except ValueError:
                print("La date n'est pas au bon format, Veuillez recommencer")
                player.date_of_birth = input("Veuillez saisir la date de naissance(jj/mm/aaaa) :")
        #Check if value is F or M
        while True:
            player.sexe = input("Veuillez entrer son sexe(F/M) : ")
            upper_sexe = player.sexe.upper()
            try:#ni F et ni M c'est pour ca que c'est and et non pas or
                if not upper_sexe == "F" and not upper_sexe == "M":
                    print(f"voici ce qui n'est pas bon : {upper_sexe}")
                    raise NameError
            except NameError:
                print(f"{upper_sexe} n'est pas pas une valeur valide, veuillez entrer F pour féminin et M pour masculin")
            else:
                break
        #Ckeck if rank is a int 
        while True:
            player.rank = input("Veuillez saisir le classement du joueur :")
            try:
                player.rank == int(player.rank)
                break
            except ValueError:
                print(f"{player.rank} n'est pas un classement valide")
        return player

    