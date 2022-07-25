'''The match to play.'''


class Match:
    '''A match has a pair of players and a result for each player'''
    def __init__(self, pair_of_players=[], player_result=0):
        self.pair_of_players = pair_of_players
        self.player_result = player_result
        
    #Getters
    @property
    def pair_of_players(self):
        return self._pair_of_players

    @property
    def player_result(self):
        return self._player_result

    #Setters
    @pair_of_players.setter
    def pair_of_players(self, pair_of_players):
        self._pair_of_players = pair_of_players

    @player_result.setter
    def player_result(self, player_result):
        self._player_result = player_result



    
