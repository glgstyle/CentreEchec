''''Define the tournament.'''

from tinydb import JSONStorage, Storage, TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
import json


class Tournament:
    """A tournament"""

    def __init__(self, name="", date="", place="", comment="", numbers_of_turns=4, time_control=""):
        """Has a name, a date, a place, a number of turns, turns, a pool of players,  time control, comments"""
        self.name = name
        self.date = date
        self.place = place
        self.comment = comment
        self.numbers_of_turns = numbers_of_turns
        self.time_control = time_control
       
    

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
    
    @property
    def rounds(self):
        return self._rounds
    
    @property
    def time_control(self):
        return self._time_control
    
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

    @rounds.setter
    def rounds(self, rounds):
        self._rounds = rounds 
    
    @time_control.setter
    def time_control(self, time_control):
        self._time_control = time_control

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__() 

    def clean_table():
        """Define the path, the name of table and clean it before inserting datas."""
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('Database/tournamentDb.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament') 
        tournament_table.truncate()	# clear the table first

    def insert_tournament_in_database(self):
        """Define the path of database, the name of table, and the datas to insert in the tournament table."""
        data = {'name' :self.name, 'date' :self.date, 'place' :self.place, 'comment' :self.comment, 'number_of_turns' :self.numbers_of_turns, 'time_control' :self.time_control}
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(),'TinyDate')
        db = TinyDB('Database/tournamentDb.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament') 
        tournament_table.insert(data)
        #tournament_table.insert(json.loads(json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)))



#Tournament.clean_table()
"""tour=Tournament("hhh","")
tour.insert_tournament_in_database()"""