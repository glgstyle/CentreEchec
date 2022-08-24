'''Define the round to play.'''


class Round:
    """A round is a list of matchs, has a name, a start time,
       a end time, some players and their results"""

    def __init__(self, name="", start_time="", end_time="",
                 pairs_of_players="", results=""):
        self.matchs = []
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.pairs_of_players = pairs_of_players
        self.results = results

    # Getters

    @property
    def name(self):
        return self._name

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def pairs_of_players(self):
        return self._pairs_of_players

    @property
    def results(self):
        return self._results

    # Setters

    @name.setter
    def name(self, name):
        self._name = name

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @pairs_of_players.setter
    def pairs_of_players(self, pairs_of_players):
        self._pairs_of_players = pairs_of_players

    @results.setter
    def results(self, results):
        self._results = results
