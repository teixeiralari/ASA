class Cliente:
    __id = None
    __nome = None

    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome

    def getId(self):
        return self.__id
        
    def getNome(self):
        return self.__nome
