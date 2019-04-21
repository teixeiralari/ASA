import psycopg2
from psycopg2 import Error

with open('/home/lariteixeira/ASA/password.txt') as f:
        password = f.read().strip()

class Vendas:
    schema = "schema.sql"
    connection = psycopg2.connect(user = "postgres",
                                password = password,
                                host = "127.0.0.1",
                                port = "5432",
                                database = "asa")
    
    cursor = connection.cursor()

    def createTable(self): 
        try:        
            create_table_query = '''CREATE TABLE gestao.vendas 
                (id_venda SERIAL PRIMARY KEY, 
                id_produto INT references gestao.produtos(id_produto) NOT NULL,
                id_vendedor INT references gestao.vendedores(id_vendedor) NOT NULL, 
                id_categoria INT references gestao.categorias(id_categoria) NOT NULL, 
                dataVenda timestamp,
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

    def addNovaVenda(self, id_vendedor, id_produto, id_categoria, dataVenda, valorTotal, quantidade):
        try:
            insert_table_query = '''INSERT INTO gestao.Vendas (id_vendedor, id_produto, id_categoria, 
            dataVenda, valorTotal, quantidade) VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (id_vendedor, id_produto, id_categoria, dataVenda, valorTotal, quantidade)
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

    def endConnection(self):
        self.cursor.close()
        self.connection.close()