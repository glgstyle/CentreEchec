''''Define the tournament.'''

from tinydb import JSONStorage, TinyDB, Query, where
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from models.player import Player
from models.match import Match
from models.round import Round


class Tournament:
    """A tournament"""

    def __init__(self, id="", name="", date="", place="", comment="",
                 numbers_of_turns=4, rounds=[], time_control="", players=[]):
        """Has a name, a date, a place, a number of turns, turns,
           a pool of players,  time control, comments"""
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
        return f"{self.id} {self.name} {self.date}"

    def __repr__(self):
        return self.__str__()

    def insert_tournament_in_database(self):
        """Define the path of database, the name of table, and the datas
           to insert in the tournament table."""
        data = {'id': self.id, 'name': self.name, 'date': self.date,
                'place': self.place, 'comment': self.comment,
                'number_of_turns': self.numbers_of_turns,
                'time_control': self.time_control,
                'players': [], 'rounds': []}
        # insert the players id in tournament
        for p in self.players:
            data["players"].append(p.id)
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
        db = TinyDB('Database/tournamentDb.json',
                    storage=serialization, indent=4)
        tournament_table = db.table('tournament')
        tournament_table.insert(data)

    def update_rounds_in_tournament_database(id, rounds):
        """Update the round in database with rounds informations."""
        serialization = SerializationMiddleware(JSONStorage)
        db = TinyDB('Database/tournamentDb.json',
                    storage=serialization, indent=4)
        tournament_table = db.table('tournament')
        q = Query()
        all_rounds = []
        i = 0
        for round in rounds:
            i += 1
            roundData = {}
            roundData['name'] = 'round' + '_' + str(i)
            roundData['start_date'] = round.start_time
            roundData['end_date'] = round.end_time
            roundData['matchs'] = []
            for mat in round.matchs:
                matchData = [] 
                matchData.append([mat.pair_of_players[0].id, mat.player_result[0] ])
                matchData.append([mat.pair_of_players[1].id, mat.player_result[1]])
                roundData['matchs'].append(matchData)
            all_rounds.append(roundData)
        tournament_table.upsert({'rounds': all_rounds}, q.id == id)

    def search_tournament_by_id(id):
        """"Allow the research of tournament by id"""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament')
        q = Query()
        result = tournament_table.search(q.id == id)
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
            tournament.players = []
            tournament.rounds = []
            for p in result[0]['players']:
                player = Player.search_player_by_id(p)
                tournament.players.append(player)
            for r in result[0]['rounds']:
                round = Round()
                round.name = r['name']
                round.start_time = r['start_date']
                round.end_time = r['end_date']
                round.matchs = []
                # refaire une boucle pour les matchs
                for m in r['matchs']:
                    match = Match()
                    match.pair_of_players=[ Player.search_player_by_id(m[0][0]), Player.search_player_by_id(m[1][0])]
                    match.player_result=[ m[0][1], m[1][1]]
                    round.matchs.append(match)
                tournament.rounds.append(round)
            return tournament
        else:
            return None

    def search_length_field_round(id):
        """Search field in tounrament."""
        db = TinyDB('Database/tournamentDb.json')
        tournament_table = db.table('tournament')
        q = Query()
        find = tournament_table.search((q.id == id))[0]
        result = len(find["rounds"])
        return result

    def find_players_in_tournament(id):
        """Search all the players with the tournament id."""
        tournament = Tournament.search_tournament_by_id(id)
        return tournament.players

# Embellir l'affichage
# utiliser le rapport flake8 pour corriger les erreurs 
# Modifier TinyDate pour s'afficher en format j/m/a

# mauvaise combinaison de pair 
# quand on revient sur le tournoi attention round-1 et round 1 en double vider la variable reprise en double
# problème deux fois le meme tournoi s'affiche dans le rapport 6
# le lieu du tournoi ne peut pas etre un chiffre
# créer une fonction pour modifier le rang du joueur dans le menu joueur(il ne doit etre modifié automatiquement)

# A controller :
# attention aux joueurs qui ont déjà joué enssembles(ne devrait pas arriver...)-->OK (à vérifier par Mamadou)

# Résolu:
# control du temps attention forcément blitz ou bullet ou rapid rien d'autre-->ok
# dans player_submenu autoriser o (uppercase) -->OK Mais au bout de deux fois s'arrete quand même
# voir dans les menus les breaks, option et else -->OK
# Ne pas mettre à jour le rang pendant le tournoi -->OK
# Dans l'ajout des scores après chaque round : écrire score match 1, les players, score matchs 2.... --> OK
# Contrainte des points acceptés vérifier mais probablement 0, 0.5, ou 1 --> OK
# retirer les prints et remettre bien ce qui va dans la vue-->OK
# Le classement doit etre un chiffre positif-->OK
# Checker pourquoi l'ordre des pool n'est pas respecté (division en 2 parties)-->OK
# dans view.display_info_rounds -> aller chercher les noms plutot que les id-->OK
# Créer le fichier database à vide au lancement du fichier--> retiré de gitignore
# attention ne pas pouvoir rentrer abc dans un rang juste un digit -->ok
# veuillez donner un nom pour le tournoi au lieu de créer un nom-->ok
# l'ajout de player o/n ne pas pouvoir mettre autre que o ou non
# checker dans le score du match si le premier player a eu 1 le deuxième ne peut pas avoir eu 1 0.5 et 1 impossible sur le meme match
# rajouter les points dans le récapitulatif des rounds du tournoi