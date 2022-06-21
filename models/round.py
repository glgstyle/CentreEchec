'''Define the round to play.'''

class Round:
    """A round is a list of matchs, has a name, a start time and a end time"""
    def __init__(self, name="", start_time="", end_time="", players="", results=""):
        self.match = []
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.players = players
        self.results = results

    #Getters
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
    def players(self):
        return self._players

    @property
    def results(self):
        return self._results
    

    #Setters
    @name.setter
    def name(self, name):
        self._name = name
    
    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @players.setter
    def players(self, players):
        self._players = players
    
    @results.setter
    def results(self, results):
        self._results = results
    

