# type:ignore
import sqlite3
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QKeyEvent, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                               QGridLayout, QLabel, QLineEdit, QMainWindow,
                               QMenu, QMenuBar, QMessageBox, QPushButton,
                               QTableWidget, QTableWidgetItem, QWidget)

from database_connection import conn_tw, cur_tw
from objects import (Categoria, Entregador, Usuario, caminho_images,
                     get_categorias, get_entregadores, get_produtos,
                     get_usuarios)


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
        self.w5_combobox_filtro_estado.addItem('Confirmado')
        self.w5_combobox_filtro_estado.addItem('Entregue')
        self.w5_combobox_filtro_estado.addItem('Recolhido')

        # Ações dos Widgets
        self.w5_acao_entregadores.triggered.connect(
            lambda: show_w5_entregadores())

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


if __name__ == "__main__":
    app = QApplication()

    # setando o estilo
    with open("estilo.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MyWindow('Inicio', usuario='1')
    window.w2_menu_principal()
    sys.exit(app.exec())
