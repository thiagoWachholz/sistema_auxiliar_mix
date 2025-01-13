import datetime
import os

from database_connection import conn_mc, conn_tw, cur_mc, cur_tw

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

    def get_product_data(self):
        cur_mc.execute(
            f"""
            SELECT AC03DESC, AC03REF, AN03PRC1
            FROM MC03PRO
            WHERE AC03CODI = '{self.codigo}'
            """
        )
        select = cur_mc.fetchone()
        self.nome = select[0]
        self.ref = select[1]
        self.preco = select[2]

        cur_tw.execute(
            f"""
            SELECT IMAGEM, CATEGORIA
            FROM PRODUTOS
            WHERE CODIGO = '{self.codigo}'
            """
        )
        select = cur_tw.fetchone()
        self.image = select[0]
        self.categoria = select[1]

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
    def __init__(self, numero) -> None:
        self.numero = numero
        self.cod_cliente = None
        self.nome = None
        self.data = None
        self.local = None
        self.tipo = None
        self.qtd_pessoas = None
        self.qtd_alcoolicos = None
        self.obs1 = None
        self.obs2 = None
        self.produtos = {}
        self.consumo = {}
        self.valor_consumo = 0
        self.avaria = {}
        self.valor_avaria = 0
        self.locacao = {}
        self.valor_locacao = 0
        self.estado = 'Não Confirmado'
        self.entregador = None
        self.recolhedor = None

        cur_mc.execute(
            f"""
            SELECT AC190_NOMECLI, AN190_CLIENTE, AC190_TELEFONE, AN190_CLIENTE
            FROM MC190_ORCAMENTO
            WHERE AN190_PEDIDO = {self.numero}
            """
        )
        select0 = cur_mc.fetchone()
        self.nome = select0[0]
        self.cod_cliente = select0[3]
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

        cur_tw.execute(f"""
            SELECT ESTADO
            FROM FESTAS_CONFIRMADAS WHERE N_ORCAMENTO = {self.numero}
        """)
        select2 = cur_tw.fetchall()
        self.estado = select2[0][0]

        cur_tw.execute(
            f"""
            SELECT ENTREGADOR, RECOLHEDOR
            FROM FESTAS_CONFIRMADAS
            WHERE N_ORCAMENTO = {self.numero}
            """
        )
        select4 = cur_tw.fetchone()
        self.entregador = select4[0]
        self.recolhedor = select4[1]

        cur_mc.execute(
            f"""
            SELECT AC191_PRODUTO, AN191_QTDE, AN191_VALOR, AC190_NOMEPRO
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
            if item[3] == '':
                self.produtos[item[0]].append(select_produtos1[0])
            else:
                self.produtos[item[0]].append(item[3])
            self.produtos[item[0]].append(select_produtos1[1])
            self.produtos[item[0]].append(float(item[1]))
            self.produtos[item[0]].append(float(item[2]))

        cur_tw.execute(f"""
            SELECT COD_PRODUTO, QUANTIDADE, VALOR
            FROM CONSUMO
            WHERE N_ORCAMENTO = {numero}
            AND TIPO = 'Consumo'
            """)
        select5 = cur_tw.fetchall()
        for item in select5:
            self.consumo[item[0]] = []
            self.consumo[item[0]].append(item[0])
            cur_mc.execute(
                f"""
                SELECT AC03DESC, AC03REF
                FROM MC03PRO
                WHERE AC03CODI = '{item[0]}'
                """
            )
            select_produtos2 = cur_mc.fetchone()
            self.consumo[item[0]].append(select_produtos2[0])
            self.consumo[item[0]].append(select_produtos2[1])
            self.consumo[item[0]].append(float(item[1]))
            self.consumo[item[0]].append(float(item[2]))
            self.valor_consumo += float(item[1])*float(item[2])

        cur_tw.execute(f"""
            SELECT COD_PRODUTO, QUANTIDADE, VALOR
            FROM CONSUMO
            WHERE N_ORCAMENTO = {numero}
            AND TIPO = 'Locação'
            """)
        select5 = cur_tw.fetchall()
        for item in select5:
            self.locacao[item[0]] = []
            self.locacao[item[0]].append(item[0])
            cur_mc.execute(
                f"""
                SELECT AC03DESC, AC03REF
                FROM MC03PRO
                WHERE AC03CODI = '{item[0]}'
                """
            )
            select_produtos2 = cur_mc.fetchone()
            self.locacao[item[0]].append(select_produtos2[0])
            self.locacao[item[0]].append(select_produtos2[1])
            self.locacao[item[0]].append(float(item[1]))
            self.locacao[item[0]].append(float(item[2]))
            self.valor_locacao += float(item[1])*float(item[2])

        cur_tw.execute(f"""
            SELECT COD_PRODUTO, QUANTIDADE, VALOR
            FROM CONSUMO
            WHERE N_ORCAMENTO = {numero}
            AND TIPO = 'Avaria'
            """)
        select5 = cur_tw.fetchall()
        for item in select5:
            self.avaria[item[0]] = []
            self.avaria[item[0]].append(item[0])
            cur_mc.execute(
                f"""
                SELECT AC03DESC, AC03REF
                FROM MC03PRO
                WHERE AC03CODI = '{item[0]}'
                """
            )
            select_produtos2 = cur_mc.fetchone()
            self.avaria[item[0]].append(select_produtos2[0])
            self.avaria[item[0]].append(select_produtos2[1])
            self.avaria[item[0]].append(float(item[1]))
            self.avaria[item[0]].append(float(item[2]))
            self.valor_avaria += float(item[1])*float(item[2])

        cur_mc.execute(
            f"""
            SELECT AC190_OBS1, AC190_OBS2
            FROM MC190_ORCAMENTO
            WHERE AN190_PEDIDO = {self.numero}
            """
        )
        select = cur_mc.fetchone()
        self.obs1 = select[0]
        self.obs2 = select[1]

    def get_produtos(self):
        cur_mc.execute(
            f"""
            SELECT AC191_PRODUTO, AN191_QTDE, AN191_VALOR,
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

    def remove_produto(self, codigo_produto):
        cur_mc.execute(
            f"""
            DELETE FROM MC191_ITEMORCAMENTO
            WHERE AN191_PEDIDO = {self.numero}
            AND AC191_PRODUTO = '{codigo_produto}'
            """
        )
        conn_mc.commit()

    def set_estado(self, estado):
        cur_tw.execute(
            f"""
            UPDATE FESTAS_CONFIRMADAS
            SET ESTADO = '{estado}'
            WHERE N_ORCAMENTO = {self.numero}
            """
        )
        conn_tw.commit()


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


class Cliente():
    def __init__(self, cod) -> None:
        self.codigo = cod
        self.nome = None
        self.telefone = None
        self.celular = None

        cur_mc.execute(
            f"""
            SELECT MC01NOME, MC01FONE, MC01CELULAR
            FROM MC01CLIENTE
            WHERE MC01CODIGO = {self.codigo}
            """
        )
        select = cur_mc.fetchone()
        self.nome = select[0]
        self.telefone = select[1]
        self.celular = select[2]


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


def get_festas_confirmadas(passados=False, order_by='DATA', n_orcamento=None,
                           check_n_orcamento=False, data='',
                           check_data=False, local='', check_local=False,
                           nome='', check_nome=False, estado='',
                           check_estado=False, anteriores=False):
    festas_confirmadas = {}
    festas_confirmadas_ordenadas = {}
    estados = []
    reverse = True
    todos_dias = False
    dias = 7
    cod_sql = """
        SELECT F.N_ORCAMENTO
        FROM FESTAS F
        JOIN FESTAS_CONFIRMADAS C ON F.N_ORCAMENTO = C.N_ORCAMENTO
        WHERE 1=1
    """
    if check_n_orcamento:
        cod_sql += f' AND F.N_ORCAMENTO = {n_orcamento}'
    if check_data:
        if data == 'Hoje':
            dias = 1
        elif data == 'Esta Semana':
            dias = 7
        elif data == 'Este Mês':
            dias = 30
        elif data == 'Todos os Dias':
            todos_dias = True
        else:
            dias = 1
    if not check_n_orcamento and not check_local and \
            not check_nome and not todos_dias:
        reverse = False
        cod_sql += ' AND'
        for i in range(dias):
            qtd_dia = i * -1 if anteriores else i
            hoje = datetime.datetime.today() + datetime.timedelta(days=qtd_dia)
            data_sql = f'{hoje.year}-{hoje.month}-{hoje.day}'
            cod_sql += f' F.DATA = "{data_sql}"'
            if i != dias-1:
                cod_sql += ' OR'
    cod_sql += ''' ORDER BY C.ESTADO ASC'''
    cur_tw.execute(cod_sql)
    select = cur_tw.fetchall()
    for festa in select:
        festa_to_add = Festa(festa[0])
        if not check_local:
            local = ''
        if not check_nome:
            nome = ''
        if check_estado:
            estados = [estado]
        else:
            estados = ['Confirmado', 'Entregue', 'Não Confirmado', 'Recolhido']
        if local.upper() in str(festa_to_add.local).upper() \
            and nome.upper() in str(festa_to_add.nome).upper() \
                and festa_to_add.estado in estados:
            festas_confirmadas[festa[0]] = festa_to_add

        festas_confirmadas_ordenadas = \
            dict(sorted(festas_confirmadas.items(),
                        key=lambda item: item[1].data,
                        reverse=reverse))

    print(dias)
    return festas_confirmadas_ordenadas


def get_clientes(order_by='MC01CODIGO', like=''):
    clientes = {}
    cur_mc.execute(
        f"""
        SELECT MC01CODIGO
        FROM MC01CLIENTE
        WHERE 1=1
        AND LOWER(MC01NOME) LIKE '%{like}%'
        ORDER BY {order_by}
        """
    )
    select = cur_mc.fetchall()
    for cliente in select:
        clientes[cliente[0]] = Cliente(cliente[0])
    return clientes


if __name__ == "__main__":
    cod = 'CÓDIGO'
    codsplit = cod.split('Ó')
    print(codsplit)
