import datetime
import os

from database_connection import conn_tw, cur_mc, cur_tw

caminho_images = os.getcwd() + '\\images'


class Usuario():
    def __init__(self, senha, nome, telefone, id=None) -> None:
        self.id = id
        self.senha = senha
        self.nome = nome
        self.telefone = telefone

    def add_usuario_database(self):
        cur_tw.execute(
            f"""
            INSERT INTO USUARIOS (NOME, SENHA, TELEFONE)
            VALUES ('{self.nome}','{self.senha}','{self.telefone}')
            """
        )
        conn_tw.commit()

    def remove_usuario_database(self):
        cur_tw.execute(
            f"""
            DELETE FROM USUARIOS
            WHERE ID = '{self.id}'
            """
        )
        conn_tw.commit()


class Produto():
    def __init__(self, codigo=None, nome=None, ref=None, preco=None,
                 image=caminho_images+'\\bebida.jpg',
                 quantidade=1, categoria='Não Definido') -> None:
        self.codigo = codigo
        self.nome = nome
        self.ref = ref
        self.preco = preco
        self.preco_consignado = preco
        self.image = image
        self.quantidade = quantidade
        self.categoria = categoria

    def change_categoria(self, nova_categoria):
        self.categoria = nova_categoria
        cur_tw.execute(
            f"""
            UPDATE PRODUTOS
            SET CATEGORIA = '{nova_categoria}'
            WHERE CODIGO = '{self.codigo}'
            """
        )
        conn_tw.commit()


class Categoria():
    def __init__(self, nome) -> None:
        self.nome = nome

    def add_to_tablesql(self):
        cur_tw.execute(
            f"""
            INSERT INTO CATEGORIA (NOME)
            VALUES ('{self.nome}')
            """
        )
        conn_tw.commit()

    def remove_fromsql(self):
        cur_tw.execute(
            f"""
            DELETE FROM CATEGORIA
            WHERE NOME = '{self.nome}'
            """
        )
        conn_tw.commit()


class Festa():
    def __init__(self, numero, confirmada=False) -> None:
        self.numero = numero
        self.nome = None
        self.data = None
        self.local = None
        self.tipo = None
        self.qtd_pessoas = None
        self.qtd_alcoolicos = None
        self.produtos = {}
        self.consumo = None
        self.avaria = None
        self.locacao = None
        self.estado = None

        cur_mc.execute(
            f"""
            SELECT AC190_NOMECLI, AN190_CLIENTE, AC190_TELEFONE FROM
            MC190_ORCAMENTO
            WHERE AN190_PEDIDO = {self.numero}
            """
        )
        select0 = cur_mc.fetchone()
        self.nome = select0[0]
        if select0[1] != 0:
            cur_mc.execute(
                f"""
                SELECT MC01FONE, MC01CELULAR
                FROM MC01CLIENTE
                WHERE MC01CODIGO = {select0[1]}
                """
            )
            select_fones = cur_mc.fetchone()
            self.telefone = select_fones[0]
            self.celular = select_fones[1]
            self.cadastrado = True
        else:
            self.telefone = select0[2]
            self.celular = None
            self.cadastrado = False

        cur_tw.execute(f"""
            SELECT DATA, LOCAL, TIPO, QTD_PESSOAS, QTD_ALCOOLICOS
            FROM FESTAS WHERE N_ORCAMENTO = {self.numero}
        """)
        select1 = cur_tw.fetchall()
        if select1[0][0] is not None:
            self.data = datetime.datetime.strptime(select1[0][0], "%Y-%m-%d")
        self.local = select1[0][1]
        self.tipo = select1[0][2]
        self.qtd_pessoas = select1[0][3]
        self.qtd_alcoolicos = select1[0][4]

        if confirmada:
            cur_tw.execute(f"""
                SELECT ESTADO, CONSUMO, LOCACAO, AVARIA
                FROM FESTAS_CONFIRMADAS WHERE N_ORCAMENTO = {self.numero}
            """)
            select2 = cur_tw.fetchall()
            self.estado = select2[0][0]
            self.consumo = select2[0][1]
            self.locacao = select2[0][2]
            self.avaria = select2[0][3]

        cur_mc.execute(
            f"""
            SELECT AC191_PRODUTO, AN191_QTDE, AN191_VALOR
            FROM MC191_ITEMORCAMENTO
            WHERE AN191_PEDIDO = {self.numero}
            """
        )
        select3 = cur_mc.fetchall()
        for item in select3:
            self.produtos[item[0]] = []
            self.produtos[item[0]].append(item[0])
            cur_mc.execute(f"""
                SELECT AC03DESC, AC03REF
                FROM MC03PRO
                WHERE AC03CODI = '{item[0]}'
            """)
            select_produtos1 = cur_mc.fetchone()
            self.produtos[item[0]].append(select_produtos1[0])
            self.produtos[item[0]].append(select_produtos1[1])
            self.produtos[item[0]].append(float(item[1]))
            self.produtos[item[0]].append(float(item[2]))


class Entregador():
    def __init__(self, id, nome, telefone) -> None:
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def add_to_sql(self):
        cur_tw.execute(
            f"""
            INSERT INTO ENTREGADORES (NOME, TELEFONE)
            VALUES
            ('{self.nome}','{self.telefone}')
            """
        )
        conn_tw.commit()

    def remove_from_sql(self):
        cur_tw.execute(
            f"""
            DELETE FROM ENTREGADORES
            WHERE ID = {self.id}
            """
        )
        conn_tw.commit()


class TipoFesta():
    def __init__(self, id, nome) -> None:
        self.id = id
        self.nome = nome

    def add_to_sql(self):
        cur_tw.execute(
            f"""
            INSERT INTO TIPO_FESTA (NOME)
            VALUES ('{self.nome}')
            """
        )
        conn_tw.commit()

    def remove_from_sql(self):
        cur_tw.execute(
            f"""
            DELETE FROM TIPO_FESTA
            WHERE ID = {self.id}
            """
        )
        conn_tw.commit()


class LocalFesta():
    def __init__(self, id=None, nome=None, contato=None, logradouro=None,
                 numero=None, bairro=None, cep=None, cidade=None) -> None:
        self.id = id
        self.nome = nome
        self.contato = contato
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade

    def add_to_sql(self):
        cur_tw.execute(
            f"""
            INSERT INTO LOCAL_FESTA (NOME, CONTATO, LOGRADOURO, NUMERO, BAIRRO,
            CEP, CIDADE)
            VALUES
            ('{self.nome}','{self.contato}','{self.logradouro}','{self.numero}',
            '{self.bairro}','{self.cep}','{self.cidade}')
            """
        )
        conn_tw.commit()

    def remove_from_sql(self):
        cur_tw.execute(
            f"""
            DELETE FROM LOCAL_FESTA
            WHERE ID = {self.id}
            """
        )
        conn_tw.commit()

    def update_sql(self):
        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET NOME = '{self.nome}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET CONTATO = '{self.contato}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET LOGRADOURO = '{self.logradouro}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET NUMERO = '{self.numero}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET BAIRRO = '{self.bairro}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET CEP = '{self.cep}'
        WHERE ID = {self.id};
        """)

        cur_tw.execute(f"""
        UPDATE LOCAL_FESTA
        SET CIDADE = '{self.cidade}'
        WHERE ID = {self.id};
        """)
        conn_tw.commit()


def get_usuarios():
    usuarios = {}
    cur_tw.execute(
        """
        SELECT * FROM USUARIOS
        """
    )
    select = cur_tw.fetchall()
    if len(select) > 0:
        for usuario in select:
            usuarios[f'{usuario[0]}'] = Usuario(
                usuario[1], usuario[2], usuario[3], id=usuario[0])
    return usuarios


def get_produtos_mc():
    produtos = {}
    cur_mc.execute(
        """
        SELECT AC03CODI, AC03DESC, AC03REF, AN03PRC1
        FROM MC03PRO
        """
    )
    select = cur_mc.fetchall()
    for produto in select:
        produtos[f'{produto[0]}'] = Produto(
            produto[0], produto[1], produto[2], produto[3])
    return produtos


def check_produtos():
    produtos_mc = get_produtos_mc()
    cur_tw.execute(
        """
        SELECT * FROM PRODUTOS
        """
    )
    select = cur_tw.fetchall()
    cod_produtos_tw = [i[1] for i in select]
    for produto in produtos_mc:
        if produto not in cod_produtos_tw:
            cur_tw.execute(
                f"""
                INSERT INTO PRODUTOS (CODIGO, CATEGORIA, IMAGEM)
                VALUES
                ('{produtos_mc[produto].codigo}',
                '{produtos_mc[produto].categoria}',
                '{produtos_mc[produto].image}')
                """
            )
    conn_tw.commit()


def get_produtos(order_by='AC03CODI', nome=None, categoria=None):
    produtos = {}
    select_base = """
        SELECT AC03CODI, AC03DESC, AC03REF, AN03PRC1
        FROM MC03PRO
        WHERE 1=1
        """
    if nome is not None:
        like = f" AND LOWER(AC03DESC) LIKE '%{nome.lower()}%'"
        select_base = select_base + like
    select_base = select_base + f" ORDER BY {order_by}"
    cur_mc.execute(
        select_base
    )
    select_mc = cur_mc.fetchall()
    cur_tw.execute(
        """
        SELECT CODIGO, CATEGORIA, IMAGEM
        FROM PRODUTOS
        """
    )
    select_tw = cur_tw.fetchall()
    for produto in select_mc:
        produtos[f'{produto[0]}'] = Produto(
            produto[0], produto[1], produto[2], produto[3])
    for produto in select_tw:
        if produto[0] in produtos:
            produtos[produto[0]].categoria = produto[1]
            produtos[produto[0]].image = produto[2]
            if categoria is not None:
                if produtos[produto[0]].categoria != categoria:
                    del produtos[produto[0]]
    return produtos


def get_categorias():
    categorias = {}
    cur_tw.execute(
        """
        SELECT NOME FROM CATEGORIA
        """
    )
    select = cur_tw.fetchall()
    for categoria in select:
        categorias[categoria[0]] = Categoria(categoria[0])
    return categorias


def get_entregadores():
    entregadores = {}
    cur_tw.execute(
        """
        SELECT ID, NOME, TELEFONE FROM ENTREGADORES
        """
    )
    select = cur_tw.fetchall()
    for i in select:
        entregadores[i[0]] = Entregador(i[0], i[1], i[2])
    return entregadores


def get_tipos_festa():
    tipos_festa = {}
    cur_tw.execute(
        """
        SELECT ID, NOME FROM TIPO_FESTA
        """
    )
    select = cur_tw.fetchall()
    for i in select:
        tipos_festa[i[0]] = TipoFesta(i[0], i[1])
    return tipos_festa


def get_locais_festa():
    locais_festa = {}
    cur_tw.execute(
        """
        SELECT ID, NOME, CONTATO, LOGRADOURO, NUMERO, BAIRRO, CIDADE, CEP
        FROM LOCAL_FESTA
        """
    )
    select = cur_tw.fetchall()
    for i in select:
        locais_festa[i[0]] = LocalFesta(
            i[0], i[1], i[2], i[3], i[4], i[5], i[7], i[6])
    return locais_festa


def get_festas_confirmadas():
    festas_confirmadas = {}
    cur_tw.execute("""
        SELECT DISTINCT N_ORCAMENTO
        FROM FESTAS_CONFIRMADAS
    """)
    select = cur_tw.fetchall()
    for festa in select:
        festas_confirmadas[festa[0]] = Festa(festa[0])
    return festas_confirmadas


if __name__ == "__main__":
    festa = Festa(11923)
    for produto in festa.produtos:
        print(festa.produtos[produto])
