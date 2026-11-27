import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost", #endereço do servidor mysql
        user="root", #usuario do banco de dados 
        password="", #senha do mysql(altere se houver)
        database="achados_perdidos"  #nome do banco criado no modulo 2
    )