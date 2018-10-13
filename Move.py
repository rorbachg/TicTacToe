class Move():
    def __init__(self):
        self.__index = None
        self.__score = None

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, ind):
        self.__index = ind
