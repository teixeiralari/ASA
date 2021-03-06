import psycopg2
from psycopg2 import Error

with open('/home/lariteixeira/ASA/password.txt') as f:
        password = f.read().strip()

class Vendedores:
    schema = "schema.sql"
    connection = psycopg2.connect(user = "postgres",
                                password = password,
                                host = "127.0.0.1",
                                port = "5432",
                                database = "asa")
    
    cursor = connection.cursor()

    def createTable(self): 
        try:        
            create_table_query = '''CREATE TABLE gestao.vendedores 
                (id_vendedor SERIAL PRIMARY KEY, 
                cpf VARCHAR(60),
                nome VARCHAR(200),
                telefone VARCHAR(60),
                carteiraTrabalho VARCHAR(60),
                dataAdmissao timestamp,
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

    def addNovoVendedor(self, cpf, nome, carteiraTrabalho, telefone, dataAdmissao):
        try:
            insert_table_query = '''INSERT INTO gestao.vendedores (cpf, nome, 
            carteiraTrabalho, telefone, dataAdmissao) VALUES (%s, %s, %s, %s, %s)'''
            values = (cpf, nome, carteiraTrabalho, telefone, dataAdmissao)
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
    
    def allVendedores(self):
        select_query = 'select * from gestao.vendedores'
        self.cursor.execute(select_query)
        vendedores = self.cursor.fetchall() 
        return vendedores
         
    
    def endConnection(self):
        self.cursor.close()
        self.connection.close()