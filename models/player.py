'''The player.'''


class Player:
    '''Player.'''

    def __init__(self, name="", firstname="", date_of_birth="", sexe="", score=0, points=0):
        '''A player has a name, a firstname, a date of birth and a sexe.'''
        self.name = name
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.sexe = sexe
        self.score = score
        self.points = points

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

    @score.setter
    def points(self, points):
        self._points = points


