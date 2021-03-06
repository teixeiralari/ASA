from flask import Flask, url_for, request, json, jsonify, abort
# from user import User
from json import dumps
from datetime import datetime
import decimal

from dbFornecedores import Fornecedores
from dbVendedores import Vendedores
from dbCategorias import Categorias
from dbProdutos import Produtos
from dbCompras import Compras
from dbVendas import Vendas

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Seja bem-vindo!!!'

@app.route('/createTableFornecedores')
def api_createdbFornecedor():
    dbFornecedores = Fornecedores()
    if (dbFornecedores.createTable()):
        result = {"result": "Tabela de fornecedores criada!"}
    else:
        result = {"result": "Problema para criar tabela de fornecedores!"}
    return jsonify(result)

@app.route('/createTableVendedores')
def api_createdbVendedores():
    dbVendedores = Vendedores()
    if (dbVendedores.createTable()):
        result = {"result": "Tabela de vendedores criada!"}
    else:
        result = {"result": "Problema para criar tabela de vendedores!"}
    return jsonify(result)


@app.route('/createTableCategorias')
def api_createdbCategorias():
    dbCategorias = Categorias()
    if (dbCategorias.createTable()):
        result = {"result": "Tabela de categorias criada!"}
    else:
        result = {"result": "Problema para criar tabela de categorias!"}
    return jsonify(result)

@app.route('/createTableProdutos')
def api_createdbProdutos():
    dbProdutos = Produtos()
    if (dbProdutos.createTable()):
        result = {"result": "Tabela de produtos criada!"}
    else:
        result = {"result": "Problema para criar tabela de produtos!"}
    return jsonify(result)

@app.route('/createTableCompras')
def api_createdbCompras():
    dbCompras = Compras()
    if (dbCompras.createTable()):
        result = {"result": "Tabela de Compras criada!"}
    else:
        result = {"result": "Problema para criar tabela de Compras!"}
    return jsonify(result)

@app.route('/createTableVendas')
def api_createdbVendas():
    dbVendas = Vendas()
    if (dbVendas.createTable()):
        result = {"result": "Tabela de Vendas criada!"}
    else:
        result = {"result": "Problema para criar tabela de Vendas!"}
    return jsonify(result)

@app.route('/addFornecedordb', methods = ['POST'])
def api_addFornecedordb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    cnpj = req_data['cnpj']
    razaoSocial = req_data['razaoSocial']
    telefone = req_data['telefone']
    endereco = req_data['endereco']
    contato = req_data['contato']

    dbFornecedores = Fornecedores()

    if(dbFornecedores.addNovoFornecedor(cnpj, razaoSocial, telefone, endereco, contato)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result)

@app.route('/addVendedordb', methods = ['POST'])
def api_addVendedordb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    cpf = req_data['cpf']
    nome = req_data['nome']
    carteiraTrabalho = req_data['carteiraTrabalho']
    telefone = req_data['telefone']
    dataAdmissao = datetime.now()

    dbVendedores = Vendedores()

    if(dbVendedores.addNovoVendedor(cpf, nome, carteiraTrabalho, telefone, dataAdmissao)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result)

@app.route('/addCategoriadb', methods = ['POST'])
def api_addCategoriadb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    tituloCategoria = req_data['tituloCategoria']
    descricaoCategoria = req_data['descricaoCategoria']

    dbCategorias = Categorias()

    if(dbCategorias.addNovaCategoria(tituloCategoria, descricaoCategoria)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result)

@app.route('/addProdutodb', methods = ['POST'])
def api_addProdutodb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    id_fornecedor = req_data['id_fornecedor']
    id_categoria = req_data['id_categoria']
    nomeProduto = req_data['nomeProduto']
    descricaoProduto = req_data['descricaoProduto']
    valorUnitario = req_data['valorUnitario']
    quantidade = req_data['quantidade']
    quantidadeMinima = req_data['quantidadeMinima']

    dbProdutos = Produtos()

    if(dbProdutos.addNovoProduto(id_fornecedor, id_categoria, nomeProduto, descricaoProduto, valorUnitario, quantidade, quantidadeMinima)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result)

@app.route('/addCompradb', methods = ['POST'])
def api_addCompradb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    id_fornecedor = req_data['id_fornecedor']
    id_categoria = req_data['id_categoria']
    id_produto = req_data['id_produto']
    dataCompra = req_data['dataCompra']
    #descricaoProduto = req_data['#descricaoProduto']
    quantidade = req_data['quantidade']
    dbCompras = Compras()
    dbProdutos = Produtos()
    preco = dbProdutos.getprecoByIdProduto("where id_produto = " + str(id_produto))
    valorTotal = 0
    for p in preco:
        valorTotal += p * quantidade
    if(dbCompras.addNovaCompra(id_fornecedor, id_produto, id_categoria, dataCompra, valorTotal, quantidade)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result) 


@app.route('/addVendasdb', methods = ['POST'])
def api_addVendasdb():
    if not request.json:
        abort(400)
    req_data = request.get_json()

    id_vendedor = req_data['id_vendedor']
    id_categoria = req_data['id_categoria']
    id_produto = req_data['id_produto']
    dataVenda = req_data['dataVenda']
    #descricaoProduto = req_data['#descricaoProduto']
    quantidade = req_data['quantidade']
    dbVendas = Vendas()
    dbProdutos = Produtos()
    preco = dbProdutos.getprecoByIdProduto("where id_produto = " + str(id_produto))
    valorTotal = 0
    taxaLucro = decimal.Decimal(0.8)
    
    for p in preco:
        valorTotal += (1 + taxaLucro) * p * quantidade 
    if(dbVendas.addNovaVenda(id_vendedor, id_produto, id_categoria, dataVenda, valorTotal, quantidade)):
        result = {"result": "Dados inseridos com sucesso"}
    else:
        result = {"result": "Problemas para inserir os dados"}
    return jsonify(result) 


@app.route('/allfornecedordb', methods = ['GET'])
def api_allfornecedor():
    allfornecedor = []
    fornecedores = Fornecedores().allFornecedores()
    for i in fornecedores:
        f = {'id_fornecedor': i[0], 'cnpj': i[1], 'razaoSocial': i[2], 'telefone': i[3], 'endereco': i[4], 'contato': i[5]}
        allfornecedor.append(f)
    Fornecedores().endConnection()
    return jsonify(allfornecedor)

@app.route('/allvendedordb', methods = ['GET'])
def api_allvendedor():
    allVendedores =  []
    vendedor = Vendedores().allVendedores()
    for i in vendedor:
        f = {'id_vendedor': i[0], 'cpf': i[1], 'nome': i[2], 'carteiraTrabalho': i[3], 'telefone': i[4], 'dataAdmissao': i[5]}
        allVendedores.append(f)
    return jsonify(allVendedores)

@app.route('/allcategoriasdb', methods = ['GET'])
def api_allcategorias():
    allcategorias =  []
    categorias = Categorias().allCategoria()
    for i in categorias:
        f = {'id_categoria': i[0], 'tituloCategoria': i[1], 'descricaoCategoria': i[2]}
        allcategorias.append(f)
    return jsonify(allcategorias)

@app.route('/allprodutosdb', methods = ['GET'])
def api_allprodutos():
    allprodutos =  []
    produtos = Produtos().allProdutos()
    for i in produtos:
        f = {'id_categoria': i[0], 'tituloCategoria': i[1], 'descricaoCategoria': i[2]}
        allprodutos.append(f)
    return jsonify(allprodutos)

@app.route('/allcomprasdb', methods = ['GET'])
def api_allcompras():
    allcompras =  []
    compras = Compras().allCompras()
    for i in compras:
        f = {'id_compra': i[0], 'id_fornecedor': i[1], 'id_produto': i[2], 'id_categoria': i[3],
        'dataCompra': i[4], 'valorTotal': float(i[5]), 'quantidade': i[6]}
        allcompras.append(f)
    return jsonify(allcompras)

@app.route('/allvendasdb', methods = ['GET'])
def api_allvendas():
    allvendas =  []
    vendas = Vendas().allVendas()
    for i in vendas:
        f = {'id_venda': i[0], 'id_vendedor': i[1], 'id_produto': i[2], 'id_categoria': i[3],
        'dataVenda': i[4], 'valorTotal': float(i[5]), 'quantidade': i[6]}
        allvendas.append(f)
    return jsonify(allvendas)


