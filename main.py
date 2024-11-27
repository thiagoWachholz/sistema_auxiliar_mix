# type: ignore
import sys

from PySide6.QtWidgets import QApplication

# from database_connection import conn_mc, conn_tw, cur_mc, cur_tw
from widgets import MyWindow

if __name__ == "__main__":
    app = QApplication()
    window = MyWindow('Tela de Login')
    window.w1_login_screen()
    sys.exit(app.exec())
