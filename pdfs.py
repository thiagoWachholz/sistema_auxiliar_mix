from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

from objects import Festa, Produto


def get_data(data):
    dia = data.day
    mes = data.month
    ano = data.year
    return f'{dia}/{mes}/{ano}'


def get_print_festa_cliente(n_festa, entrada=False):

    festa = Festa(n_festa)

    nome_arquivo = f"Festa {n_festa}.pdf"

    doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
    styles = getSampleStyleSheet()

    conteudo = []

    titulo = Paragraph(
        'Orçamento para festa - Mix Bebidas', styles['Title']
    )
    logo = Image('images/logo.png', height=100, width=100)

    dados_tabela_dados_cliente = [
        [
            Paragraph(f'<b>Nome:</b> {festa.nome}', style=styles['BodyText']),
            Paragraph(
                f'<b>Telefone:</b> {festa.telefone}',
                style=styles['BodyText']),
            Paragraph(
                f'<b>Celular:</b> {festa.celular}', style=styles['BodyText'])
        ],
        [
            Paragraph(f'<b>Data:</b> {get_data(festa.data)}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Local:</b> {festa.local}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Tipo:</b> {festa.tipo}', style=styles['BodyText'])
        ],
        [
            f'{festa.qtd_pessoas} Pessoas',
            f'{festa.qtd_alcoolicos} Bebem Bebida Alcoólica'
        ],
    ]
    tabela_dados_cliente = Table(dados_tabela_dados_cliente)
    estilo_tabela_dados = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ])
    tabela_dados_cliente.setStyle(estilo_tabela_dados)

    dados_tabela_obs = [
        ['Observação 1:', f'{festa.obs1}'],
        ['Observação 2:', f'{festa.obs2}'],
    ]
    tabela_obs = Table(dados_tabela_obs)

    titulo_produtos = Paragraph(
        'Produtos', styles['Title']
    )

    dados_tabela_produtos = [
        ['Imagem', 'Descrição', 'Referência', 'Quantidade', 'Valor', 'Total']
    ]
    valor_total = 0
    for produto in festa.produtos:
        print(festa.produtos[produto])
        item = Produto(produto)
        item.get_product_data()
        imagem = Image(item.image, width=45, height=45)
        qtd = int(festa.produtos[produto][3])
        total_produto = festa.produtos[produto][4] * festa.produtos[produto][3]
        total_produto = float(total_produto)
        valor_total += total_produto
        total_produto = (f'{total_produto:.2f}').replace('.', ',')
        valor = (f'{festa.produtos[produto][4]:.2f}').replace('.', ',')
        data_to_add = [imagem, festa.produtos[produto][1],
                       festa.produtos[produto][2],
                       qtd,
                       valor,
                       total_produto]

        dados_tabela_produtos.append(data_to_add)
    tabela_produtos = Table(dados_tabela_produtos)
    tabela_produtos.setStyle(estilo_tabela_dados)

    def arredondar_numero_divisivel(n1, nd):
        numero = round(n1/nd)*nd
        return numero

    valor_entrada = arredondar_numero_divisivel(valor_total*0.6, 10)
    valor_entrada = (f'{valor_entrada:.2f}').replace('.', ',')
    valor_total = (f'{valor_total:.2f}').replace('.', ',')

    dados_tabela_valores = [
        [Paragraph(
            f'<b>Valor total:</b> R${valor_total}', style=styles['BodyText'])]
    ]
    if entrada:
        dados_tabela_valores[0].append(
            Paragraph(
                text=f'<b>Valor Entrada:</b> R${valor_entrada}',  # type:ignore
                style=styles['BodyText']))
    tabela_valores = Table(dados_tabela_valores)
    tabela_valores.hAlign = 0

    dados_tabela_pagamento = [
        ['Valor pago:'],
        ['R$'+'_'*75],
        ['Assinatura Recebedor:'],
        ['_'*75]
    ]
    tabela_pagamento = Table(dados_tabela_pagamento)
    tabela_pagamento.hAlign = 0

    dados_tabela_info = [
        ['Mix Bebidas', 'CNPJ: 31.847.694/0001-20'],
        ['Rua Cap. Adolfo Castro, 527 | Vila Nova | Camaquã',
         'CEP: 96783-000'],
        ['Fone Whats: (51) 99706-3311', 'Plantão: (00) 00000-0000'],
        ['E-mail: thiagomixbebidas@gmail.com', '']
    ]
    tabela_info = Table(dados_tabela_info)

    titulo_termos = Paragraph('Informe de Prestação de Serviços',
                              style=styles['Heading3'])
    termo_1 = Paragraph('''
        1. O Contratante pode optar pelo modelo de fornecimento de bebidas em
consignação.
    ''', style=styles['BodyText'])
    termo_1_1 = Paragraph("""
        1.1 Neste modelo de proposta o contratante deve pagar uma entrada de
60% do valor do orçamento de bebidas para o evento, previamente
apresentado.
    """, style=styles['BodyText'])
    termo_1_2 = Paragraph("""
        1.2 Após o evento, será feito o recolhimento das bebidas não
consumidas, e a diferença do valor em bebidas consumidas e valor de entrada
deverá ser pago em até 7 dias caso o valor em bebidas consumidas seja
superior ao valor dado de entrada, caso o valor em bebidas consumidas seja
inferior ao valor dado de entrada, a diferença será convertida em crédito para
o
cliente retirar em produtos da loja.
    """, style=styles['BodyText'])
    termo_1_3 = Paragraph("""
        1.3 Casos especiais
    """, style=styles['BodyText'])
    termo_1_3_1 = Paragraph("""
        1.3.1 O gelo pode ser aceito no recolhimento, porém, se no
momento do recolhimento, julgarmos que ele não está em condições de
ser comercializado, não será aceito e será cobrado no valor do
consumo.
    """, style=styles['BodyText'])
    termo_1_3_2 = Paragraph("""
        1.3.2 Bebidas congeladas não são aceitas no recolhimento.
    """, style=styles['BodyText'])
    termo_1_4 = Paragraph("""
        1.4 Plantão
    """, style=styles['BodyText'])
    termo_1_4_1 = Paragraph("""
        1.4.1 O cliente que optar pelo fornecimento de bebidas em
modelo consignado, poderá contar com plantão durante a festa, caso
necessário, ele poderá ligar para o número de telefone do plantão e
solicitar quaisquer que forem os itens que deseja, e desde que os itens
estiverem disponíveis na loja, lhe será entregue, o plantão atenderá
somente na zona urbana de Camaquã.

    """, style=styles['BodyText'])
    termo_1_4_2 = Paragraph("""
        1.4.2 Caso sejam solicitados itens no plantão durante a festa, e no
recolhimento, todos os itens referentes à determinada entrega do
plantão não forem consumidos, uma taxa adicional de R$50,00 será
cobrada.
    """, style=styles['BodyText'])
    termo_2 = Paragraph("""
        2. Fornecimento de bebidas
    """, style=styles['BodyText'])
    termo_2_1 = Paragraph("""
        2.1 Orçamentos de bebidas devem ser confirmados pelo cliente.
    """, style=styles['BodyText'])
    termo_2_2 = Paragraph("""
        2.2 Entregas que precisem ser realizadas em domingos ou feriados, ou
que por decisão/condição do cliente, a entrega tenha que ser feita fora do
horário de atendimento da loja (Entre 18:00 (aos sábados às 16:00) e 23:59, ou
00:00 e 08:00) terão taxa adicional de R$50,00.
    """, style=styles['BodyText'])
    termo_2_3 = Paragraph("""
        2.3 Há a possibilidade da falta de disponibilidade de itens previstos
no
orçamento para a data do evento, por possíveis motivos como falta na fábrica,
fornecedor sem estoque, entre outros. Nesses casos, o item faltante deverá ser
removido do orçamento ou substituído.
    """, style=styles['BodyText'])
    termo_2_4 = Paragraph("""
        2.4 Entregas que precisem ser feitas em localidades fora da zona urbana
de Camaquã, terão um custo adicional de R$4,00/Km.
    """, style=styles['BodyText'])
    termo_3 = Paragraph("""
        3. Locação.
    """, style=styles['BodyText'])
    termo_3_1 = Paragraph("""
        3.1 Itens locados são de responsabilidade do cliente, ele se
responsabiliza por garantir o seu retorno da forma como foram entregues, o
ideal é que sejam conferidos no momento da retirada/entrega, reclamações
posteriores podem não ser aceitas.
    """, style=styles['BodyText'])
    termo_3_2 = Paragraph("""
        3.2 Qualquer avaria a um item, sofrida durante o momento em que o
item se encontra locado, é de responsabilidade do cliente, e um valor adicional
poderá ser cobrado.
    """, style=styles['BodyText'])
    termo_3_3 = Paragraph("""
        3.3 Casos especiais.
    """, style=styles['BodyText'])
    termo_3_3_1 = Paragraph("""
        3.3.1 Pratos e talheres devem ser entregues limpos ao devolvêlos à
loja,
caso contrário poderá ser cobrado taxa adicional de limpeza proporcional à
quantidade de itens locados.
    """, style=styles['BodyText'])
    termo_3_3_1_1 = Paragraph("""
        3.3.1.1 Valor de limpeza do prato: R$0,50.
    """, style=styles['BodyText'])
    termo_3_3_1_2 = Paragraph("""
        3.3.1.2 Valor de limpeza do garfo: R$0,25.
    """, style=styles['BodyText'])
    termo_3_3_1_3 = Paragraph("""
        3.3.1.3 Valor de limpeza da faca: R$0,25.
    """, style=styles['BodyText'])
    termo_3_3_2 = Paragraph("""
        3.3.2 Em orçamentos com bebidas, poderão ser locados sem
custo, uma quantidade de copos/taças relacionada com a quantidade de
bebidas da festa, e somente de um tipo de copo/taça, qualquer
quantidade sobressalente, terá seu valor de locação mantido.
    """, style=styles['BodyText'])

    espaco = Spacer(1, 12)

    conteudo.append(logo)
    conteudo.append(titulo)
    conteudo.append(tabela_dados_cliente)
    conteudo.append(espaco)
    conteudo.append(tabela_obs)
    conteudo.append(espaco)
    conteudo.append(titulo_produtos)
    conteudo.append(tabela_produtos)
    conteudo.append(espaco)
    conteudo.append(tabela_valores)
    conteudo.append(espaco)
    conteudo.append(tabela_pagamento)
    conteudo.append(espaco)
    conteudo.append(tabela_info)
    conteudo.append(espaco)
    conteudo.append(titulo_termos)
    conteudo.append(termo_1)
    conteudo.append(termo_1_1)
    conteudo.append(termo_1_2)
    conteudo.append(termo_1_3)
    conteudo.append(termo_1_3_1)
    conteudo.append(termo_1_3_2)
    conteudo.append(termo_1_4)
    conteudo.append(termo_1_4_1)
    conteudo.append(termo_1_4_2)
    conteudo.append(termo_2)
    conteudo.append(termo_2_1)
    conteudo.append(termo_2_2)
    conteudo.append(termo_2_3)
    conteudo.append(termo_2_4)
    conteudo.append(termo_3)
    conteudo.append(termo_3_1)
    conteudo.append(termo_3_2)
    conteudo.append(termo_3_3)
    conteudo.append(termo_3_3_1)
    conteudo.append(termo_3_3_1_1)
    conteudo.append(termo_3_3_1_2)
    conteudo.append(termo_3_3_1_3)
    conteudo.append(termo_3_3_2)

    doc.build(conteudo)

    return nome_arquivo


def get_print_festa_entregador(n_festa):

    festa = Festa(n_festa)

    nome_arquivo = f"Festa {n_festa} Entregador.pdf"

    doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
    styles = getSampleStyleSheet()

    titulo = Paragraph(
        'Pedido para festa - Mix Bebidas', styles['Heading2']
    )

    conteudo = []

    dados_tabela_dados_cliente = [
        [
            Paragraph(f'<b>Nome:</b> {festa.nome}', style=styles['BodyText']),
            Paragraph(
                f'<b>Telefone:</b> {festa.telefone}',
                style=styles['BodyText']),
            Paragraph(
                f'<b>Celular:</b> {festa.celular}', style=styles['BodyText'])
        ],
        [
            Paragraph(f'<b>Data:</b> {get_data(festa.data)}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Local:</b> {festa.local}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Tipo:</b> {festa.tipo}', style=styles['BodyText'])
        ],
        [
            f'{festa.qtd_pessoas} Pessoas',
            f'{festa.qtd_alcoolicos} Bebem Bebida Alcoólica'
        ],
    ]
    tabela_dados_cliente = Table(dados_tabela_dados_cliente)
    tabela_dados_cliente.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))

    dados_tabela_obs = [
        ['Observação 1:', f'{festa.obs1}'],
        ['Observação 2:', f'{festa.obs2}'],
    ]
    tabela_obs = Table(dados_tabela_obs)
    tabela_obs.hAlign = 'LEFT'

    titulo_produtos = Paragraph('Produtos', style=styles['Heading2'])

    dados_tabela_produtos = [
        ['Código', 'Descrição', 'Referência', 'Quantidade', 'Valor', 'Total']
    ]
    valor_total = 0
    for produto in festa.produtos:
        item = Produto(produto)
        item.get_product_data()
        qtd = int(festa.produtos[produto][3])
        total_produto = festa.produtos[produto][4] * festa.produtos[produto][3]
        total_produto = float(total_produto)
        valor_total += total_produto
        total_produto = (f'{total_produto:.2f}').replace('.', ',')
        valor = (f'{festa.produtos[produto][4]:.2f}').replace('.', ',')
        data_to_add = [item.codigo, festa.produtos[produto][1],
                       festa.produtos[produto][2],
                       qtd,
                       valor,
                       total_produto]

        dados_tabela_produtos.append(data_to_add)
    tabela_produtos = Table(dados_tabela_produtos)
    tabela_produtos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))

    obs_paragraph = Paragraph('Observações', style=styles['BodyText'])

    dados_tabela_valores = [
        [Paragraph(
            (f'<b>Valor total:</b> R${valor_total:.2f}').replace('.', ','),
            style=styles['BodyText']),
            Paragraph('<b>Valor pago:</b> R$_____________',
                      style=styles['BodyText'])]
    ]
    tabela_valores = Table(dados_tabela_valores)
    tabela_valores.hAlign = 0

    espaco = Spacer(1, 12)
    espaco_obs = Spacer(1, 60)

    dados_tabela_entregadores = [
        [Paragraph('<b>Entregou</b>', style=styles['BodyText']),
         Paragraph('<b>Recolheu</b>', style=styles['BodyText']),],
        ['', '']
    ]
    tabela_entregadores = Table(dados_tabela_entregadores)
    tabela_entregadores.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))
    tabela_entregadores.hAlign = 'LEFT'

    conteudo.append(titulo)
    conteudo.append(tabela_dados_cliente)
    conteudo.append(tabela_obs)
    conteudo.append(titulo_produtos)
    conteudo.append(tabela_produtos)
    conteudo.append(obs_paragraph)
    conteudo.append(espaco_obs)
    conteudo.append(tabela_valores)
    conteudo.append(espaco)
    conteudo.append(tabela_entregadores)

    doc.build(conteudo)

    return nome_arquivo


def get_print_consumo(n_festa, valor_pago=0):

    festa = Festa(n_festa)

    nome_arquivo = f"Festa {n_festa} Consumo.pdf"

    doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
    styles = getSampleStyleSheet()

    titulo = Paragraph(
        'Relatório de Consumo - Mix Bebidas', styles['Heading2']
    )

    conteudo = []

    dados_tabela_dados_cliente = [
        [
            Paragraph(f'<b>Nome:</b> {festa.nome}', style=styles['BodyText']),
            Paragraph(
                f'<b>Telefone:</b> {festa.telefone}',
                style=styles['BodyText']),
            Paragraph(
                f'<b>Celular:</b> {festa.celular}', style=styles['BodyText'])
        ],
        [
            Paragraph(f'<b>Data:</b> {get_data(festa.data)}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Local:</b> {festa.local}',
                      style=styles['BodyText']),
            Paragraph(f'<b>Tipo:</b> {festa.tipo}', style=styles['BodyText'])
        ],
        [
            f'{festa.qtd_pessoas} Pessoas',
            f'{festa.qtd_alcoolicos} Bebem Bebida Alcoólica'
        ],
    ]
    tabela_dados_cliente = Table(dados_tabela_dados_cliente)
    tabela_dados_cliente.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))

    titulo_bebidas = Paragraph('Bebidas Consumidas', style=styles['Heading2'])

    dados_tabela_consumo = [
        ['Descrição', 'Referência', 'Quantidade', 'Valor', 'Total']
    ]
    valor_consumo = 0
    for produto in festa.consumo:
        item = Produto(produto)
        item.get_product_data()
        qtd = int(festa.consumo[produto][3])
        total_produto = festa.consumo[produto][4] * festa.consumo[produto][3]
        total_produto = float(total_produto)
        valor_consumo += total_produto
        total_produto = (f'{total_produto:.2f}').replace('.', ',')
        valor = (f'{festa.consumo[produto][4]:.2f}').replace('.', ',')
        data_to_add = [festa.consumo[produto][1],
                       festa.consumo[produto][2],
                       qtd,
                       valor,
                       total_produto]

        dados_tabela_consumo.append(data_to_add)
    tabela_consumo = Table(dados_tabela_consumo)
    tabela_consumo.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))
    tabela_consumo.hAlign = 'LEFT'

    titulo_locacao = Paragraph('Itens Locados', style=styles['Heading2'])

    dados_tabela_locacao = [
        ['Descrição', 'Referência', 'Quantidade', 'Valor', 'Total']
    ]
    valor_locacao = 0
    for produto in festa.locacao:
        item = Produto(produto)
        item.get_product_data()
        qtd = int(festa.locacao[produto][3])
        total_produto = festa.locacao[produto][4] * festa.locacao[produto][3]
        total_produto = float(total_produto)
        valor_locacao += total_produto
        total_produto = (f'{total_produto:.2f}').replace('.', ',')
        valor = (f'{festa.locacao[produto][4]:.2f}').replace('.', ',')
        data_to_add = [festa.locacao[produto][1],
                       festa.locacao[produto][2],
                       qtd,
                       valor,
                       total_produto]

        dados_tabela_locacao.append(data_to_add)
    tabela_locacao = Table(dados_tabela_locacao)
    tabela_locacao.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))
    tabela_locacao.hAlign = 'LEFT'

    titulo_avaria = Paragraph('Itens Avariados', style=styles['Heading2'])

    dados_tabela_avaria = [
        ['Descrição', 'Referência', 'Quantidade', 'Valor', 'Total']
    ]
    valor_avaria = 0
    for produto in festa.avaria:
        item = Produto(produto)
        item.get_product_data()
        qtd = int(festa.avaria[produto][3])
        total_produto = festa.avaria[produto][4] * festa.avaria[produto][3]
        total_produto = float(total_produto)
        valor_avaria += total_produto
        total_produto = (f'{total_produto:.2f}').replace('.', ',')
        valor = (f'{festa.avaria[produto][4]:.2f}').replace('.', ',')
        data_to_add = [festa.avaria[produto][1],
                       festa.avaria[produto][2],
                       qtd,
                       valor,
                       total_produto]

        dados_tabela_avaria.append(data_to_add)
    tabela_avaria = Table(dados_tabela_avaria)
    tabela_avaria.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))
    tabela_avaria.hAlign = 'LEFT'

    total_festa = valor_consumo+valor_locacao+valor_avaria
    p_total_festa = Paragraph(
        (f'<b>Valor total:</b> R${total_festa:.2f}').replace('.', ','),
        style=styles['BodyText'])
    p_pago = Paragraph(
        (f'<b>Valor pago:</b> R${valor_pago:.2f}').replace('.', ','),
        style=styles['BodyText'])
    p_restante = Paragraph(
        (f'<b>Valor restante:</b> R${total_festa-valor_pago:.2f}').replace('.', ','),
        style=styles['BodyText'])

    tabela_valores = Table(
        [[p_total_festa, p_pago, p_restante]]
    )

    espaco = Spacer(1, 12)

    conteudo.append(titulo)
    conteudo.append(tabela_dados_cliente)
    conteudo.append(espaco)
    conteudo.append(tabela_valores)
    conteudo.append(espaco)
    if len(festa.consumo) > 0:
        conteudo.append(titulo_bebidas)
        conteudo.append(tabela_consumo)
    if len(festa.locacao) > 0:
        conteudo.append(titulo_locacao)
        conteudo.append(tabela_locacao)
    if len(festa.avaria) > 0:
        conteudo.append(titulo_avaria)
        conteudo.append(tabela_avaria)

    doc.build(conteudo)

    return nome_arquivo


if __name__ == "__main__":
    get_print_festa_cliente(10711, entrada=True)
    get_print_festa_entregador(10711)
    get_print_consumo(10711)
