''''Define the tournament.'''

from tinydb import JSONStorage, Storage, TinyDB, Query, where
from tinydb.table import Document
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
import json
import re

#from controllers.base import Controller
from models.player import Player
from models.match import Match
from models.round import Round




class Tournament:
    """A tournament"""

    def __init__(self, id="", name="",date="",place="",comment="",numbers_of_turns=4,rounds=[],time_control="",players=[]):
        """Has a name, a date, a place, a number of turns, turns, a pool of players,  time control, comments"""
        self.id = id
        self.name = name
        self.date = date
        self.place = place
        self.comment = comment
        self.numbers_of_turns = numbers_of_turns
        self.rounds = rounds
        self.time_control = time_control
        self.players = players
       
    

    # Getters
    @property
    def id(self):
        return self._id

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

    @property
    def players(self):
        return self._players
    
    # Setters
    @id.setter
    def id(self, id):
        self._id = id

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

    @players.setter
    def players(self, players):
        self._players = players

    def __str__(self):
        #return json.dumps(dict(self), ensure_ascii=False)
        return f"{self.id} {self.name} {self.date}"

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
        data = {'id' :self.id, 'name' :self.name, 'date' :self.date, 'place' :self.place, 'comment' :self.comment, 'number_of_turns' :self.numbers_of_turns, 'time_control' :self.time_control, 'players' :[], 'rounds' :[]}
        # insert the players id in tournament
        for p in self.players:
            #print(f"Voici le p, {p}")
            data["players"].append(p.id)
        """for r in self.rounds:
            data['rounds'].append(r)"""
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(),'TinyDate')
        db = TinyDB('Database/tournamentDb.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament') 
        tournament_table.insert(data)
        #tournament_table.insert(json.loads(json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)))

    def update_rounds_in_tournament_database(id, rounds):
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('Database/tournamentDb.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament')
        q = Query()
        #place = tournament_table.search(q.id == id)
        match = Match()
        #docId = Tournament.find_doc_id_in_database_with_tournament_id(id)
        all_rounds = []
        i=0
        for round in rounds:
            i+=1
            roundData = {} 
            roundData['name'] = 'round'+'_'+str(i)
            roundData['start_date']= round.start_time
            roundData['end_date']= round.end_time
            roundData['matchs']=[]
            for team in match.pair_of_players:
                matchData = []
                for player in team: #chaque joueur doit avoir son tableau contenant id et point
                    print(player)
                    matchData.append([player.id, player.points[int(i)-1]])
                roundData['matchs'].append(matchData)
            all_rounds.append(roundData)
        tournament_table.upsert({'rounds':all_rounds}, q.id == id)

    def find_doc_id_in_database_with_tournament_id(id):
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('Database/tournamentDb.json', storage=serialization, indent=4)
        tournament_table = db.table('tournament')
        q = Query()
        docId = tournament_table.get(q.id == id)
        print("***********id du doc_id", docId.doc_id)
        print("////////////////",id)
        return docId.doc_id

    def search_tournament_by_id(id):
        """"Allow the research of tournament by id"""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament') 
        q = Query()
        result = tournament_table.search(q.id == id)
        #print(result)
        if len(result) == 1:
            # convert the TinyDb object in object tournament
            tournament = Tournament()
            tournament.id = result[0]['id']
            tournament.name = result[0]['name']
            tournament.date = result[0]['date']
            tournament.place = result[0]['place']
            tournament.comment = result[0]['comment']
            tournament.numbers_of_turns = result[0]['number_of_turns']
            tournament.time_control = result[0]['time_control']
            for p in result[0]['players']:
                #print(p)
                player = Player.search_player_by_id(p)
                #print(player)
                tournament.players.append(player)
            for r in result[0]['rounds']:
                #print(r)  
                round = Round()
                round.name = r['name']
                round.start_time = r['start_date']
                round.end_time = r['end_date']
                round.matchs = r['matchs']
                #refaire une boucle pour les matchs
                for match in round.matchs:
                    match = Match()
                    #print(match)
                tournament.rounds.append(round)
            return tournament
        else:
            return None

    def search_field_round(id):
        """Search field in tournament."""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament') 
        q = Query()
        #find = tournament_table.search((q.id == id))[0]
        find = tournament_table.search((q.id == id))
        if len(find) == 1:
            tournament = Tournament()
            #round = Round()
            #result = find["rounds"]
            tournament.rounds = find[0]['rounds']
            for round in tournament.rounds:
                round = Round()
                print("round in tournament.rounds", round)
                print(round['name'])
                round.name = round['name']
                #print(round.name)
                #print(round['start_date'])
                #print(round['end_date'])
                #print(round['matchs'])
        
                """round.start_time = round[1]['start_time']
                round.end_time = round[2]['end_time']
                round.matchs = []"""

        print("************ Rounds :",tournament.rounds)
        return tournament.rounds

    def search_length_field_round(id):
        """Search field in tounrament."""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament') 
        q = Query()
        find = tournament_table.search((q.id == id))[0]
        result = len(find["rounds"])
        print("************ résultat :",result)
        return result

    def getFieldData(fieldName, id):
        """Get the datas from a field in tiny database with tournament id."""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament') 
        results = tournament_table.search(where('id') == id)
        result = [r[fieldName] for r in results]
        return result

    def find_players_in_tournament(id):
        """Search all the players with the tournament id."""
        tournament = Tournament.search_tournament_by_id(id)
        """print("*******tournament.players", tournament.players)
        ids = tournament.players
        list_of_players = []
        for i in ids:
            player = Player.search_player_by_id(i)
            print("******player",player)
            list_of_players.append(player)
        return list_of_players"""
        return tournament.players
#Tournament.clean_table()
"""tour=Tournament("hhh","")
tour.insert_tournament_in_database()"""
#pour le tournoi il ne faut pas que le tournoi deja executé puisse être écrasé ou renouvellé( si un tournoi où tous les rounds ont été fait on ne peut pas le recommencer mais on doit pouvoir le reprendre si on s'est arrété au round 1 par exemple)
#faire des boucles pour revenir au menu principal ou au menu précédent --> OK
#updater les rounds apres chaque round et non pas dans insert tournament in database --> OK
#quand on doit choisir un joueur ou un tournoi lister les joueurs par numéro au lieu des id par les indexes de position dans la liste
#Embellir l'affichage