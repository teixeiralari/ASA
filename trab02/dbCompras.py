import psycopg2
from psycopg2 import Error

with open('/home/lariteixeira/ASA/password.txt') as f:
        password = f.read().strip()

class Compras:
    schema = "schema.sql"
    connection = psycopg2.connect(user = "postgres",
                                password = password,
                                host = "127.0.0.1",
                                port = "5432",
                                database = "asa")
    
    cursor = connection.cursor()

    def createTable(self): 
        try:        
            create_table_query = '''CREATE TABLE gestao.compras 
                (id_compra SERIAL PRIMARY KEY, 
                id_produto INT references gestao.produtos(id_produto) NOT NULL,
                id_fornecedor INT references gestao.fornecedores(id_fornecedor) NOT NULL, 
                id_categoria INT references gestao.categorias(id_categoria) NOT NULL, 
                dataCompra timestamp,
                valorTotal NUMERIC,
                quantidade INT,
                fg_ativo INT default 1); '''
            # cursor, connection = connect()
            self.cursor.execute(create_table_query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            res = True
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to create table", error) 
            res = False
        return res
    
    def addNovaCompra(self, id_fornecedor, id_produto, id_categoria, dataCompra, valorTotal, quantidade):
        try:
            insert_table_query = '''INSERT INTO gestao.Compras (id_fornecedor, id_produto, id_categoria, 
            dataCompra, valorTotal, quantidade) VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (id_fornecedor, id_produto, id_categoria, dataCompra, valorTotal, quantidade)
            self.cursor.execute(insert_table_query, values)
            self.connection.commit()
            count = self.cursor.rowcount
            print (count, "Record inserted successfully into table")
            self.endConnection()
            res = True
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to insert record into table", error) 
            res = False
        return res
    

    def getprecoByIdProduto(self, where):
        select_query = "select valorUnitario from gestao.produtos " + where
        self.cursor.execute(select_query)
        preco = self.cursor.fetchone() 
        return preco


    def endConnection(self):
        self.cursor.close()
        self.connection.close()