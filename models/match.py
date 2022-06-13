'''The match to play.'''


class Match:
    '''A match has a pair of players and a result for each player'''
    def __init__(self, pair_of_players, player_match_result):
        self.pair_of_players = pair_of_players
        self.player_match_result = player_match_result

    #Getters
    @property
    def pair_of_players(self):
        return self._pair_of_players

    @property
    def player_match_result(self):
        return self._player_match_result

    #Setters
    @pair_of_players.setter
    def pair_of_players(self, pair_of_players):
        self._pair_of_players = pair_of_players

    @player_match_result.setter
    def player_match_result(self, player_match_result):
        self._player_match_result = player_match_result



    
