import mysql.connector
from datetime import datetime
import flet as ft

# Conectar ao banco de dados
def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="060601",
            database="mydb"
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

# Gerenciamento de Usuários
def adicionar_usuario(nome, email, senha, tipo, cpf=None, data_nascimento=None, cnpj=None):
    conexao = conectar()
    if not conexao:
        return
    cursor = conexao.cursor()
    
    sql = "INSERT INTO Usuario (Nome, Email, Senha, Tipo) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome, email, senha, tipo))
    conexao.commit()
    usuario_id = cursor.lastrowid
    
    if tipo == "Jogador" and data_nascimento:
        data_nascimento = datetime.strptime(data_nascimento, "%d%m%Y").strftime("%Y-%m-%d")
        sql_jogador = "INSERT INTO Jogador (Usuario_id_Usuario, CPF, Saldo_Carteira, Data_Nascimento) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_jogador, (usuario_id, cpf, 100.00, data_nascimento))
    elif tipo == "Empresa" and cnpj:
        sql_empresa = "INSERT INTO Empresa (Usuario_id_Usuario, CNPJ) VALUES (%s, %s)"
        cursor.execute(sql_empresa, (usuario_id, cnpj))
    
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_usuarios():
    conexao = conectar()
    if not conexao:
        return []
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios

def remover_usuario(id_usuario):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id_Usuario = %s", (id_usuario,))
        conexao.commit()
        cursor.close()
        conexao.close()

# Gerenciamento de Jogos
def adicionar_jogo(titulo, descricao, gratuito, requisitos, preco, data_lancamento, id_empresa):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO Jogo (Titulo, Descricao, Gratuito, Requisitos, Preco, Data_Lancamento, Empresa_Usuario_id_Usuario) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (titulo, descricao, gratuito, requisitos, preco, data_lancamento, id_empresa)
        )
        conexao.commit()

        # Obtém o ID do jogo inserido
        jogo_id = cursor.lastrowid  # Pega o ID gerado automaticamente
        cursor.close()
        conexao.close()
        return jogo_id  # Retorna o ID do jogo inserido
    return None



def listar_jogos():
    conexao = conectar()
    if not conexao:
        return []
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT idJogo, titulo, descricao, preco, requisitos, Data_Lancamento, gratuito, Empresa_Usuario_id_Usuario
        FROM Jogo
    """)
    jogos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jogos

def avaliar_jogo(id_jogo, id_jogador, nota, comentario):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = "INSERT INTO Avaliacao (Jogo_id_Jogo, Jogador_id_Jogador, Nota, Comentario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_jogo, id_jogador, nota, comentario))
        conexao.commit()
        cursor.close()
        conexao.close()

# Compra e Biblioteca
def adicionar_biblioteca_jogo(page: ft.Page, id_jogo, usuario_id):
    conexao = conectar()
    if not conexao:
        return
    cursor = conexao.cursor()
    
    cursor.execute("SELECT Saldo_Carteira FROM Jogador WHERE Usuario_id_Usuario = %s", (usuario_id,))
    saldo_jogador = cursor.fetchone()[0]
    cursor.execute("SELECT Preco FROM Jogo WHERE id_Jogo = %s", (id_jogo,))
    preco_jogo = cursor.fetchone()[0]
    
    if saldo_jogador < preco_jogo:
        page.add(ft.Text("Saldo insuficiente para comprar este jogo.", color="red"))
    else:
        cursor.execute("SELECT * FROM Biblioteca WHERE Jogo_id_Jogo = %s AND Jogador_id_Jogador = %s", (id_jogo, usuario_id))
        if cursor.fetchone():
            page.add(ft.Text("Você já possui este jogo."))
        else:
            cursor.execute("UPDATE Jogador SET Saldo_Carteira = %s WHERE Usuario_id_Usuario = %s", (saldo_jogador - preco_jogo, usuario_id))
            cursor.execute("INSERT INTO Biblioteca (Jogo_id_Jogo, Jogador_id_Jogador, Data_Aquisicao) VALUES (%s, %s, NOW())", (id_jogo, usuario_id))
            conexao.commit()
            page.add(ft.Text("Jogo comprado e adicionado à biblioteca com sucesso!"))
    
    page.update()
    cursor.close()
    conexao.close()











                                                                        ### Interface Gráfica ###



def tela_inicial(page: ft.Page):
    page.title = "Mew Games"
    page.bgcolor = "#F5F5F5"  # Fundo claro e suave

    # Título estilizado
    title = ft.Text(
        "Mew Games",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#673AB7",  # Roxo vibrante
    )

    # Função para criar botões personalizados
    def custom_button(text, on_click, color):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=color,
            color="white",
            width=220,
            height=55,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                shadow_color=ft.colors.BLACK12,  # Sombra leve para destaque
            ),
        )

    cadastro_button = custom_button("Criar Conta", lambda e: navegar_para_cadastro(page), "#673AB7")  # Roxo
    login_button = custom_button("Entrar", lambda e: navegar_para_login(page), "#009688")  # Verde água

    # Layout principal
    layout = ft.Container(
        content=ft.Column(
            [
                title,
                cadastro_button,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

    page.add(layout)


# Função para a tela de login
def tela_login(page: ft.Page):
    page.title = "Entrar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    email_input = ft.TextField(label="Email", autofocus=True)
    senha_input = ft.TextField(label="Senha", password=True)
    status_text = ft.Text("", color="green")

    def on_entrar_click(e):
        email = email_input.value
        senha = senha_input.value
        usuarios = listar_usuarios()  # Função para listar os usuários cadastrados

        for usuario in usuarios:
            if usuario[2] == email and senha == usuario[3]:
                status_text.value = "✅ Login realizado com sucesso!"
                status_text.color = "green"
                page.update()
                tipo_usuario = usuario[5]
                print(f"Usuário {usuario[1]} logado com sucesso! Tipo: {tipo_usuario}")
                navegar_para_gerenciamento(page, usuario[0], tipo_usuario)
                return

        status_text.value = "⚠️ Email ou senha incorretos!"
        status_text.color = "red"
        page.update()

    entrar_button = ft.ElevatedButton("Entrar", on_click=on_entrar_click)
    voltar_button = ft.ElevatedButton("Voltar", on_click=lambda e: navegar_para_home(page))

    page.add(
        ft.Text("Entrar", size=24, weight="bold"),
        email_input,
        senha_input,
        entrar_button,
        status_text,
        voltar_button
    )


# Função para a tela de cadastro de usuário
def tela_cadastro(page: ft.Page):
    page.title = "Cadastro de Usuário"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    nome_input = ft.TextField(label="Nome", autofocus=True)
    email_input = ft.TextField(label="Email")
    senha_input = ft.TextField(label="Senha", password=True)
    tipo_input = ft.Dropdown(
        label="Tipo de Usuário",
        options=[ft.dropdown.Option("Jogador"), ft.dropdown.Option("Empresa")],
        value="Jogador"
    )
    
    cpf_input = ft.TextField(label="CPF", visible=False)
    data_nascimento_input = ft.TextField(label="Data de Nascimento", visible=False)
    cnpj_input = ft.TextField(label="CNPJ", visible=False)

    status_text = ft.Text("", color="green")

    def on_tipo_change(e):
        if tipo_input.value == "Jogador":
            cpf_input.visible = True
            data_nascimento_input.visible = True
            cnpj_input.visible = False
        elif tipo_input.value == "Empresa":
            cnpj_input.visible = True
            cpf_input.visible = False
            data_nascimento_input.visible = False
        page.update()

    tipo_input.on_change = on_tipo_change

    def on_adicionar_click(e):
        nome = nome_input.value
        email = email_input.value
        senha = senha_input.value
        tipo = tipo_input.value
        
        if tipo == "Jogador":
            cpf = cpf_input.value
            data_nascimento = data_nascimento_input.value
            adicionar_usuario(nome, email, senha, tipo, cpf=cpf, data_nascimento=data_nascimento)
            status_text.value = "✅ Jogador adicionado com sucesso!"
        elif tipo == "Empresa":
            cnpj = cnpj_input.value
            adicionar_usuario(nome, email, senha, tipo, cnpj=cnpj)
            status_text.value = "✅ Empresa adicionada com sucesso!"
        
        status_text.color = "green"
        page.update()

    voltar_button = ft.ElevatedButton("Voltar", on_click=lambda e: navegar_para_home(page))
    adicionar_button = ft.ElevatedButton("Adicionar Usuário", on_click=on_adicionar_click)

    page.add(
        ft.Text("Cadastro de Usuário", size=24, weight="bold"),
        nome_input,
        email_input,
        senha_input,
        tipo_input,
        cpf_input,
        data_nascimento_input,
        cnpj_input,
        adicionar_button,
        status_text,
        voltar_button
    )


# Função para a tela de gerenciamento de jogos
import flet as ft

def tela_adicionar_jogo(page: ft.Page, usuario_id):
    # Verifica se o usuário é uma empresa
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT Tipo FROM Usuario WHERE id_Usuario = %s", (usuario_id,))
        tipo_usuario = cursor.fetchone()
        cursor.execute("SELECT id_Genero, Nome FROM Genero")  # Busca gêneros do banco
        generos = cursor.fetchall()
        cursor.close()
        conexao.close()

        if tipo_usuario is None or tipo_usuario[0] != "Empresa":
            page.add(ft.Text("Você não tem permissão para adicionar jogos. Apenas empresas podem fazer isso.", color="red"))
            page.update()
            return

    # Interface de adicionar jogo para empresas
    page.clean()
    titulo = ft.Text("Adicionar Jogo", size=30)
    descricao = ft.Text("Informe os dados do jogo para adicionar.", size=20)

    campo_titulo = ft.TextField(label="Título do Jogo", autofocus=True)
    campo_descricao = ft.TextField(label="Descrição")
    campo_preco = ft.TextField(label="Preço", keyboard_type=ft.KeyboardType.NUMBER)
    campo_requisitos = ft.TextField(label="Requisitos do Jogo")
    campo_data_lancamento = ft.TextField(label="Data de Lançamento (DD/MM/YYYY)")
    campo_gratuito = ft.Checkbox(label="Gratuito")

    # Criar checkboxes para gêneros
    checkboxes_genero = []
    for genero in generos:
        checkbox = ft.Checkbox(label=genero[1], value=False)
        checkboxes_genero.append(checkbox)

    def salvar_jogo(e):
        titulo_jogo = campo_titulo.value
        descricao_jogo = campo_descricao.value
        try:
            preco_jogo = float(campo_preco.value.replace(',', '.'))
        except ValueError:
            page.add(ft.Text("Preço inválido! Insira um valor numérico válido.", color="red"))
            page.update()
            return
        requisitos_jogo = campo_requisitos.value
        data_lancamento = campo_data_lancamento.value
        gratuito = campo_gratuito.value
        id_empresa = usuario_id  # O ID da empresa será o ID do usuário logado (empresa)

        # Convertendo a data de lançamento para o formato adequado
        try:
            data_lancamento = datetime.strptime(data_lancamento, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            page.add(ft.Text("Data inválida! Use o formato DD/MM/YYYY.", color="red"))
            page.update()
            return

        # Obtém os gêneros selecionados
        generos_selecionados = [genero[0] for genero, checkbox in zip(generos, checkboxes_genero) if checkbox.value]

        if not generos_selecionados:
            page.add(ft.Text("Selecione pelo menos um gênero!", color="red"))
            page.update()
            return

        # Adiciona o jogo no banco de dados
        jogo_id = adicionar_jogo(titulo_jogo, descricao_jogo, gratuito, requisitos_jogo, preco_jogo, data_lancamento, id_empresa)


        # Adiciona os gêneros do jogo na tabela relacional
        for genero_id in generos_selecionados:
            adicionar_genero_jogo(jogo_id, genero_id)

        page.add(ft.Text("Jogo adicionado com sucesso!"))
        page.update()

    botao_salvar = ft.ElevatedButton("Salvar Jogo", on_click=salvar_jogo)
    botao_voltar = ft.ElevatedButton("Sair", on_click=lambda e: navegar_para_login(page))

    # Adiciona os componentes na página
    conteudo = ft.Column(
        controls=[
            titulo, descricao, campo_titulo, campo_descricao, campo_preco,
            campo_requisitos, campo_data_lancamento, campo_gratuito,
            ft.Text("Selecione os gêneros do jogo:"),
            *checkboxes_genero,
            botao_salvar, botao_voltar
        ]
    )

    # Usando ListView para rolagem
    conteudo_scroll = ft.ListView(
        width=500,
        height=600,  # Defina a altura conforme necessário
        controls=[
            titulo, descricao, campo_titulo, campo_descricao, campo_preco,
            campo_requisitos, campo_data_lancamento, campo_gratuito,
            ft.Text("Selecione os gêneros do jogo:"),
            *checkboxes_genero,
            botao_salvar, botao_voltar
        ]
    )

    page.add(conteudo_scroll)
    page.update()


# Função para adicionar um gênero a um jogo   
def adicionar_genero_jogo(jogo_id, genero_id):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO jogo_genero (Jogo_idJogo, Genero_id_Genero) VALUES (%s, %s)",
            (jogo_id, genero_id)
        )
        conexao.commit()
        cursor.close()
        conexao.close()






def tela_loja(page: ft.Page, usuario_id):
    """Verifica se o usuário é um jogador antes de acessar a loja."""
    conexao = conectar()
    
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT Tipo FROM Usuario WHERE id_Usuario = %s", (usuario_id,))
        tipo_usuario = cursor.fetchone()
        cursor.close()
        conexao.close()

        if tipo_usuario and tipo_usuario[0] != "Jogador":
            page.clean()
            page.add(ft.Text("Você não tem permissão para comprar jogos. Apenas jogadores podem acessar a loja.", color="red"))
            botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: navegar_para_gerenciamento(page, usuario_id, "Empresa"))
            page.add(botao_voltar)
            page.update()
            return

    # Se o usuário for jogador, exibe a loja
    tela_loja_jogos(page, usuario_id)

def tela_loja_jogos(page: ft.Page, usuario_id):
    """Exibe os jogos disponíveis para compra na loja com filtro por gênero."""
    jogos_disponiveis = listar_jogos()
    saldo = obter_saldo(usuario_id)  # Buscar saldo do jogador

    page.clean()

    titulo = ft.Text("Loja de Jogos", size=30, weight=ft.FontWeight.BOLD)
    descricao = ft.Text("Escolha um jogo para comprar e adicionar à sua biblioteca.", size=20)

    # Exibir saldo do jogador
    saldo_texto = ft.Text(f"Saldo: R$ {saldo:.2f}", size=18, color="blue")

    # Obter lista de gêneros disponíveis
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_Genero, nome FROM genero")
    generos = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Adicionar o dropdown de gêneros
    genero_opcoes = [ft.DropdownOption(text=g[1], key=g[0]) for g in generos]
    dropdown_genero = ft.Dropdown(
        label="Filtrar por Gênero",
        options=genero_opcoes,
        on_change=lambda e: listar_jogos_por_genero(page, usuario_id, e.control.value)  # Chama a função para listar jogos filtrados
    )

    lista_jogos = []
    for jogo in jogos_disponiveis:
        id_jogo, titulo_jogo, descricao_jogo, preco, requisitos, data_lancamento, gratuito, _ = jogo

        preco_texto = "Gratuito" if gratuito == 1 else f"R$ {preco:.2f}"

        card_jogo = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([ 
                    ft.Text(titulo_jogo, size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Descrição: {descricao_jogo}", size=16),
                    ft.Text(f"Preço: {preco_texto}", size=16, color="green"),
                    ft.Text(f"Requisitos: {requisitos}", size=14, italic=True),
                    ft.Text(f"Lançamento: {data_lancamento}", size=14),
                    ft.ElevatedButton(
                        "Comprar Jogo",
                        on_click=lambda e, jogo_id=id_jogo, usuario_id=usuario_id: exibir_opcoes_pagamento(page, jogo_id, usuario_id)
                    ),
                    ft.ElevatedButton(
                        "Avaliar Jogo",
                        on_click=lambda e, jogo_id=id_jogo, usuario_id=usuario_id: tela_avaliacao_jogo(page, jogo_id, usuario_id)
                    ),
                    ft.ElevatedButton(
                        "Avaliações",
                        on_click=lambda e, jogo_id=id_jogo, usuario_id=usuario_id: mostrar_avaliacoes(page, jogo_id, usuario_id)
                    ),
                ])
            )
        )

        lista_jogos.append(card_jogo)

    jogos_vertical = ft.ListView(
        controls=lista_jogos,
        expand=True
    )

    botao_biblioteca = ft.ElevatedButton("Minha Biblioteca", on_click=lambda e: tela_biblioteca(page, usuario_id))
    botao_voltar = ft.ElevatedButton("Sair", on_click=lambda e: navegar_para_login(page))

    page.add(titulo, descricao, saldo_texto, dropdown_genero, jogos_vertical, botao_biblioteca, botao_voltar)
    page.update()





def comprar_jogo(page: ft.Page, id_jogo, usuario_id, forma_pagamento):
    conexao = conectar()
    if not conexao:
        page.add(ft.Text("Erro ao conectar ao banco de dados.", color="red"))
        page.update()
        return

    cursor = conexao.cursor()

    # Verifica saldo do jogador
    cursor.execute("SELECT Saldo_Carteira FROM jogador WHERE Usuario_id_Usuario = %s", (usuario_id,))
    resultado_saldo = cursor.fetchone()
    saldo_jogador = resultado_saldo[0] if resultado_saldo else 0.0

    # Verifica preço do jogo
    cursor.execute("SELECT Preco, Gratuito FROM jogo WHERE idJogo = %s", (id_jogo,))
    resultado_jogo = cursor.fetchone()
    
    if not resultado_jogo:
        page.add(ft.Text("Jogo não encontrado.", color="red"))
        page.update()
        cursor.close()
        conexao.close()
        return

    preco_jogo, gratuito = resultado_jogo

    if not gratuito and saldo_jogador < preco_jogo:
        page.add(ft.Text("Saldo insuficiente para comprar este jogo.", color="red"))
        page.update()
        cursor.close()
        conexao.close()
        return

    # Verifica se o jogador já possui o jogo na biblioteca
    cursor.execute("SELECT * FROM biblioteca WHERE Jogo_id_Jogo = %s AND Usuario_id_Usuario = %s", (id_jogo, usuario_id))
    if cursor.fetchone():
        page.add(ft.Text("Você já possui este jogo na sua biblioteca.", color="orange"))
        page.update()
        cursor.close()
        conexao.close()
        return

    # Adiciona o jogo na biblioteca
    cursor.execute("INSERT INTO biblioteca (Jogo_id_Jogo, Usuario_id_Usuario, Data_Aquisicao) VALUES (%s, %s, NOW())", (id_jogo, usuario_id))
    
    # Se o jogo não for gratuito, debita o saldo do jogador e registra o pagamento
    if not gratuito:
        novo_saldo = saldo_jogador - preco_jogo
        cursor.execute("UPDATE jogador SET Saldo_Carteira = %s WHERE Usuario_id_Usuario = %s", (novo_saldo, usuario_id))
        
        cursor.execute("""
            INSERT INTO pagamento (Valor_Pago, Forma_Pagamento, Data_Pagamento, jogo_idJogo, Usuario_id_Usuario) 
            VALUES (%s, %s, NOW(), %s, %s)
        """, (preco_jogo, forma_pagamento, id_jogo, usuario_id))

    conexao.commit()
    
    page.add(ft.Text("Jogo comprado e adicionado à sua biblioteca com sucesso!", color="green"))
    page.update()

    cursor.close()
    conexao.close()

def exibir_opcoes_pagamento(page: ft.Page, id_jogo, usuario_id):
    """Exibe as opções de pagamento para o jogador escolher."""
    saldo = obter_saldo(usuario_id)  # Buscar saldo do jogador

    # Exibir opções de pagamento
    titulo_pagamento = ft.Text("Escolha a forma de pagamento:", size=20, weight=ft.FontWeight.BOLD)

    # Botões de pagamento, agora com o parâmetro forma_pagamento
    botao_pix = ft.ElevatedButton("Pagar com Pix", on_click=lambda e: comprar_jogo(page, id_jogo, usuario_id, "Pix"))
    botao_cartao = ft.ElevatedButton("Pagar com Cartão", on_click=lambda e: comprar_jogo(page, id_jogo, usuario_id, "Cartão de Crédito"))
    botao_saldo = ft.ElevatedButton("Pagar com Saldo da Conta", on_click=lambda e: comprar_jogo(page, id_jogo, usuario_id, "Saldo da Conta"))

    # Mostrar o saldo atual do jogador
    saldo_texto = ft.Text(f"Seu saldo atual: R$ {saldo:.2f}", size=18, color="blue")

    # Adicionar elementos à página
    page.add(titulo_pagamento, saldo_texto, botao_pix, botao_cartao, botao_saldo)
    page.update()


# Função para obter o saldo da carteira do jogador
def obter_saldo(usuario_id):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT Saldo_Carteira FROM jogador WHERE Usuario_id_Usuario = %s", (usuario_id,))
        saldo = cursor.fetchone()
        cursor.close()
        conexao.close()
        return saldo[0] if saldo else 0.0  # Retorna o saldo ou 0.0 caso não encontre
    return 0.0

def obter_jogos_na_biblioteca(usuario_id):
    """Obtém os jogos que o jogador possui na biblioteca."""
    
    # Estabelece a conexão com o banco de dados
    conexao = conectar()  # Certifique-se de ter uma função conectar() que retorna a conexão
    cursor = conexao.cursor()

    query = """
    SELECT Jogo.titulo
    FROM Jogador
    INNER JOIN Biblioteca ON Jogador.Usuario_id_Usuario = Biblioteca.Usuario_id_Usuario
    INNER JOIN Jogo ON Biblioteca.Jogo_id_Jogo = Jogo.idJogo
    WHERE Jogador.Usuario_id_Usuario = %s
    """
    
    cursor.execute(query, (usuario_id,))
    jogos = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    cursor.close()
    conexao.close()

    return jogos


def tela_biblioteca(page: ft.Page, usuario_id):
    """Exibe a biblioteca de jogos do jogador."""
    page.clean()

    titulo = ft.Text("Biblioteca de Jogos", size=30, weight=ft.FontWeight.BOLD)
    descricao = ft.Text("Aqui estão os jogos que você possui.", size=20)

    # Obtém os jogos na biblioteca do jogador
    jogos = obter_jogos_na_biblioteca(usuario_id)

    lista_jogos = []
    for jogo in jogos:
        titulo_jogo = jogo[0]  # Obtém o título do jogo da tupla retornada

        card_jogo = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text(titulo_jogo, size=22, weight=ft.FontWeight.BOLD),
                ])
            )
        )

        lista_jogos.append(card_jogo)

    botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: tela_loja_jogos(page, usuario_id))

    page.add(titulo, descricao, *lista_jogos, botao_voltar)
    page.update()

def tela_avaliacao_jogo(page: ft.Page, id_jogo, usuario_id):
    """Tela para o jogador avaliar o jogo."""
    page.clean()

    # Título da tela
    titulo = ft.Text("Avaliação do Jogo", size=30, weight=ft.FontWeight.BOLD)
    
    # Campos para nota e comentário
    nota_input = ft.TextField(label="Nota (de 1 a 5)", keyboard_type=ft.KeyboardType.NUMBER)
    comentario_input = ft.TextField(label="Comentário", multiline=True, height=100)
    
    # Função para enviar avaliação
    def enviar_avaliacao(e):
        try:
            nota = float(nota_input.value)
            if nota < 1 or nota > 5:
                raise ValueError("A nota deve estar entre 1 e 5.")
            comentario = comentario_input.value
            
            # Chamada para a função que registra a avaliação no banco de dados
            avaliar_jogo(usuario_id, id_jogo, nota, comentario)
            
            page.add(ft.Text("Avaliação enviada com sucesso!", color="green"))
            page.update()
        except ValueError as ex:
            page.add(ft.Text(f"Erro: {ex}", color="red"))
            page.update()
    
    # Botão de enviar
    botao_enviar = ft.ElevatedButton("Enviar Avaliação", on_click=enviar_avaliacao)
    
    # Botão de voltar
    botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: tela_loja_jogos(page, usuario_id))
    
    # Adiciona os controles à tela
    page.add(titulo, nota_input, comentario_input, botao_enviar, botao_voltar)
    page.update()

def avaliar_jogo(usuario_id, id_jogo, nota, comentario):
    """Registra a avaliação do jogo no banco de dados."""
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()

        # Verifica se o jogador já avaliou o jogo
        cursor.execute("SELECT idAvaliacao FROM Avaliacao WHERE Jogo_idJogo = %s AND Usuario_id_Usuario = %s", (id_jogo, usuario_id))
        avaliacao_existente = cursor.fetchone()

        if avaliacao_existente:
            # Atualiza a avaliação existente
            cursor.execute("UPDATE Avaliacao SET Nota = %s, Comentario = %s WHERE idAvaliacao = %s", (nota, comentario))
            conexao.commit()
        else:
            # Insere uma nova avaliação
            cursor.execute("INSERT INTO Avaliacao (Jogo_idJogo, Usuario_id_Usuario, Nota, Comentario) VALUES (%s, %s, %s, %s)", (id_jogo, usuario_id, nota, comentario))
            conexao.commit()

        cursor.close()
        conexao.close()

def mostrar_avaliacoes(page: ft.Page, id_jogo, usuario_id):
    """Exibe as avaliações detalhadas de um jogo, mas sem remover o botão de avaliação."""
    
    # Conectar ao banco de dados
    conexao = conectar()  # Certifique-se de ter uma função conectar() que retorna uma conexão válida
    if not conexao:
        page.add(ft.Text("Erro ao conectar ao banco de dados.", color="red"))
        page.update()
        return

    # Criar o cursor e executar a consulta
    cursor = conexao.cursor()
    cursor.execute("SELECT Nota, Comentario FROM Avaliacao WHERE Jogo_idJogo = %s", (id_jogo,))
    avaliacoes = cursor.fetchall()
    cursor.close()  # Fechar o cursor após a consulta

    # Criar uma área para exibir as avaliações
    avaliacoes_texto = []
    for nota, comentario in avaliacoes:
        avaliacoes_texto.append(ft.Text(f"Nota: {nota}/5\nComentário: {comentario}", size=16))

    # Exibir avaliações em um novo container sem remover a loja
    container_avaliacoes = ft.Container(
        content=ft.Column(avaliacoes_texto),
        padding=10,
        expand=True
    )

    # Adicionar as avaliações na página sem remover o resto da interface
    page.add(container_avaliacoes)
    page.update()

    # Manter o botão de avaliação visível
    voltar_botao = ft.ElevatedButton("Voltar para a Loja", on_click=lambda e: tela_loja_jogos(page, usuario_id))
    page.add(voltar_botao)
    
    # Fechar a conexão
    conexao.close()

def listar_jogos_por_genero(page: ft.Page, usuario_id, genero_id=None):
    """Exibe os jogos organizados por gênero ou todos os jogos se nenhum gênero for selecionado."""
    conexao = conectar()
    if not conexao:
        page.add(ft.Text("Erro ao conectar ao banco de dados.", color="red"))
        page.update()
        return

    cursor = conexao.cursor()

    # Consulta para obter jogos e seus gêneros, com opção de filtrar por gênero
    if genero_id:
        cursor.execute("""
            SELECT j.idJogo, j.titulo, GROUP_CONCAT(g.nome ORDER BY g.nome SEPARATOR ', ') AS generos
            FROM jogo j
            JOIN jogo_genero jg ON j.idJogo = jg.Jogo_idJogo
            JOIN genero g ON jg.Genero_id_Genero = g.id_Genero
            WHERE g.id_Genero = %s  # Filtra pelo gênero
            GROUP BY j.idJogo
            ORDER BY j.titulo;
        """, (genero_id,))
    else:
        cursor.execute("""
            SELECT j.idJogo, j.titulo, GROUP_CONCAT(g.nome ORDER BY g.nome SEPARATOR ', ') AS generos
            FROM jogo j
            JOIN jogo_genero jg ON j.idJogo = jg.Jogo_idJogo
            JOIN genero g ON jg.Genero_id_Genero = g.id_Genero
            GROUP BY j.idJogo
            ORDER BY j.titulo;
        """)

    jogos = cursor.fetchall()

    if not jogos:
        page.add(ft.Text("Nenhum jogo encontrado.", color="red"))
        page.update()
        cursor.close()
        conexao.close()
        return

    # Exibir jogos e gêneros
    lista_jogos = []
    for jogo in jogos:
        id_jogo, titulo_jogo, generos = jogo
        card_jogo = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([ 
                    ft.Text(titulo_jogo, size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Gêneros: {generos}", size=16),
                    # Adicione botões ou outros elementos conforme necessário
                ])
            )
        )
        lista_jogos.append(card_jogo)

    jogos_vertical = ft.ListView(
        controls=lista_jogos,
        expand=True
    )

    botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: tela_loja_jogos(page, usuario_id))

    page.add(jogos_vertical, botao_voltar)
    page.update()

    cursor.close()
    conexao.close()


# Função de navegação para a tela inicial
def navegar_para_home(page: ft.Page):
    page.clean()
    tela_inicial(page)


# Função para navegar para a tela de login
def navegar_para_login(page: ft.Page):
    page.clean()
    tela_login(page)


# Função para navegar para a tela de cadastro de usuário
def navegar_para_cadastro(page: ft.Page):
    page.clean()
    tela_cadastro(page)



# Função para navegar para a tela de gerenciamento de jogos
def navegar_para_gerenciamento(page: ft.Page, usuario_id, tipo_usuario):
    page.clean()
    if tipo_usuario == "Empresa":
        tela_adicionar_jogo(page, usuario_id)
    elif tipo_usuario == "Jogador":
        tela_loja(page, usuario_id)



# Função principal para iniciar a aplicação
def main(page: ft.Page):
    navegar_para_home(page)


# Inicia a aplicação Flet
ft.app(target=main)
