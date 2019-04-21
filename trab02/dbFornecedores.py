import psycopg2
from psycopg2 import Error

with open('/home/lariteixeira/ASA/password.txt') as f:
        password = f.read().strip()

class Fornecedores:
    schema = "schema.sql"
    connection = psycopg2.connect(user = "postgres",
                                password = password,
                                host = "127.0.0.1",
                                port = "5432",
                                database = "asa")
    
    cursor = connection.cursor()

    def createTable(self): 
        try:        
            create_table_query = '''CREATE TABLE gestao.fornecedores 
                (id_fornecedor SERIAL PRIMARY KEY, 
                cnpj VARCHAR(60),
                razaoSocial VARCHAR(200),
                telefone VARCHAR(60),
                contato VARCHAR(60),
                endereco varchar(100),
                fg_ativo INT default 1); '''
            # cursor, connection = connect()
            self.cursor.execute(create_table_query)
            self.connection.commit()
            self.endConnection()
            res = True
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to create table", error) 
            res = False
        return res
    
    def addNovoFornecedor(self, cnpj, razaoSocial, telefone, endereco, contato):
        try:
            insert_table_query = '''INSERT INTO gestao.fornecedores (cnpj, razaoSocial, 
            telefone, endereco, contato) VALUES (%s, %s, %s, %s, %s)'''
            values = (cnpj, razaoSocial, telefone, endereco, contato)
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
    
#     def getUsuario(self):
#         select_query = "select * from cadastro.usuarios"
#         self.cursor.execute(select_query)
#         self.connection.commit()
#         usuario = self.cursor.fetchall() 
#         return usuario
    
#     def endConnection(self):
#         self.cursor.close()
#         self.connection.close()
