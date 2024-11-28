# type:ignore
import sqlite3
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar, QMessageBox,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QWidget)

from database_connection import cur_tw
from objects import Usuario, get_usuarios


class MyTable(QTableWidget):
    def __init__(self):
        super().__init__()

    def tabela_usuarios(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 50)
            self.setColumnCount(3)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 500)
            self.setHorizontalHeaderLabels(['ID', 'Nome', 'Telefone'])
            for i in range(len(lista)):
                item1 = QTableWidgetItem(str(lista[i].id))
                item1.setFlags(item1.flags() & Qt.ItemIsEditable)
                item2 = QTableWidgetItem(lista[i].nome)
                item2.setFlags(item2.flags() & Qt.ItemIsEditable)
                item3 = QTableWidgetItem(lista[i].telefone)
                item3.setFlags(item3.flags() & Qt.ItemIsEditable)
                self.setItem(i, 0, item1)
                self.setItem(i, 1, item2)
                self.setItem(i, 2, item3)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))


class MyButton(QPushButton):
    def __init__(self, texto):
        super().__init__()
        self.setText(texto)
        self.janela_pai = self.parent()

    def activated(self, fun):

        def check_selected():
            if self.window().focusWidget() == self:
                return fun()

        self.setFocusPolicy(Qt.StrongFocus)
        self.atalho = QShortcut(QKeySequence("Return"), self)
        self.atalho.activated.connect(check_selected)
        self.clicked.connect(check_selected)


class MyMessageBox(QMessageBox):
    def __init__(self, mensagem):
        super().__init__()
        self.setText(mensagem)
        self.setIcon(QMessageBox.Warning)
        self.exec()


class MyWindow(QMainWindow):
    def __init__(self, titulo, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(titulo)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.central_widget.setLayout(self.layout)

    # Janela 1 - Tela de login
    def w1_login_screen(self):

        # Checando os dados de login
        def check_login(codigo, senha):
            try:
                cur_tw.execute(
                    F"""
                    SELECT ID, SENHA FROM USUARIOS
                    WHERE ID = {codigo}
                    """
                )
                dados_login = cur_tw.fetchone()
                if dados_login is None or dados_login[1] != senha:
                    return False
                else:
                    return True
            except sqlite3.OperationalError:
                return False

        def login(codigo, senha):
            if check_login(codigo, senha):

                def remover_widgets(self):
                    while self.layout.count() > 0:
                        item = self.layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()

                self.usuario = codigo
                self.setWindowTitle('Início')
                remover_widgets(self)
                self.w2_menu_principal()
                return True
            else:
                MyMessageBox(
                    'Falha no Login'
                )
                return False

        # Widgets da janela
        self.label_codigo = QLabel('Código Usuário: ')
        self.input_codigo = QLineEdit()
        self.label_senha = QLabel('Senha Usuário: ')
        self.input_senha = QLineEdit()
        self.button_entrar = MyButton('Entrar')

        # Propriedades dos widgets
        self.input_senha.setEchoMode(QLineEdit.Password)

        # Signals dos widgets
        self.button_entrar.activated(
            lambda: login(
                self.input_codigo.text(),
                self.input_senha.text())
        )

        # Layout da janela
        self.layout.addWidget(self.label_codigo, 1, 1, 1, 1)
        self.layout.addWidget(self.input_codigo, 1, 2, 1, 1)
        self.layout.addWidget(self.label_senha, 2, 1, 1, 1)
        self.layout.addWidget(self.input_senha, 2, 2, 1, 1)
        self.layout.addWidget(self.button_entrar, 3, 1, 1, 2)

        self.show()

    def w2_menu_principal(self):

        def show_w3():
            self.w3 = MyWindow('Usuários', usuario=self.usuario)
            self.w3.w3_usuarios()

        # Menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        menu_arquivo = QMenu('Arquivo', self)
        menu_bar.addMenu(menu_arquivo)
        acao_usuarios = QAction('Usuarios', self)
        menu_arquivo.addAction(acao_usuarios)

        # Widgets da janela
        self.button_eventos = QPushButton('Eventos')
        self.button_produtos = QPushButton('Produtos')

        # Signals dos widgets
        acao_usuarios.triggered.connect(lambda: show_w3())

        # Layout da janela
        self.layout.addWidget(self.button_eventos, 1, 1, 1, 1)
        self.layout.addWidget(self.button_produtos, 2, 1, 1, 1)

        self.showMaximized()

    def w3_usuarios(self):

        def check_values(senha):
            if len(senha) != 5:
                print('Erro')
                return False
            else:
                print('Acerto')
                return True

        def add_usuario(nome, senha, telefone):
            if not check_values(senha.text()):
                MyMessageBox('Senha deve ter apenas 5 dígitos!')
                return False
            novo_usuario = Usuario(senha.text(), nome.text(), telefone.text())
            novo_usuario.add_usuario_database()
            senha.setText('')
            nome.setText('')
            telefone.setText('')
            MyMessageBox('Usuário Adicionado com Sucesso!')

        # Widgets da janela
        self.w3_label_nome = QLabel('Nome: ')
        self.w3_input_nome = QLineEdit()
        self.w3_label_senha = QLabel('Senha: ')
        self.w3_input_senha = QLineEdit()
        self.w3_label_telefone = QLabel('Telefone: ')
        self.w3_input_telefone = QLineEdit()
        self.w3_button_adicionar = MyButton("Adicionar")
        self.w3_table_usuarios = MyTable()
        self.w3_button_remover = MyButton("Remover")

        # Ações dos Widgets
        self.w3_table_usuarios.tabela_usuarios(get_usuarios())
        self.w3_button_adicionar.clicked.connect(lambda: add_usuario(
            self.w3_input_nome, self.w3_input_senha,
            self.w3_input_telefone
        ))
        self.w3_button_adicionar.clicked.connect(
            lambda: self.w3_table_usuarios.tabela_usuarios(get_usuarios()))

        # Layout da janela
        self.layout.addWidget(self.w3_label_nome, 1, 1, 1, 1)
        self.layout.addWidget(self.w3_input_nome, 1, 2, 1, 1)
        self.layout.addWidget(self.w3_label_senha, 2, 1, 1, 1)
        self.layout.addWidget(self.w3_input_senha, 2, 2, 1, 1)
        self.layout.addWidget(self.w3_label_telefone, 3, 1, 1, 1)
        self.layout.addWidget(self.w3_input_telefone, 3, 2, 1, 1)
        self.layout.addWidget(self.w3_button_adicionar, 4, 1, 1, 2)
        self.layout.addWidget(self.w3_table_usuarios, 5, 1, 1, 2)
        self.layout.addWidget(self.w3_button_remover, 6, 1, 1, 2)

        self.showMaximized()


if __name__ == "__main__":
    app = QApplication()
    window = MyWindow('Inicio', usuario='1')
    window.w2_menu_principal()
    sys.exit(app.exec())
