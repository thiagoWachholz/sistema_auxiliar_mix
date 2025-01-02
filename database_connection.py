# type:ignore
# import datetime
import json
import os
import sqlite3

import firebirdsql

database_path = 'database_path.json'

# Criacao do arquivo json que armazena o caminho dos databases
if os.path.exists(database_path):
    with open(database_path, 'r', encoding='utf-8') as arquivo:
        database_name = json.load(arquivo)
else:
    with open(database_path, 'w') as arquivo:
        database_name = ['a', 'b']
        json.dump(database_name, arquivo)
database_name_mc = database_name[0] + '\\MCSISTEMASFB.FDB'
database_name_tw = database_name[0] + '\\banco_tw.db'

username = "SYSDBA"
password = "masterkey"
port = 3050
host = "localhost"

# Criando conexão com banco de dados da MC Sistemas
conn_mc = firebirdsql.connect(
    user=username,
    password=password,
    database=database_name_mc,
    host='localhost',
    charset='ANSI'
)
cur_mc = conn_mc.cursor()

# Criando conexão com banco de dados proprio do sistema
conn_tw = sqlite3.connect(database_name_tw)
cur_tw = conn_tw.cursor()

# Criando tabelas caso ainda não existam
cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS USUARIOS (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        SENHA CHAR(5),
        NOME VARCHAR(50),
        TELEFONE VARCHAR(20)
    );
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS TIPO_FESTA (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(255)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS ENTREGADORES (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(255),
        TELEFONE VARCHAR(15)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS LOCAL_FESTA (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(255),
        CONTATO VARCHAR(255),
        LOGRADOURO VARCHAR(100),
        NUMERO VARCHAR(10),
        BAIRRO VARCHAR(30),
        CIDADE VARCHAR(30),
        CEP VARCHAR(9)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS PRODUTOS (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CODIGO CHAR(7),
        CATEGORIA VARCHAR(255),
        IMAGEM VARCHAR(8000)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS FESTAS (
        N_ORCAMENTO INTEGER NOT NULL PRIMARY KEY,
        DATA DATE,
        LOCAL VARCHAR(255),
        TIPO VARCHAR(255),
        QTD_PESSOAS INT,
        QTD_ALCOOLICOS INT
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS FESTAS_CONFIRMADAS (
        N_ORCAMENTO INTEGER NOT NULL PRIMARY KEY,
        ESTADO VARCHAR(10),
        CONSUMO DECIMAL(10,2),
        LOCACAO DECIMAL(10,2),
        AVARIA DECIMAL(10,2),
        FOREIGN KEY (N_ORCAMENTO) REFERENCES FESTAS(N_ORCAMENTO)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS CONSUMO (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        N_ORCAMENTO INTEGER,
        COD_PRODUTO CHAR(7),
        QUANTIDADE INT,
        VALOR DECIMAL(10,2),
        TIPO VARCHAR (15),
        FOREIGN KEY (N_ORCAMENTO) REFERENCES FESTAS(N_ORCAMENTO)
    )
    """
)

cur_tw.execute(
    """
    CREATE TABLE IF NOT EXISTS CATEGORIA (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(50)
    )
    """
)

conn_tw.commit()

if __name__ == "__main__":
    cur_tw.execute(
        """
        SELECT *
        FROM FESTAS
        WHERE DATA BETWEEN 2024-12-30 AND 2025-1-5
        """
    )
    conn_tw.commit()
    select = cur_tw.fetchall()
    print(select)
    conn_tw.commit()
