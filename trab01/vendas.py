class Vendas:
    __idCliente = None
    __idProduto = None
    __quantidade = None
    __totalVenda = None

    def __init__(self, idCliente, idProduto, quantidade, totalVenda):
        self.__idCliente = idCliente
        self.__idProduto = idProduto
        self.__quantidade = quantidade
        self.__totalVenda = totalVenda

    def getId(self):
        return self.__idCliente

    def getProduto(self):
        return self.__idProduto

    def getQuantidade(self):
        return self.__quantidade

    def getTotalVendas(self):
        return self.__totalVenda