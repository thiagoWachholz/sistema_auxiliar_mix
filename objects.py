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
    def __init__(self, codigo, nome, ref, preco,
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


def get_produtos(order_by='AC03CODI', nome=None):
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
    return produtos


if __name__ == "__main__":
    with open('images/bebida.jpg', 'rb') as arquivo:
        image = arquivo.read()

    print(len(str(image)))
