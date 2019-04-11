from flask import Flask, url_for, request, json, jsonify
from json import dumps


from cliente import Cliente
from produto import Produto
from vendas import Vendas


app = Flask(__name__)


cliente = []
produto = []
vendas = []

@app.route('/')
def api_root():
    return 'Seja bem-vindo!'

@app.route('/cadCliente', methods = ['POST'])
def cadastrarCliente():
    global cliente
    req_data = request.get_json()

    id = len(cliente)
    nome = req_data['nome']
    new_cliente = Cliente(id, nome)
    cliente.append(new_cliente)
    res = {'status': 'ok'}
    return jsonify(res)


@app.route('/cadProduto', methods = ['POST'])
def cadastrarProduto():
    global produto
    req_data = request.get_json()

    id = len(produto)
    produto_desc = req_data['produto']
    preco = req_data['preco']
    new_produto = Produto(id, produto_desc, preco)
    produto.append(new_produto)
    res = {'status': 'ok'}
    return jsonify(res)

@app.route('/registrarVenda', methods = ['POST'])
def registrarVendas():
    global vendas

    req_data = request.get_json()
    idCliente = req_data['idCliente']
    idProduto = req_data['idProduto']
    quantidade = req_data['quantidade']
    #totalVendas = req_data['totalVendas']
   
    preco = 0
    for i in produto:
        if (i.getId() == idProduto):
            preco = i.getPreco()
    
    new_venda = Vendas(idCliente, idProduto, quantidade, preco * quantidade)
    vendas.append(new_venda) 
    print(list(p.getTotalVendas() for p in vendas))
    res = {'status': 'ok'}
    return jsonify(res)

@app.route('/totalVendasCliente/<id>', methods=['GET'])
def totalVendasCliente(id):
    id = int(id)
    usuario = []
    acumulador = 0
    for i in vendas:
        if i.getId() == id:
            acumulador += i.getTotalVendas()
    usuario = {'id': id, 'Total': acumulador}
    return jsonify(usuario)

@app.route('/todosClientes', methods = ['GET'])
def todosClientes():
        clientes = []
        for i in cliente:
                c = {'id': i.getId(), 'nome': i.getNome()}
                clientes.append(c)
        return jsonify(clientes)



