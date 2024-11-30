# type: ignore
import os
import sys

from PySide6.QtWidgets import QApplication

from objects import check_produtos, get_usuarios
# from database_connection import conn_mc, conn_tw, cur_mc, cur_tw
from widgets import MyWindow

check_produtos()
usuarios = get_usuarios()

caminho_images = os.getcwd() + '\\images'

# Verifique se a pasta já existe
if not os.path.exists(caminho_images):
    # Se não existir, crie a pasta
    os.makedirs(caminho_images)


if __name__ == "__main__":
    app = QApplication()

    # setando o estilo
    with open("estilo.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow('Tela de Login')
    window.w1_login_screen()
    sys.exit(app.exec())
