# type:ignore
import json
import os

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
database_name_tw = database_name[0] + '\\TWDATABASE.FDB'

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
conn_tw = firebirdsql.connect(
    user=username,
    password=password,
    database=database_name_tw,
    host='localhost',
    charset='ANSI'
)
cur_tw = conn_tw.cursor()

if __name__ == "__main__":
    pass
