class Produto:
    __id = None
    __produto = None
    __preco = None

    def __init__(self, id, produto, preco):
        self.__id = id
        self.__produto = produto
        self.__preco = preco

    def getId(self):
        return self.__id

    def getProduto(self):
        return self.__produto

    def getPreco(self):
        return self.__preco

