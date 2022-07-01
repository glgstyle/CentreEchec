''''Define the tournament.'''


#from models.player import Player
from tinydb import JSONStorage, Storage, TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

class Tournament:
    """A tournament"""

    def __init__(self, name="", date="", place="", comment="", numbers_of_turns=4):
        """Has a name, a date, a place, a number of turns, turns, a pool of players,  time control, comments"""
        self.name = name
        self.date = date
        self.place = place
        self.comment = comment
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

    def clean_table():
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('db.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament') 
        tournament_table.truncate()	# clear the table first

    def insert_tournament_in_database(self):
        data = {'name' :self.name, 'place' :self.place, 'comment' :self.comment, 'number_of_turns' :self.numbers_of_turns}
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(),'TinyDate')
        db = TinyDB('db.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament') 
        #tournament_table.insert({'name' :self.name, 'place' :self.place, 'comment' :self.comment, 'number_of_turns' :self.numbers_of_turns})
        tournament_table.insert(data)





