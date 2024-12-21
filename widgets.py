# type:ignore
import datetime
import sqlite3
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QIntValidator, QKeyEvent, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                               QGridLayout, QLabel, QLineEdit, QMainWindow,
                               QMenu, QMenuBar, QMessageBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QTextEdit,
                               QWidget)

from database_connection import conn_mc, conn_tw, cur_mc, cur_tw
from objects import (Categoria, Cliente, Entregador, Festa, LocalFesta,
                     TipoFesta, Usuario, caminho_images, get_categorias,
                     get_clientes, get_entregadores, get_festas_confirmadas,
                     get_locais_festa, get_produtos, get_tipos_festa,
                     get_usuarios)


class MyTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setSelectionBehavior(QTableWidget.SelectRows)

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
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].id))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(lista[i].nome)
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3 = QTableWidgetItem(lista[i].telefone)
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_produtos(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(7)
            self.setColumnWidth(0, 100)
            self.setColumnWidth(1, 300)
            self.setColumnWidth(2, 100)
            self.setColumnWidth(3, 100)
            self.setColumnWidth(4, 100)
            self.setColumnWidth(5, 100)
            self.setColumnWidth(6, 100)
            self.setHorizontalHeaderLabels(
                ['Código', 'Nome', 'Categoria', 'Referência', 'Valor',
                 'Valor Consignado', 'Imagem'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].codigo))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(lista[i].nome)
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)

                item3 = QTableWidgetItem(lista[i].categoria)
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)

                item4 = QTableWidgetItem(lista[i].ref)
                item4.setFlags(item4.flags() & ~Qt.ItemIsEditable)

                preco = format(lista[i].preco, '.2f')
                item5 = QTableWidgetItem(str(preco))
                item5.setFlags(item5.flags() & ~Qt.ItemIsEditable)

                preco_consignado = format(lista[i].preco_consignado, '.2f')
                item6 = QTableWidgetItem(str(preco_consignado))
                item6.setFlags(item6.flags() & ~Qt.ItemIsEditable)
                if lista[i].image == caminho_images+'\\bebida.jpg':
                    item7 = QTableWidgetItem('Não')
                    item7.setBackground(QColor(105, 45, 33))
                else:
                    item7 = QTableWidgetItem('Sim')
                    item7.setBackground(QColor(44, 138, 82))
                item7.setFlags(item6.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
                self.setItem(numero, 3, item4)
                self.setItem(numero, 4, item5)
                self.setItem(numero, 5, item6)
                self.setItem(numero, 6, item7)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_categorias(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(1)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 150)
            self.setHorizontalHeaderLabels(['Nome'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].nome))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_entregadores(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(3)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 150)
            self.setHorizontalHeaderLabels(['Id', 'Nome', 'Telefone'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].id))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(str(lista[i].nome))
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3 = QTableWidgetItem(str(lista[i].telefone))
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_tipos_festa(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(2)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 150)
            self.setHorizontalHeaderLabels(['Id', 'Nome'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].id))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(str(lista[i].nome))
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_locais_festa(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(3)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 150)
            self.setHorizontalHeaderLabels(['Id', 'Nome', 'Contato'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].id))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(str(lista[i].nome))
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3 = QTableWidgetItem(str(lista[i].contato))
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_festas_confirmadas(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(5)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 300)
            self.setHorizontalHeaderLabels(
                ['Número', 'Data', 'Local', 'Nome', 'Estado'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].numero))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                if lista[i].data is not None:
                    dia = lista[i].data.day
                    mes = lista[i].data.month
                    ano = lista[i].data.year
                    data_orcamento = f'{dia}/{mes}/{ano}'
                else:
                    data_orcamento = None
                item2 = QTableWidgetItem(data_orcamento)
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3 = QTableWidgetItem(str(lista[i].local))
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
                item4 = QTableWidgetItem(str(lista[i].nome))
                item4.setFlags(item4.flags() & ~Qt.ItemIsEditable)
                item5 = QTableWidgetItem(str(lista[i].estado))
                item5.setFlags(item5.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
                self.setItem(numero, 3, item4)
                self.setItem(numero, 4, item5)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_produtos_festa(self, n_orcamento=None):
        if n_orcamento is None:
            lista = []
        else:
            lista = Festa(n_orcamento).produtos
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(6)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 280)
            self.setHorizontalHeaderLabels(
                ['Código', 'Descrição', 'Referência', 'Quantidade',
                 'Valor Unitário', 'Valor Total'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(lista[i][0])
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(lista[i][1])
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                item3 = QTableWidgetItem(lista[i][2])
                item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
                item4 = QTableWidgetItem(str(lista[i][3]).replace('.', ','))
                item4.setFlags(item4.flags() & ~Qt.ItemIsEditable)
                item5 = QTableWidgetItem(
                    (f'R${lista[i][4]:.2f}').replace('.', ','))
                item5.setFlags(item5.flags() & ~Qt.ItemIsEditable)
                valor_total = lista[i][3] * lista[i][4]
                item6 = QTableWidgetItem(
                    (f'R${valor_total:.2f}').replace('.', ','))
                item6.setFlags(item6.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
                self.setItem(numero, 2, item3)
                self.setItem(numero, 3, item4)
                self.setItem(numero, 4, item5)
                self.setItem(numero, 5, item6)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))

    def tabela_clientes(self, lista):
        if len(lista) >= 1:
            self.clear()
            self.setRowCount(len(lista))
            for i in range(self.rowCount()):
                self.setRowHeight(i, 20)
            self.setColumnCount(2)
            for i in range(self.columnCount()):
                self.setColumnWidth(i, 150)
            self.setColumnWidth(1, 350)
            self.setHorizontalHeaderLabels(['Código', 'Nome'])
            for numero, i in enumerate(lista):
                item1 = QTableWidgetItem(str(lista[i].codigo))
                item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
                item2 = QTableWidgetItem(str(lista[i].nome))
                item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
                self.setItem(numero, 0, item1)
                self.setItem(numero, 1, item2)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            self.setItem(0, 0, QTableWidgetItem('Sem Registros'))


class MyButton(QPushButton):
    def __init__(self, texto):
        super().__init__()
        self.setText(texto)
        self.janela_pai = self.parent()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clicked.emit()


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

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.focusNextChild()

    def remover_widgets(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def confirm(self, titulo, mensagem):
        resposta = QMessageBox.question(
            self, titulo, mensagem)
        if resposta == QMessageBox.Yes:
            return True
        else:
            return False

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

                self.usuario = codigo
                self.setWindowTitle('Início')
                self.remover_widgets()
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
        self.button_entrar.clicked.connect(
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

        def show_w4():
            self.w4 = MyWindow('Produtos', usuario=self.usuario)
            self.w4.w4_produtos()

        def show_w5():
            self.w5 = MyWindow('Eventos', usuario=self.usuario)
            self.w5.w5_eventos()

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
        self.button_produtos.clicked.connect(lambda: show_w4())
        self.button_eventos.clicked.connect(lambda: show_w5())

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

        def w3w(table):
            if table.item(table.currentRow(), 0) is not None:
                self.w3w = MyWindow('Janela', usuario='1')
                self.w3w.w3_check_remove_user(table)

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
        self.w3_input_nome.returnPressed.connect(
            lambda: w3w(self.w3_table_usuarios)
        )
        self.w3_button_remover.clicked.connect(
            lambda: w3w(self.w3_table_usuarios)
        )

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

    # Função para checar a remoção do usuario
    def w3_check_remove_user(self, table):

        def check_senha_user(senha, usuario, usuarios):
            if senha == usuarios[usuario].senha:
                return True
            else:
                return False

        def remove_user(senha, usuario):
            usuarios = get_usuarios()
            if check_senha_user(senha.text(), usuario, usuarios):
                usuarios[usuario].remove_usuario_database()
            else:
                MyMessageBox('Senha Incorreta!')
            self.close()

        self.user_to_remove = table.item(table.currentRow(), 0).text()

        self.w3_label_title_check_senha = QLabel(
            f'Deseja remover o usuário {self.user_to_remove}?')
        self.w3_label_check_senha = QLabel('Senha do Usuário: ')
        self.w3_input_check_senha = QLineEdit()
        self.w3_button_yes_check_senha = MyButton('Sim')
        self.w3_button_no_check_senha = MyButton('Não')

        self.w3_button_yes_check_senha.clicked.connect(
            lambda: remove_user(self.w3_input_check_senha, self.user_to_remove)
        )
        self.w3_button_yes_check_senha.clicked.connect(
            lambda: table.tabela_usuarios(get_usuarios())
        )
        self.w3_button_no_check_senha.clicked.connect(lambda: self.close())

        self.layout.addWidget(self.w3_label_title_check_senha, 1, 1, 1, 2)
        self.layout.addWidget(self.w3_label_check_senha, 2, 1, 1, 1)
        self.layout.addWidget(self.w3_input_check_senha, 2, 2, 1, 1)
        self.layout.addWidget(self.w3_button_yes_check_senha, 3, 1, 1, 1)
        self.layout.addWidget(self.w3_button_no_check_senha, 3, 2, 1, 1)

        self.show()

    def w4_produtos(self):

        def show_image(table):
            item = table.item(table.currentRow(), 1).text()

            produtos = get_produtos()
            produto_selecionado = table.item(table.currentRow(), 0).text()
            imagem = produtos[produto_selecionado].image

            self.w4_image = MyWindow(item)
            self.w4_image.w4_image(caminho_imagem=imagem)

        def att_w4_table(pesquisa, table):
            table.tabela_produtos(get_produtos(nome=pesquisa))

        def change_image(table):
            item = table.item(table.currentRow(), 0).text()
            caminho_arquivo, _ = QFileDialog.getOpenFileName(
                self, "Selecionar Arquivo")
            if caminho_arquivo:
                cur_tw.execute(
                    f"""
                    UPDATE PRODUTOS
                    SET IMAGEM = '{caminho_arquivo}'
                    WHERE CODIGO = '{item}'
                    """
                )
                conn_tw.commit()
                MyMessageBox('Imagem Alterada!')

        def show_categorias():
            self.w_categorias = MyWindow('Categorias')
            self.w_categorias.w4_categorias()

        def change_categoria(table):
            item = table.item(table.currentRow(), 1).text()
            self.w_change_categoria = MyWindow(f'{item}')
            self.w_change_categoria.w4_change_categoria(table)

        # Menu da janela
        self.w4_menu_bar = QMenuBar(self)
        self.setMenuBar(self.w4_menu_bar)
        self.w4_menu_arquivo = QMenu('Arquivo', self)
        self.w4_menu_bar.addMenu(self.w4_menu_arquivo)
        self.w4_acao_categorias = QAction('Categorias', self)
        self.w4_menu_arquivo.addAction(self.w4_acao_categorias)

        # Widgets da janela
        self.w4_label_pesquisa = QLabel('Pesquisa')
        self.w4_input_pesquisa = QLineEdit()
        self.w4_table_produtos = MyTable()
        self.w4_button_image = MyButton('Ver Imagem')
        self.w4_button_change_image = MyButton('Trocar Imagem')
        self.w4_button_categoria_produto = MyButton('Categoria')

        # Ações dos Widgets
        self.w4_table_produtos.tabela_produtos(get_produtos())
        self.w4_input_pesquisa.textChanged.connect(
            lambda: att_w4_table(self.w4_input_pesquisa.text(),
                                 self.w4_table_produtos))
        self.w4_button_image.clicked.connect(
            lambda: show_image(self.w4_table_produtos))
        self.w4_button_change_image.clicked.connect(
            lambda: change_image(self.w4_table_produtos)
        )
        self.w4_acao_categorias.triggered.connect(lambda: show_categorias())
        self.w4_button_categoria_produto.clicked.connect(
            lambda: change_categoria(self.w4_table_produtos)
        )

        # Layout da janela
        self.layout.addWidget(self.w4_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.w4_input_pesquisa, 0, 1, 1, 2)
        self.layout.addWidget(self.w4_table_produtos, 1, 0, 1, 3)
        self.layout.addWidget(self.w4_button_image, 2, 0, 1, 1)
        self.layout.addWidget(self.w4_button_change_image, 2, 1, 1, 1)
        self.layout.addWidget(self.w4_button_categoria_produto, 2, 2, 1, 1)

        self.showMaximized()

    def w4_image(self, caminho_imagem=caminho_images+'\\bebida.jpg'):

        self.w4_label_image = QLabel()
        pixmap = QPixmap(caminho_imagem)
        pixmap = pixmap.scaled(480, 480)
        self.w4_label_image.setPixmap(pixmap)

        self.layout.addWidget(self.w4_label_image, 0, 0, 1, 1)

        self.show()

    def w4_categorias(self):

        def add_categoria(lineedit: QLineEdit, table: MyTable):
            nova_categoria = Categoria(lineedit.text())
            nova_categoria.add_to_tablesql()
            table.tabela_categorias(get_categorias())
            lineedit.setText('')

        def remove_categoria(table: MyTable):
            nome_categoria = table.item(table.currentRow(), 0).text()
            if self.confirm('Remover categoria', f"""
            Tem certeza que deseja remover a categoria {nome_categoria}?
            """):
                categoria_to_remove = Categoria(nome_categoria)
                categoria_to_remove.remove_fromsql()
                table.tabela_categorias(get_categorias())
                produtos = get_produtos(categoria=nome_categoria)
                for i in produtos:
                    produtos[i].change_categoria('Não Definido')

        self.w4_label_categoria = QLabel('Nova Categoria: ')
        self.w4_input_categoria = QLineEdit()
        self.w4_button_add_categoria = MyButton('Adicionar Categoria')
        self.w4_table_categorias = MyTable()
        self.w4_button_remove_categoria = MyButton('Remover Categoria')

        self.w4_table_categorias.tabela_categorias(get_categorias())
        self.w4_button_add_categoria.clicked.connect(
            lambda: add_categoria(self.w4_input_categoria,
                                  self.w4_table_categorias)
        )
        self.w4_button_remove_categoria.clicked.connect(
            lambda: remove_categoria(self.w4_table_categorias)
        )

        self.layout.addWidget(self.w4_label_categoria, 0, 0, 1, 1)
        self.layout.addWidget(self.w4_input_categoria, 0, 1, 1, 1)
        self.layout.addWidget(self.w4_button_add_categoria, 2, 0, 1, 2)
        self.layout.addWidget(self.w4_table_categorias, 3, 0, 1, 2)
        self.layout.addWidget(self.w4_button_remove_categoria, 4, 0, 1, 2)

        self.show()

    def w4_change_categoria(self, table):

        def change_categoria(produtos, produto, nova_categoria, table):
            produtos[produto].change_categoria(nova_categoria)
            table.tabela_produtos(get_produtos())

        item = table.item(table.currentRow(), 0).text()
        produtos = get_produtos()
        self.w4_label_atual_categoria = QLabel(
            f'Categoria Atual: {produtos[item].nome}')
        self.w4_label_nova_categoria = QLabel('Nova Categoria do Item: ')
        self.w4_combo_categoria = QComboBox()
        categorias = get_categorias()
        for categoria in categorias:
            self.w4_combo_categoria.addItem(categorias[categoria].nome)
        self.w4_button_trocar_categoria = MyButton('Trocar Categoria')

        self.w4_button_trocar_categoria.clicked.connect(
            lambda: change_categoria(produtos, item,
                                     self.w4_combo_categoria.currentText(),
                                     table)
        )
        self.w4_button_trocar_categoria.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.w4_label_atual_categoria, 0, 0, 1, 2)
        self.layout.addWidget(self.w4_label_nova_categoria, 1, 0, 1, 1)
        self.layout.addWidget(self.w4_combo_categoria, 1, 1, 1, 1)
        self.layout.addWidget(self.w4_button_trocar_categoria, 2, 0, 1, 2)

        self.show()

    def w5_eventos(self):

        def show_w5_entregadores():
            self.w5_e = MyWindow('Entregadores', usuario=self.usuario)
            self.w5_e.w5_entregadores()

        def show_w5_tipos_festa():
            self.w5_tf = MyWindow('Tipos de Festa', usuario=self.usuario)
            self.w5_tf.w5_tipos_de_festa()

        def show_w5_locais_festa():
            self.w5_lf = MyWindow('Locais de Festa', usuario=self.usuario)
            self.w5_lf.w5_locais_de_festa()

        def show_w6_festa(table=None):
            n_orcamento = None
            if table is not None:
                n_orcamento = table.item(table.currentRow(), 0).text()
                n_orcamento = int(n_orcamento)

            self.w6_f = MyWindow('Festa', usuario=self.usuario)
            self.w6_f.w6_festa(n_orcamento, table)

        def show_w5_nova_festa(table):
            self.w5_nf = MyWindow('Nova Festa', usuario=self.usuario)
            self.w5_nf.w5_nova_festa(table)

        def delete_festa(table: MyTable):
            festa_to_delete = table.item(table.currentRow(), 0).text()
            if self.confirm('Remover Festa',
                            f"""
            Tem certeza que deseja remover a festa {festa_to_delete}?
            """):
                cur_tw.execute(
                    f"""
                    DELETE FROM FESTAS_CONFIRMADAS
                    WHERE N_ORCAMENTO = {festa_to_delete}
                    """
                )
                cur_tw.execute(
                    f"""
                    DELETE FROM FESTAS
                    WHERE N_ORCAMENTO = {festa_to_delete}
                    """
                )
                conn_tw.commit()
                table.tabela_festas_confirmadas(get_festas_confirmadas())

        # Menu da janela
        self.w5_menu_bar = QMenuBar(self)
        self.setMenuBar(self.w5_menu_bar)
        self.w5_menu_cadastros = QMenu('Cadastros', self)
        self.w5_menu_bar.addMenu(self.w5_menu_cadastros)
        self.w5_acao_entregadores = QAction('Entregadores', self)
        self.w5_menu_cadastros.addAction(self.w5_acao_entregadores)
        self.w5_acao_tiposdefesta = QAction('Tipos de Festa', self)
        self.w5_menu_cadastros.addAction(self.w5_acao_tiposdefesta)
        self.w5_acao_locaisdefesta = QAction('Locais de Festa', self)
        self.w5_menu_cadastros.addAction(self.w5_acao_locaisdefesta)

        # Widgets da janela
        self.w5_label_titulo_eventos = QLabel('Eventos Confirmados')
        self.w5_label_filtro_norcamento = QLabel('N° Orçamento:')
        self.w5_input_filtro_norcamento = QLineEdit()
        self.w5_checkbox_filtro_norcamento = QCheckBox()
        self.w5_label_filtro_data = QLabel('Data:')
        self.w5_input_filtro_data = QLineEdit()
        self.w5_checkbox_filtro_data = QCheckBox()
        self.w5_label_filtro_local = QLabel('Local da Festa:')
        self.w5_input_filtro_local = QLineEdit()
        self.w5_checkbox_filtro_local = QCheckBox()
        self.w5_label_filtro_nome = QLabel('Nome:')
        self.w5_input_filtro_nome = QLineEdit()
        self.w5_checkbox_filtro_nome = QCheckBox()
        self.w5_label_filtro_estado = QLabel('Estado:')
        self.w5_combobox_filtro_estado = QComboBox()
        self.w5_checkbox_filtro_estado = QCheckBox()
        self.w5_table_eventos_confirmados = MyTable()
        self.w5_button_consultar_festa = MyButton('Consultar Festa')
        self.w5_button_adicionar_festa = MyButton('Adicionar Festa')
        self.w5_button_remover_festa = MyButton('Remover Festa')
        self.w5_button_imprimir_festa = MyButton('Imprimir Festa')
        self.w5_button_impressoes = MyButton('Impressões')

        # Propriedades dos Widgets
        self.w5_input_filtro_data.setInputMask('00/00/0000')
        self.w5_input_filtro_norcamento.setInputMask('000000')
        self.w5_combobox_filtro_estado.addItem('Não Confirmado')
        self.w5_combobox_filtro_estado.addItem('Confirmado')
        self.w5_combobox_filtro_estado.addItem('Entregue')
        self.w5_combobox_filtro_estado.addItem('Recolhido')

        # Ações dos Widgets
        self.w5_table_eventos_confirmados.tabela_festas_confirmadas(
            get_festas_confirmadas()
        )
        self.w5_acao_entregadores.triggered.connect(
            lambda: show_w5_entregadores())
        self.w5_acao_tiposdefesta.triggered.connect(
            lambda: show_w5_tipos_festa()
        )
        self.w5_acao_locaisdefesta.triggered.connect(
            lambda: show_w5_locais_festa()
        )
        self.w5_button_consultar_festa.clicked.connect(
            lambda: show_w6_festa(self.w5_table_eventos_confirmados)
        )
        self.w5_button_adicionar_festa.clicked.connect(
            lambda: show_w5_nova_festa(self.w5_table_eventos_confirmados)
        )
        self.w5_button_remover_festa.clicked.connect(
            lambda: delete_festa(self.w5_table_eventos_confirmados)
        )

        # Layout da janela
        self.layout.addWidget(self.w5_label_titulo_eventos, 0, 0, 1, 12)
        self.layout.addWidget(self.w5_label_filtro_norcamento, 1, 0, 1, 1)
        self.layout.addWidget(self.w5_input_filtro_norcamento, 1, 1, 1, 1)
        self.layout.addWidget(self.w5_checkbox_filtro_norcamento, 1, 2, 1, 1)
        self.layout.addWidget(self.w5_label_filtro_data, 1, 3, 1, 1)
        self.layout.addWidget(self.w5_input_filtro_data, 1, 4, 1, 1)
        self.layout.addWidget(self.w5_checkbox_filtro_data, 1, 5, 1, 1)
        self.layout.addWidget(self.w5_label_filtro_local, 1, 6, 1, 1)
        self.layout.addWidget(self.w5_input_filtro_local, 1, 7, 1, 1)
        self.layout.addWidget(self.w5_checkbox_filtro_local, 1, 8, 1, 1)
        self.layout.addWidget(self.w5_label_filtro_nome, 1, 9, 1, 1)
        self.layout.addWidget(self.w5_input_filtro_nome, 1, 10, 1, 1)
        self.layout.addWidget(self.w5_checkbox_filtro_nome, 1, 11, 1, 1)
        self.layout.addWidget(self.w5_label_filtro_estado, 2, 0, 1, 1)
        self.layout.addWidget(self.w5_combobox_filtro_estado, 2, 1, 1, 1)
        self.layout.addWidget(self.w5_checkbox_filtro_estado, 2, 2, 1, 1)
        self.layout.addWidget(self.w5_table_eventos_confirmados, 3, 0, 1, 12)
        self.layout.addWidget(self.w5_button_consultar_festa, 4, 0, 1, 3)
        self.layout.addWidget(self.w5_button_adicionar_festa, 4, 3, 1, 3)
        self.layout.addWidget(self.w5_button_remover_festa, 4, 6, 1, 3)
        self.layout.addWidget(self.w5_button_imprimir_festa, 4, 9, 1, 3)
        self.layout.addWidget(self.w5_button_impressoes, 5, 0, 1, 12)

        self.showMaximized()

    def w5_nova_festa(self, table):

        def nova_festa(n_orcamento=None, table=None):
            if n_orcamento is None:
                cur_mc.execute(
                    """
                    SELECT MAX(AN190_PEDIDO)
                    FROM MC190_ORCAMENTO
                    """
                )
                select = cur_mc.fetchone()
                n_orcamento = select[0] + 1
                hoje = datetime.datetime.today()
                dia = hoje.day
                mes = hoje.month
                ano = hoje.year
                cur_mc.execute(
                    f"""
                    INSERT INTO MC190_ORCAMENTO
                    (AN190_PEDIDO, AD190_EMISSAO, AN190_CLIENTE,
                    AC190_BAIXARESTOQUE,
                    AC190_PRECOPROD, AC190_SIT, AC190_TIPOPRECO,
                    AC190_DESC_PERC, AN190_MARGE_CUSTO, AN190_EMPRESA)
                    VALUES
                    ({n_orcamento},'{ano}-{mes}-{dia}', 0, 'N', 'S', 'A', 'D',
                    0, 0, 0)
                    """
                )
                conn_mc.commit()
            else:
                cur_mc.execute(
                    """
                    SELECT AN190_PEDIDO FROM MC190_ORCAMENTO
                    """
                )
                select = cur_mc.fetchall()
                n_orcamentos = []
                for n in select:
                    n_orcamentos.append(n[0])
                if int(n_orcamento) not in n_orcamentos:
                    return MyMessageBox('Orçamento Não Encontrado!')
            cur_tw.execute("""
                SELECT N_ORCAMENTO FROM FESTAS
                """)
            select1 = cur_tw.fetchall()
            n_festas = []
            for n in select1:
                n_festas.append(n[0])
            if n_orcamento not in n_festas:
                cur_tw.execute(
                    f"""
                    INSERT INTO FESTAS (N_ORCAMENTO)
                    VALUES ({n_orcamento})
                    """
                )
                cur_tw.execute(
                    f"""
                    INSERT INTO FESTAS_CONFIRMADAS (N_ORCAMENTO)
                    VALUES ({n_orcamento})
                    """
                )
            self.w_nova_festa = MyWindow('Nova Festa', usuario=self.usuario)
            self.w_nova_festa.w6_festa(int(n_orcamento), table)

        self.w5_button_nova_festa = MyButton('Nova Festa')
        self.w5_input_num_nova_festa = QLineEdit()
        self.w5_button_num_nova_festa = MyButton(
            'Nova Festa a partir do orçamento')

        self.w5_input_num_nova_festa.setInputMask('000000')

        self.w5_button_nova_festa.clicked.connect(
            lambda: nova_festa(n_orcamento=None, table=table)
        )
        self.w5_button_nova_festa.clicked.connect(
            lambda: self.close()
        )
        self.w5_button_num_nova_festa.clicked.connect(
            lambda: nova_festa(n_orcamento=self.w5_input_num_nova_festa.text(),
                               table=table)
        )
        self.w5_button_num_nova_festa.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.w5_button_nova_festa, 1, 0, 1, 12)
        self.layout.addWidget(self.w5_input_num_nova_festa, 2, 0, 1, 12)
        self.layout.addWidget(self.w5_button_num_nova_festa, 3, 0, 1, 12)

        self.resize(300, 150)
        self.show()

    def w5_entregadores(self):

        def add_entregador(table: MyTable, nome_entregador,
                           telefone_entregador):
            entregador = Entregador(None, nome_entregador.text(),
                                    telefone_entregador.text())
            entregador.add_to_sql()
            table.tabela_entregadores(get_entregadores())
            nome_entregador.setText('')
            telefone_entregador.setText('')

        def remove_entregador(table: MyTable):
            id_entregador = table.item(table.currentRow(), 0).text()
            nome_entregador = table.item(table.currentRow(), 1).text()
            if self.confirm('Remover Entregador',
                            f"""
Tem certeza que deseja remover o entregador {nome_entregador}?
                            """):
                entregadores = get_entregadores()
                entregadores[int(id_entregador)].remove_from_sql()
                table.tabela_entregadores(get_entregadores())

        self.w5_label_entregadores = QLabel('Entregadores')
        self.w5_label_novo_entregador = QLabel('Entregador:')
        self.w5_input_novo_entregador = QLineEdit()
        self.w5_label_telefone_entregador = QLabel('Telefone:')
        self.w5_input_telefone_entregador = QLineEdit()
        self.w5_button_novo_entregador = MyButton('Novo Entregador')
        self.w5_table_entregadores = MyTable()
        self.w5_button_remove_entregador = MyButton('Remover Entregador')

        self.w5_input_telefone_entregador.setInputMask('(00) 00000-0000')

        self.w5_table_entregadores.tabela_entregadores(get_entregadores())
        self.w5_button_novo_entregador.clicked.connect(
            lambda: add_entregador(self.w5_table_entregadores,
                                   self.w5_input_novo_entregador,
                                   self.w5_input_telefone_entregador)
        )
        self.w5_button_remove_entregador.clicked.connect(
            lambda: remove_entregador(self.w5_table_entregadores)
        )

        self.layout.addWidget(self.w5_label_entregadores, 0, 0, 1, 12)
        self.layout.addWidget(self.w5_label_novo_entregador, 1, 0, 1, 3)
        self.layout.addWidget(self.w5_input_novo_entregador, 1, 3, 1, 3)
        self.layout.addWidget(self.w5_label_telefone_entregador, 1, 6, 1, 3)
        self.layout.addWidget(self.w5_input_telefone_entregador, 1, 9, 1, 3)
        self.layout.addWidget(self.w5_button_novo_entregador, 2, 0, 1, 12)
        self.layout.addWidget(self.w5_table_entregadores, 3, 0, 1, 12)
        self.layout.addWidget(self.w5_button_remove_entregador, 4, 0, 1, 12)

        self.resize(800, 600)
        self.show()

    def w5_tipos_de_festa(self):

        def add_tipo_festa(input, table: MyTable):
            nome_tipo_festa = input.text()
            novo_tipo_festa = TipoFesta(None, nome_tipo_festa)
            novo_tipo_festa.add_to_sql()
            table.tabela_tipos_festa(get_tipos_festa())
            input.setText('')

        def remove_tipo_festa(table: MyTable):
            id_tipo_festa = table.item(table.currentRow(), 0).text()
            nome_tipo_festa = table.item(table.currentRow(), 1).text()
            if self.confirm('Remover Tipo de Festa',
                            f"""
Deseja remover o tipo de festa {nome_tipo_festa}?
                            """):
                tipos_festa = get_tipos_festa()
                tipos_festa[int(id_tipo_festa)].remove_from_sql()
                table.tabela_tipos_festa(get_tipos_festa())

        self.w5_label_tipo_festa = QLabel('Tipos de festas')
        self.w5_label_novo_tipo_festa = QLabel('Novo Tipo de Festa:')
        self.w5_input_novo_tipo_festa = QLineEdit()
        self.w5_button_novo_tipo_festa = MyButton(
            'Adicionar Tipo de Festa')
        self.w5_table_tipos_festa = MyTable()
        self.w5_button_remove_tipo_festa = MyButton(
            'Remover Tipo de Festa')

        self.w5_table_tipos_festa.tabela_tipos_festa(get_tipos_festa())
        self.w5_button_novo_tipo_festa.clicked.connect(
            lambda: add_tipo_festa(self.w5_input_novo_tipo_festa,
                                   self.w5_table_tipos_festa)
        )
        self.w5_button_remove_tipo_festa.clicked.connect(
            lambda: remove_tipo_festa(self.w5_table_tipos_festa)
        )

        self.layout.addWidget(self.w5_label_tipo_festa, 0, 0, 1, 12)
        self.layout.addWidget(self.w5_label_novo_tipo_festa, 1, 0, 1, 4)
        self.layout.addWidget(self.w5_input_novo_tipo_festa, 1, 4, 1, 4)
        self.layout.addWidget(self.w5_button_novo_tipo_festa, 1, 8, 1, 4)
        self.layout.addWidget(self.w5_table_tipos_festa, 2, 0, 1, 12)
        self.layout.addWidget(self.w5_button_remove_tipo_festa, 3, 0, 1, 12)

        self.resize(800, 600)
        self.show()

    def w5_locais_de_festa(self):

        def show_local_screen(table):
            self.win = MyWindow('Locais de Festa', usuario=self.usuario)
            self.win.w5_add_local_festa(table)

        def show_edit_local_screen(table):
            id_to_change = table.item(table.currentRow(), 0).text()
            self.win = MyWindow('Locais de Festa', usuario=self.usuario)
            self.win.w5_add_local_festa(table, id_to_change)

        def remove_local_festa(table: MyTable):
            id_local_festa = table.item(table.currentRow(), 0).text()
            nome_local_festa = table.item(table.currentRow(), 1).text()
            if self.confirm('Remover Local de Festa', f"""
            Deseja Remover o local de festas {nome_local_festa}?
            """):
                locais_festa = get_locais_festa()
                locais_festa[int(id_local_festa)].remove_from_sql()
                table.tabela_locais_festa(get_locais_festa())

        self.w5_label_locais_de_festa = QLabel('Locais de Festa')
        self.w5_button_novo_local_festa = MyButton('Novo Local de Festa')
        self.w5_table_locais_festa = MyTable()
        self.w5_button_editar_local_festa = MyButton('Editar Local de Festa')
        self.w5_button_remove_local_festa = MyButton('Remover Local de Festa')

        self.w5_table_locais_festa.tabela_locais_festa(get_locais_festa())
        self.w5_button_novo_local_festa.clicked.connect(
            lambda: show_local_screen(self.w5_table_locais_festa)
        )
        self.w5_button_editar_local_festa.clicked.connect(
            lambda: show_edit_local_screen(self.w5_table_locais_festa)
        )
        self.w5_button_remove_local_festa.clicked.connect(
            lambda: remove_local_festa(self.w5_table_locais_festa)
        )

        self.layout.addWidget(self.w5_label_locais_de_festa, 0, 0, 1, 12)
        self.layout.addWidget(self.w5_button_novo_local_festa, 1, 0, 1, 12)
        self.layout.addWidget(self.w5_table_locais_festa, 2, 0, 1, 12)
        self.layout.addWidget(self.w5_button_editar_local_festa, 3, 0, 1, 6)
        self.layout.addWidget(self.w5_button_remove_local_festa, 3, 6, 1, 6)

        self.resize(800, 600)
        self.show()

    def w5_add_local_festa(self, table: MyTable, id=None):

        def add_local_festa(table: MyTable, input_nome, input_contato,
                            input_logradouro,
                            input_numero, input_bairro, input_cidade,
                            input_cep, id):
            if input_nome.text() != '':
                if id is None:
                    local_to_add = LocalFesta(None, input_nome.text(),
                                              input_contato.text(),
                                              input_logradouro.text(),
                                              input_numero.text(),
                                              input_bairro.text(),
                                              input_cep.text(),
                                              input_cidade.text())
                    local_to_add.add_to_sql()
                else:
                    local_to_add = LocalFesta(id, input_nome.text(),
                                              input_contato.text(),
                                              input_logradouro.text(),
                                              input_numero.text(),
                                              input_bairro.text(),
                                              input_cep.text(),
                                              input_cidade.text())
                    local_to_add.update_sql()
                table.tabela_locais_festa(get_locais_festa())

        self.w5_label_novo_local_de_festa = QLabel('Novo Local:')
        self.w5_input_novo_local_de_festa = QLineEdit()
        self.w5_label_contato_local_festa = QLabel('Contato:')
        self.w5_input_contato_local_festa = QLineEdit()
        self.w5_label_logradouro_local_festa = QLabel('Logradouro:')
        self.w5_input_logradouro_local_festa = QLineEdit()
        self.w5_label_numero_local = QLabel('Número:')
        self.w5_input_numero_local = QLineEdit()
        self.w5_label_bairro_local = QLabel('Bairro:')
        self.w5_input_bairro_local = QLineEdit()
        self.w5_label_cidade_local = QLabel('Cidade:')
        self.w5_input_cidade_local = QLineEdit()
        self.w5_label_cep_local = QLabel('CEP:')
        self.w5_input_cep_local = QLineEdit()
        self.w5_button_confirmar_novo_local = MyButton('Confirmar')
        self.w5_button_cancelar_novo_local = MyButton('Cancelar')

        self.w5_input_contato_local_festa.setInputMask('(00) 00000-0000')
        self.w5_input_cep_local.setInputMask('00000-000')

        if id is not None:
            int_id = int(id)
            locais_festa = get_locais_festa()
            self.w5_input_novo_local_de_festa.setText(
                locais_festa[int_id].nome)
            self.w5_input_contato_local_festa.setText(
                locais_festa[int_id].contato)
            self.w5_input_logradouro_local_festa.setText(
                locais_festa[int_id].logradouro)
            self.w5_input_numero_local.setText(locais_festa[int_id].numero)
            self.w5_input_bairro_local.setText(locais_festa[int_id].bairro)
            self.w5_input_cidade_local.setText(locais_festa[int_id].cidade)
            self.w5_input_cep_local.setText(locais_festa[int_id].cep)

        self.w5_button_confirmar_novo_local.clicked.connect(
            lambda: add_local_festa(table, self.w5_input_novo_local_de_festa,
                                    self.w5_input_contato_local_festa,
                                    self.w5_input_logradouro_local_festa,
                                    self.w5_input_numero_local,
                                    self.w5_input_bairro_local,
                                    self.w5_input_cidade_local,
                                    self.w5_input_cep_local,
                                    id)
        )
        self.w5_button_confirmar_novo_local.clicked.connect(
            lambda: self.close()
        )
        self.w5_button_cancelar_novo_local.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.w5_label_novo_local_de_festa, 0, 0, 1, 2)
        self.layout.addWidget(self.w5_input_novo_local_de_festa, 0, 2, 1, 10)
        self.layout.addWidget(self.w5_label_contato_local_festa, 1, 0, 1, 2)
        self.layout.addWidget(self.w5_input_contato_local_festa, 1, 2, 1, 10)
        self.layout.addWidget(self.w5_label_logradouro_local_festa, 2, 0, 1, 2)
        self.layout.addWidget(self.w5_input_logradouro_local_festa, 2, 2, 1, 6)
        self.layout.addWidget(self.w5_label_numero_local, 2, 8, 1, 1)
        self.layout.addWidget(self.w5_input_numero_local, 2, 9, 1, 3)
        self.layout.addWidget(self.w5_label_bairro_local, 3, 0, 1, 2)
        self.layout.addWidget(self.w5_input_bairro_local, 3, 2, 1, 4)
        self.layout.addWidget(self.w5_label_cep_local, 3, 6, 1, 2)
        self.layout.addWidget(self.w5_input_cep_local, 3, 8, 1, 4)
        self.layout.addWidget(self.w5_label_cidade_local, 4, 0, 1, 2)
        self.layout.addWidget(self.w5_input_cidade_local, 4, 2, 1, 10)
        self.layout.addWidget(self.w5_button_confirmar_novo_local, 5, 0, 1, 6)
        self.layout.addWidget(self.w5_button_cancelar_novo_local, 5, 6, 1, 6)

        self.resize(800, 600)
        self.show()

    def w6_festa(self, n_orcamento=None, table=None | MyTable):

        def show_wse(*args):
            self.wse = MyWindow('Entregadores', usuario=self.usuario)
            self.wse.w_search_entregadores(*args)

        def show_wstf(*args):
            self.wstf = MyWindow('Tipos de Festa', usuario=self.usuario)
            self.wstf.w_search_tipos_festa(*args)

        def show_wslf(*args):
            self.wslf = MyWindow('Locais de Festa', usuario=self.usuario)
            self.wslf.w_search_locais_festa(*args)

        def show_wsp(*args):
            self.wsp = MyWindow('Produtos', usuario=self.usuario)
            self.wsp.w_search_produtos(*args)

        def show_wsc(*args):
            self.wsc = MyWindow('Clientes', usuario=self.usuario)
            self.wsc.w_search_clientes(*args)

        def att_input(input_cod, input_text, function):
            input_text.setReadOnly(False)
            input_text.setEnabled(True)
            locais_festa = function()
            print(locais_festa)
            codigo_local = int(input_cod.text())
            print(codigo_local)
            if codigo_local in locais_festa:
                input_text.setText(locais_festa[codigo_local].nome)
                input_text.setReadOnly(True)
                input_text.setEnabled(False)

        def att_janela(festa, label):
            valor_total = 0
            produtos = festa.produtos
            for produto in festa.produtos:
                total_produto = produtos[produto][3] * produtos[produto][4]
                valor_total += total_produto
            label.setText(
                (f'Valor Total: R${valor_total:.2f}').replace('.', ',')
            )

        def remove_produto(n_orcamento, table: MyTable):
            nome_produto = table.item(table.currentRow(), 1).text()
            if self.confirm('Remover Produto',
                            f"""
                Tem certeza que deseja remover {nome_produto}?
            """):
                cod_produto = table.item(table.currentRow(), 0).text()
                festa = Festa(int(n_orcamento))
                festa.remove_produto(cod_produto)
                table.tabela_produtos_festa(int(n_orcamento))

        def fill_produto_inputs(input_cod, input_prod, input_qtd, input_valor,
                                checkbox_consignado):
            produtos = get_produtos()
            if input_cod.text() in produtos:
                produto = produtos[input_cod.text()]
                input_prod.setText(f'{produto.nome} {produto.ref}')
                input_qtd.setText('1')
                if checkbox_consignado.isChecked():
                    input_valor.setText(f'{produto.preco_consignado}')
                else:
                    input_valor.setText(f'{produto.preco}')
            else:
                MyMessageBox('Produto não encontrado!')

        def cod_produto_typed(input_cod, *args):
            if len(input_cod.text()) == 7:
                fill_produto_inputs(*args)

        def add_produto_into_festa(table: MyTable, n_orcamento, input_cod,
                                   input_name, input_qtd, input_valor):
            cur_mc.execute(
                f"""
                INSERT INTO MC191_ITEMORCAMENTO
                (AN191_PEDIDO, AC191_PRODUTO, AN191_QTDE, AN191_VALOR,
                AC190_NOMEPRO, AN191_EMPRESA)
                VALUES
                ({n_orcamento},'{input_cod.text()}',{input_qtd.text()},
                {input_valor.text()},'{input_name.text()}',0)
                """
            )
            conn_mc.commit()
            table.tabela_produtos_festa(n_orcamento)
            input_cod.setText('')
            input_name.setText('')
            input_qtd.setText('')
            input_valor.setText('')
            input_cod.setFocus()

        def check_data(data):
            try:
                datetime.datetime.strptime(data, "%d/%m/%Y")
                return True
            except ValueError:
                return False

        def att_festa(n_orcamento, cod_cliente, nome_cliente, tel_cliente,
                      data, local, tipo, qtd_pessoas, qtd_alc, estado,
                      consumo, locacao, avaria, entregador, recolhedor, obs1,
                      obs2):
            # Salvando codigo cliente
            if cod_cliente.text() != '':
                codigo_cliente = cod_cliente.text().split(' ')
                codigo_cliente = int(codigo_cliente[1])
                cur_mc.execute(
                    f"""
                    UPDATE MC190_ORCAMENTO
                    SET AN190_CLIENTE = {codigo_cliente}
                    WHERE AN190_PEDIDO = {n_orcamento}
                    """
                )
                conn_mc.commit()
            cur_mc.execute(
                f"""
                UPDATE MC190_ORCAMENTO
                SET AC190_NOMECLI = '{nome_cliente.text()}'
                WHERE AN190_PEDIDO = {n_orcamento}
                """
            )
            conn_mc.commit()
            cur_mc.execute(
                f"""
                UPDATE MC190_ORCAMENTO
                SET AC190_TELEFONE = '{tel_cliente.text()}'
                WHERE AN190_PEDIDO = {n_orcamento}
                """
            )
            conn_mc.commit()
            cur_mc.execute(
                f"""
                UPDATE MC190_ORCAMENTO
                SET AC190_OBS1 = '{obs1.toPlainText()}'
                WHERE AN190_PEDIDO = {n_orcamento}
                """
            )
            conn_mc.commit()
            cur_mc.execute(
                f"""
                UPDATE MC190_ORCAMENTO
                SET AC190_OBS2 = '{obs2.toPlainText()}'
                WHERE AN190_PEDIDO = {n_orcamento}
                """
            )
            conn_mc.commit()
            if check_data(data.text()):
                data_edit = datetime.datetime.strptime(data.text(), "%d/%m/%Y")
                dia = data_edit.day
                mes = data_edit.month
                ano = data_edit.year
                data_sql = f'{ano}-{mes}-{dia}'
                cur_tw.execute(
                    f"""
                    UPDATE FESTAS
                    SET DATA = '{data_sql}'
                    WHERE N_ORCAMENTO = {n_orcamento}
                    """
                )
                conn_tw.commit()
            else:
                MyMessageBox('Data Inválida!')
            cur_tw.execute(
                f"""
                UPDATE FESTAS
                SET LOCAL = '{local.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS
                SET TIPO = '{tipo.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS
                SET QTD_PESSOAS = {qtd_pessoas.text()}
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS
                SET QTD_ALCOOLICOS = {qtd_alc.text()}
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET ESTADO = '{estado.currentText()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET CONSUMO = '{consumo.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET LOCACAO = '{locacao.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET AVARIA = '{avaria.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET ENTREGADOR = '{entregador.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()
            cur_tw.execute(
                f"""
                UPDATE FESTAS_CONFIRMADAS
                SET RECOLHEDOR = '{recolhedor.text()}'
                WHERE N_ORCAMENTO = {n_orcamento}
                """
            )
            conn_tw.commit()

        # Widgets da janela
        self.w6_label_n_orcamento = QLabel(
            f'Número do Orçamento: {n_orcamento}')
        self.w6_label_cod_cliente = QLabel('')
        self.w6_label_nome_cliente = QLabel('Nome do Cliente:')
        self.w6_input_nome_cliente = QLineEdit()
        self.w6_button_clientes = QPushButton('Clientes')
        self.w6_label_telefone_cliente = QLabel('Telefone do Cliente:')
        self.w6_input_telefone_cliente = QLineEdit()
        self.w6_label_celular_cliente = QLabel('Celular do Cliente:')
        self.w6_input_celular_cliente = QLineEdit()
        self.w6_label_data_evento = QLabel('Data do Evento:')
        self.w6_input_data_evento = QLineEdit()
        self.w6_label_local_evento = QLabel('Local do Evento:')
        self.w6_button_local_evento = QPushButton('Locais de Evento')
        self.w6_input_cod_local_evento = QLineEdit()
        self.w6_input_local_evento = QLineEdit()
        self.w6_label_tipo_festa = QLabel('Tipo de Festa:')
        self.w6_button_tipo_festa = QPushButton('Tipos de Festa')
        self.w6_input_cod_tipo_festa = QLineEdit()
        self.w6_input_tipo_festa = QLineEdit()
        self.w6_label_qtd_pessoas = QLabel('Quantidade de Pessoas:')
        self.w6_input_qtd_pessoas = QLineEdit()
        self.w6_label_qtd_alcoolicos = QLabel(
            'Pessoas que bebem bebida alcoólica:')
        self.w6_input_qtd_alcoolicos = QLineEdit()
        self.w6_label_obs1 = QLabel('Observação 1:')
        self.w6_textarea_obs1 = QTextEdit()
        self.w6_label_obs2 = QLabel('Observação 2:')
        self.w6_textarea_obs2 = QTextEdit()
        self.w6_label_quebra = QLabel(370*'-')
        self.w6_label_produtos = QLabel('Produtos')
        self.w6_label_cod_produto = QLabel('Código:')
        self.w6_button_cod_produto = QPushButton('Produtos')
        self.w6_input_cod_produto = QLineEdit()
        self.w6_input_nome_produto = QLineEdit()
        self.w6_label_quantidade_produto = QLabel('Quantidade:')
        self.w6_input_quantidade_produto = QLineEdit()
        self.w6_checkbox_consignado = QCheckBox('Consignado')
        self.w6_label_valor_produto = QLabel('Valor:')
        self.w6_input_valor_produto = QLineEdit()
        self.w6_button_adicionar_produto = MyButton('Adicionar Produto')
        self.w6_button_remover_produto = MyButton('Remover Produto')
        self.w6_table_produtos = MyTable()
        self.w6_label_valor_total = QLabel('Valor total:')
        self.w6_label_consumo = QLabel('Consumo:')
        self.w6_input_consumo = QLineEdit()
        self.w6_button_carregar_consumo = MyButton('Carregar Consumo')
        self.w6_button_consultar_consumo = MyButton('Consultar Consumo')
        self.w6_label_valor_consumo = QLabel('Valor Consumo:')
        self.w6_label_locacao = QLabel('Locação:')
        self.w6_input_locacao = QLineEdit()
        self.w6_button_carregar_locacao = MyButton('Carregar Locação')
        self.w6_button_consultar_locacao = MyButton('Consultar Locação')
        self.w6_label_valor_locacao = QLabel('Valor Locação:')
        self.w6_label_avaria = QLabel('Avaria:')
        self.w6_input_avaria = QLineEdit()
        self.w6_button_carregar_avaria = MyButton('Carregar Avaria')
        self.w6_button_consultar_avaria = MyButton('Consultar Avaria')
        self.w6_label_valor_avaria = QLabel('Valor Avaria:')
        self.w6_label_entregador = QLabel('Entregador:')
        self.w6_button_entregador = QPushButton('Entregadores')
        self.w6_input_cod_entregador = QLineEdit()
        self.w6_input_entregador = QLineEdit()
        self.w6_label_recolhedor = QLabel('Recolhedor:')
        self.w6_button_recolhedor = QPushButton('Entregadores')
        self.w6_input_cod_recolhedor = QLineEdit()
        self.w6_input_recolhedor = QLineEdit()
        self.w6_combobox_estado_festa = QComboBox()
        self.w6_button_confirmar = MyButton('Confirmar')
        self.w6_button_sair = MyButton('Sair')

        # Propriedades do Widgets
        self.w6_label_telefone_cliente.setAlignment(Qt.AlignRight)
        self.w6_label_local_evento.setAlignment(Qt.AlignRight)
        self.w6_label_qtd_pessoas.setAlignment(Qt.AlignRight)
        self.w6_label_quantidade_produto.setAlignment(Qt.AlignRight)
        self.w6_label_valor_produto.setAlignment(Qt.AlignRight)
        self.w6_label_valor_total.setAlignment(Qt.AlignRight)
        self.w6_input_cod_entregador.setPlaceholderText('Código')
        self.w6_input_cod_local_evento.setPlaceholderText('Código')
        self.w6_input_cod_produto.setPlaceholderText('Código')
        self.w6_input_cod_recolhedor.setPlaceholderText('Código')
        self.w6_input_cod_tipo_festa.setPlaceholderText('Código')
        self.w6_int_validator = QIntValidator()
        self.w6_input_cod_local_evento.setValidator(self.w6_int_validator)
        self.w6_input_celular_cliente.setEnabled(False)
        self.w6_input_cod_produto.setInputMask('99.9999')
        self.w6_input_data_evento.setInputMask('00/00/0000')
        self.w6_input_qtd_pessoas.setInputMask('0000')
        self.w6_input_qtd_alcoolicos.setInputMask('0000')
        self.w6_combobox_estado_festa.addItem('Não Confirmado')
        self.w6_combobox_estado_festa.addItem('Confirmado')
        self.w6_combobox_estado_festa.addItem('Entregue')
        self.w6_combobox_estado_festa.addItem('Recolhido')
        self.w6_textarea_obs1.setMaximumSize(400, 80)
        self.w6_textarea_obs2.setMaximumSize(400, 80)
        if n_orcamento is not None:
            festa_atual = Festa(n_orcamento)
            if festa_atual.cod_cliente != 0:
                self.w6_label_cod_cliente.setText(
                    f'Código: {festa_atual.cod_cliente}')
                self.w6_input_nome_cliente.setEnabled(False)
                self.w6_input_telefone_cliente.setEnabled(True)
            self.w6_input_nome_cliente.setText(festa_atual.nome)
            self.w6_input_telefone_cliente.setText(festa_atual.telefone)
            self.w6_input_celular_cliente.setText(festa_atual.celular)
            if festa_atual.cadastrado:
                self.w6_input_telefone_cliente.setEnabled(False)
            else:
                self.w6_input_telefone_cliente.setEnabled(True)
            self.w6_input_celular_cliente.setReadOnly(True)
            if festa_atual.data is not None:
                dia = festa_atual.data.day
                mes = festa_atual.data.month
                ano = festa_atual.data.year
                data_evento = f'{dia}/{mes}/{ano}'
            else:
                data_evento = None
            self.w6_input_data_evento.setText(data_evento)
            locais_festa = get_locais_festa()
            for local in locais_festa:
                if festa_atual.local == locais_festa[local].nome:
                    self.w6_input_cod_local_evento.setText(str(local))
            self.w6_input_local_evento.setText(festa_atual.local)
            del locais_festa
            tipos_festa = get_tipos_festa()
            for tipo in tipos_festa:
                if festa_atual.tipo == tipos_festa[tipo].nome:
                    self.w6_input_cod_tipo_festa.setText(str(tipo))
            self.w6_input_tipo_festa.setText(festa_atual.tipo)
            del tipos_festa
            self.w6_input_qtd_pessoas.setText(str(festa_atual.qtd_pessoas))
            self.w6_input_qtd_alcoolicos.setText(
                str(festa_atual.qtd_alcoolicos))
            att_janela(festa_atual, self.w6_label_valor_total)
            if festa_atual.consumo is not None:
                self.w6_input_consumo.setText(festa_atual.consumo)
            if festa_atual.avaria is not None:
                self.w6_input_avaria.setText(festa_atual.avaria)
            if festa_atual.locacao is not None:
                self.w6_input_locacao.setText(festa_atual.locacao)
            if festa_atual.entregador is not None:
                self.w6_input_entregador.setText(festa_atual.entregador)
            if festa_atual.recolhedor is not None:
                self.w6_input_recolhedor.setText(festa_atual.recolhedor)
            if festa_atual.obs1 is not None:
                self.w6_textarea_obs1.setText(festa_atual.obs1)
            if festa_atual.obs2 is not None:
                self.w6_textarea_obs2.setText(festa_atual.obs2)

        # Ações dos Widgets
        self.w6_table_produtos.tabela_produtos_festa(n_orcamento=n_orcamento)
        self.w6_button_clientes.clicked.connect(
            lambda: show_wsc(self.w6_input_nome_cliente,
                             self.w6_label_cod_cliente,
                             self.w6_input_telefone_cliente,
                             self.w6_input_celular_cliente)
        )
        self.w6_input_cod_local_evento.textChanged.connect(
            lambda: att_input(self.w6_input_cod_local_evento,
                              self.w6_input_local_evento,
                              get_locais_festa)
        )
        self.w6_button_local_evento.clicked.connect(
            lambda: show_wslf(self.w6_input_cod_local_evento)
        )
        self.w6_input_cod_tipo_festa.textChanged.connect(
            lambda: att_input(self.w6_input_cod_tipo_festa,
                              self.w6_input_tipo_festa,
                              get_tipos_festa)
        )
        self.w6_button_tipo_festa.clicked.connect(
            lambda: show_wstf(self.w6_input_cod_tipo_festa)
        )
        self.w6_input_cod_entregador.textChanged.connect(
            lambda: att_input(self.w6_input_cod_entregador,
                              self.w6_input_entregador,
                              get_entregadores)
        )
        self.w6_button_entregador.clicked.connect(
            lambda: show_wse(self.w6_input_cod_entregador)
        )
        self.w6_input_cod_recolhedor.textChanged.connect(
            lambda: att_input(self.w6_input_cod_recolhedor,
                              self.w6_input_recolhedor,
                              get_entregadores)
        )
        self.w6_button_recolhedor.clicked.connect(
            lambda: show_wse(self.w6_input_cod_recolhedor)
        )
        self.w6_input_cod_produto.textChanged.connect(
            lambda: cod_produto_typed(self.w6_input_cod_produto,
                                      self.w6_input_cod_produto,
                                      self.w6_input_nome_produto,
                                      self.w6_input_quantidade_produto,
                                      self.w6_input_valor_produto,
                                      self.w6_checkbox_consignado)
        )
        self.w6_button_cod_produto.clicked.connect(
            lambda: show_wsp(self.w6_input_cod_produto)
        )
        self.w6_button_adicionar_produto.clicked.connect(
            lambda: add_produto_into_festa(self.w6_table_produtos,
                                           n_orcamento,
                                           self.w6_input_cod_produto,
                                           self.w6_input_nome_produto,
                                           self.w6_input_quantidade_produto,
                                           self.w6_input_valor_produto)
        )
        self.w6_button_adicionar_produto.clicked.connect(
            lambda: att_janela(Festa(int(n_orcamento)),
                               self.w6_label_valor_total)
        )
        self.w6_button_remover_produto.clicked.connect(
            lambda: remove_produto(n_orcamento,
                                   self.w6_table_produtos)
        )
        self.w6_button_remover_produto.clicked.connect(
            lambda: att_janela(Festa(int(n_orcamento)),
                               self.w6_label_valor_total)
        )
        self.w6_button_confirmar.clicked.connect(
            lambda: att_festa(n_orcamento, self.w6_label_cod_cliente,
                              self.w6_input_nome_cliente,
                              self.w6_input_telefone_cliente,
                              self.w6_input_data_evento,
                              self.w6_input_local_evento,
                              self.w6_input_tipo_festa,
                              self.w6_input_qtd_pessoas,
                              self.w6_input_qtd_alcoolicos,
                              self.w6_combobox_estado_festa,
                              self.w6_input_consumo, self.w6_input_locacao,
                              self.w6_input_avaria, self.w6_input_entregador,
                              self.w6_input_recolhedor,
                              self.w6_textarea_obs1,
                              self.w6_textarea_obs2)
        )
        self.w6_button_confirmar.clicked.connect(
            lambda: table.tabela_festas_confirmadas(
                get_festas_confirmadas())
        )
        self.w6_button_confirmar.clicked.connect(
            lambda: self.close()
        )
        self.w6_button_sair.clicked.connect(
            lambda: self.close()
        )

        # Layout da janela
        self.layout.addWidget(self.w6_label_n_orcamento, 0, 0, 1, 12)
        self.layout.addWidget(self.w6_label_cod_cliente, 1, 0, 1, 1)
        self.layout.addWidget(self.w6_label_nome_cliente, 1, 1, 1, 1)
        self.layout.addWidget(self.w6_input_nome_cliente, 1, 2, 1, 2)
        self.layout.addWidget(self.w6_button_clientes, 1, 4, 1, 1)
        self.layout.addWidget(self.w6_label_telefone_cliente, 1, 5, 1, 1)
        self.layout.addWidget(self.w6_input_telefone_cliente, 1, 6, 1, 1)
        self.layout.addWidget(self.w6_label_celular_cliente, 1, 7, 1, 1)
        self.layout.addWidget(self.w6_input_celular_cliente, 1, 8, 1, 1)
        self.layout.addWidget(self.w6_label_data_evento, 2, 0, 1, 1)
        self.layout.addWidget(self.w6_input_data_evento, 2, 1, 1, 1)
        self.layout.addWidget(self.w6_label_local_evento, 2, 2, 1, 1)
        self.layout.addWidget(self.w6_input_cod_local_evento, 2, 3, 1, 1)
        self.layout.addWidget(self.w6_button_local_evento, 2, 4, 1, 1)
        self.layout.addWidget(self.w6_input_local_evento, 2, 5, 1, 8)
        self.layout.addWidget(self.w6_label_tipo_festa, 3, 0, 1, 1)
        self.layout.addWidget(self.w6_input_cod_tipo_festa, 3, 1, 1, 1)
        self.layout.addWidget(self.w6_button_tipo_festa, 3, 2, 1, 1)
        self.layout.addWidget(self.w6_input_tipo_festa, 3, 3, 1, 3)
        self.layout.addWidget(self.w6_label_qtd_pessoas, 3, 6, 1, 1)
        self.layout.addWidget(self.w6_input_qtd_pessoas, 3, 7, 1, 2)
        self.layout.addWidget(self.w6_label_qtd_alcoolicos, 3, 9, 1, 1)
        self.layout.addWidget(self.w6_input_qtd_alcoolicos, 3, 10, 1, 2)
        self.layout.addWidget(self.w6_label_obs1, 4, 0, 1, 1)
        self.layout.addWidget(self.w6_textarea_obs1, 4, 1, 1, 5)
        self.layout.addWidget(self.w6_label_obs2, 4, 6, 1, 1)
        self.layout.addWidget(self.w6_textarea_obs2, 4, 7, 1, 5)
        self.layout.addWidget(self.w6_label_quebra, 5, 0, 1, 12)
        self.layout.addWidget(self.w6_label_produtos, 6, 0, 1, 12)
        self.layout.addWidget(self.w6_label_cod_produto, 7, 0, 1, 1)
        self.layout.addWidget(self.w6_input_cod_produto, 7, 1, 1, 1)
        self.layout.addWidget(self.w6_button_cod_produto, 7, 2, 1, 1)
        self.layout.addWidget(self.w6_input_nome_produto, 7, 3, 1, 2)
        self.layout.addWidget(self.w6_label_quantidade_produto, 7, 5, 1, 1)
        self.layout.addWidget(self.w6_input_quantidade_produto, 7, 6, 1, 1)
        self.layout.addWidget(self.w6_label_valor_produto, 7, 7, 1, 1)
        self.layout.addWidget(self.w6_input_valor_produto, 7, 8, 1, 1)
        self.layout.addWidget(self.w6_checkbox_consignado, 7, 9, 1, 1)
        self.layout.addWidget(self.w6_button_adicionar_produto, 7, 10, 1, 1)
        self.layout.addWidget(self.w6_button_remover_produto, 7, 11, 1, 1)
        self.layout.addWidget(self.w6_table_produtos, 8, 0, 1, 12)
        self.layout.addWidget(self.w6_label_valor_total, 9, 0, 1, 12)
        self.layout.addWidget(self.w6_label_consumo, 10, 0, 1, 1)
        self.layout.addWidget(self.w6_input_consumo, 10, 1, 1, 1)
        self.layout.addWidget(self.w6_button_carregar_consumo, 10, 2, 1, 1)
        self.layout.addWidget(self.w6_button_consultar_consumo, 10, 3, 1, 1)
        self.layout.addWidget(self.w6_label_valor_consumo, 10, 4, 1, 1)
        self.layout.addWidget(self.w6_label_locacao, 11, 0, 1, 1)
        self.layout.addWidget(self.w6_input_locacao, 11, 1, 1, 1)
        self.layout.addWidget(self.w6_button_carregar_locacao, 11, 2, 1, 1)
        self.layout.addWidget(self.w6_button_consultar_locacao, 11, 3, 1, 1)
        self.layout.addWidget(self.w6_label_valor_locacao, 11, 4, 1, 1)
        self.layout.addWidget(self.w6_label_avaria, 12, 0, 1, 1)
        self.layout.addWidget(self.w6_input_avaria, 12, 1, 1, 1)
        self.layout.addWidget(self.w6_button_carregar_avaria, 12, 2, 1, 1)
        self.layout.addWidget(self.w6_button_consultar_avaria, 12, 3, 1, 1)
        self.layout.addWidget(self.w6_label_valor_avaria, 12, 4, 1, 1)
        self.layout.addWidget(self.w6_label_entregador, 13, 0, 1, 1)
        self.layout.addWidget(self.w6_input_cod_entregador, 13, 1, 1, 1)
        self.layout.addWidget(self.w6_button_entregador, 13, 2, 1, 1)
        self.layout.addWidget(self.w6_input_entregador, 13, 3, 1, 1)
        self.layout.addWidget(self.w6_label_recolhedor, 13, 6, 1, 1)
        self.layout.addWidget(self.w6_input_cod_recolhedor, 13, 7, 1, 1)
        self.layout.addWidget(self.w6_button_recolhedor, 13, 8, 1, 1)
        self.layout.addWidget(self.w6_input_recolhedor, 13, 9, 1, 1)
        self.layout.addWidget(self.w6_combobox_estado_festa, 14, 0, 1, 12)
        self.layout.addWidget(self.w6_button_confirmar, 15, 0, 1, 6)
        self.layout.addWidget(self.w6_button_sair, 15, 6, 1, 6)

        self.showMaximized()

    def w_search_clientes(self, input_target, label_target, input_tel,
                          input_cel):

        def att_cliente(table: MyTable):
            codigo = table.item(table.currentRow(), 0).text()
            cliente = Cliente(int(codigo))
            label_target.setText(f'Código: {cliente.codigo}')
            input_target.setText(cliente.nome)
            input_target.setEnabled(False)
            input_tel.setText(cliente.telefone)
            input_tel.setEnabled(False)
            input_cel.setText(cliente.celular)

        def att_tabela(table: MyTable, input):
            table.tabela_clientes(get_clientes(like=input.text()))

        self.wsc_label_pesquisa = QLabel('Pesquisar:')
        self.wsc_input_pesquisa = QLineEdit()
        self.wsc_table_clientes = MyTable()
        self.wsc_button_confirmar = MyButton('Confirmar')
        self.wsc_button_cancelar = MyButton('Cancelar')

        self.wsc_table_clientes.tabela_clientes(get_clientes())
        self.wsc_input_pesquisa.textChanged.connect(
            lambda: att_tabela(self.wsc_table_clientes,
                               self.wsc_input_pesquisa)
        )
        self.wsc_button_confirmar.clicked.connect(
            lambda: att_cliente(self.wsc_table_clientes)
        )
        self.wsc_button_confirmar.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.wsc_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.wsc_input_pesquisa, 0, 1, 1, 11)
        self.layout.addWidget(self.wsc_table_clientes, 1, 0, 1, 12)
        self.layout.addWidget(self.wsc_button_confirmar, 2, 0, 1, 6)
        self.layout.addWidget(self.wsc_button_cancelar, 2, 6, 1, 6)

        self.resize(800, 800)
        self.show()

    def w_search_produtos(self, input_cod):

        def choose_produto(table: MyTable, input_cod):
            codigo = table.item(table.currentRow(), 0).text()
            input_cod.setText(f'{codigo}')

        def att_janela(table: MyTable, input):
            table.tabela_produtos(get_produtos(nome=input.text()))

        self.wsp_label_pesquisa = QLabel('Pesquisar:')
        self.wsp_input_pesquisa = QLineEdit()
        self.wsp_table_produtos = MyTable()
        self.wsp_button_confirmar = MyButton('Confirmar')
        self.wsp_button_cancelar = MyButton('Cancelar')

        self.wsp_table_produtos.tabela_produtos(get_produtos())
        self.wsp_input_pesquisa.textChanged.connect(
            lambda: att_janela(self.wsp_table_produtos,
                               self.wsp_input_pesquisa)
        )
        self.wsp_button_confirmar.clicked.connect(
            lambda: choose_produto(self.wsp_table_produtos,
                                   input_cod)
        )
        self.wsp_button_confirmar.clicked.connect(
            lambda: self.close()
        )
        self.wsp_button_cancelar.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.wsp_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.wsp_input_pesquisa, 0, 1, 1, 11)
        self.layout.addWidget(self.wsp_table_produtos, 1, 0, 1, 12)
        self.layout.addWidget(self.wsp_button_confirmar, 2, 0, 1, 6)
        self.layout.addWidget(self.wsp_button_cancelar, 2, 6, 1, 6)

        self.resize(1200, 800)
        self.show()

    def w_search_locais_festa(self, input_cod):

        def choose_local(table: MyTable, input_cod):
            codigo = table.item(table.currentRow(), 0).text()
            input_cod.setText(f'{codigo}')

        self.wslf_label_pesquisa = QLabel('Pesquisar:')
        self.wslf_input_pesquisa = QLineEdit()
        self.wslf_table_locais_festa = MyTable()
        self.wslf_button_confirmar = MyButton('Confirmar')
        self.wslf_button_cancelar = MyButton('Cancelar')

        self.wslf_table_locais_festa.tabela_locais_festa(get_locais_festa())
        self.wslf_button_confirmar.clicked.connect(
            lambda: choose_local(self.wslf_table_locais_festa,
                                 input_cod)
        )
        self.wslf_button_confirmar.clicked.connect(
            lambda: self.close()
        )
        self.wslf_button_cancelar.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.wslf_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.wslf_input_pesquisa, 0, 1, 1, 11)
        self.layout.addWidget(self.wslf_table_locais_festa, 1, 0, 1, 12)
        self.layout.addWidget(self.wslf_button_confirmar, 2, 0, 1, 6)
        self.layout.addWidget(self.wslf_button_cancelar, 2, 6, 1, 6)

        self.resize(600, 400)
        self.show()

    def w_search_tipos_festa(self, input_cod):

        def choose_tipo(table: MyTable, input_cod):
            codigo = table.item(table.currentRow(), 0).text()
            input_cod.setText(f'{codigo}')

        self.wstf_label_pesquisa = QLabel('Pesquisar:')
        self.wstf_input_pesquisa = QLineEdit()
        self.wstf_table_tipos_festa = MyTable()
        self.wstf_button_confirmar = MyButton('Confirmar')
        self.wstf_button_cancelar = MyButton('Cancelar')

        self.wstf_table_tipos_festa.tabela_tipos_festa(get_tipos_festa())
        self.wstf_button_confirmar.clicked.connect(
            lambda: choose_tipo(self.wstf_table_tipos_festa,
                                input_cod)
        )
        self.wstf_button_confirmar.clicked.connect(
            lambda: self.close()
        )
        self.wstf_button_cancelar.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.wstf_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.wstf_input_pesquisa, 0, 1, 1, 11)
        self.layout.addWidget(self.wstf_table_tipos_festa, 1, 0, 1, 12)
        self.layout.addWidget(self.wstf_button_confirmar, 2, 0, 1, 6)
        self.layout.addWidget(self.wstf_button_cancelar, 2, 6, 1, 6)

        self.resize(600, 400)
        self.show()

    def w_search_entregadores(self, input_cod):

        def choose_entregador(table: MyTable, input_cod):
            codigo = table.item(table.currentRow(), 0).text()
            input_cod.setText(f'{codigo}')

        self.wse_label_pesquisa = QLabel('Pesquisar:')
        self.wse_input_pesquisa = QLineEdit()
        self.wse_table_entregadores = MyTable()
        self.wse_button_confirmar = MyButton('Confirmar')
        self.wse_button_cancelar = MyButton('Cancelar')

        self.wse_table_entregadores.tabela_entregadores(get_entregadores())
        self.wse_button_confirmar.clicked.connect(
            lambda: choose_entregador(self.wse_table_entregadores,
                                      input_cod)
        )
        self.wse_button_confirmar.clicked.connect(
            lambda: self.close()
        )
        self.wse_button_cancelar.clicked.connect(
            lambda: self.close()
        )

        self.layout.addWidget(self.wse_label_pesquisa, 0, 0, 1, 1)
        self.layout.addWidget(self.wse_input_pesquisa, 0, 1, 1, 11)
        self.layout.addWidget(self.wse_table_entregadores, 1, 0, 1, 12)
        self.layout.addWidget(self.wse_button_confirmar, 2, 0, 1, 6)
        self.layout.addWidget(self.wse_button_cancelar, 2, 6, 1, 6)

        self.resize(600, 400)
        self.show()


if __name__ == "__main__":
    app = QApplication()

    # setando o estilo
    with open("estilo.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MyWindow('Inicio', usuario='1')
    window.w2_menu_principal()
    sys.exit(app.exec())
