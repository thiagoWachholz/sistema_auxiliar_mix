from database_connection import conn_tw, cur_tw


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


def get_usuarios():
    usuarios = []
    cur_tw.execute(
        """
        SELECT * FROM USUARIOS
        """
    )
    select = cur_tw.fetchall()
    if len(select) > 0:
        for usuario in select:
            usuarios.append(
                Usuario(usuario[1], usuario[2], usuario[3], id=usuario[0])
            )
    return usuarios


if __name__ == "__main__":
    usuarios = get_usuarios()
    for usuario in usuarios:
        print(usuario.nome, usuario.id, usuario.senha, usuario.telefone)
