#Importa o modulo do pyodbc para a conexao com o banco de dados
import pyodbc
#Importa o modulo tkinter para construção de interface gráfica
from tkinter import *
#Importa a classe ttk do modulo tkinter
from tkinter import ttk

#Função que verifica credenciais
def verifica():
    conexao = pyodbc.connect("Driver={SQLite3 ODBC Driver};Server=localhost;Database=C:\\Users\\João Pedro\\Desktop\\Python SQL\\Projetos_Compras.db")

    cursor = conexao.cursor()

    #Executando uma query que seleciona os usuários que possuem o nome de usuário e senha inseridos pelo usuário
    cursor.execute("SELECT * FROM Usuarios WHERE Nome = ? and Senha = ?", (nameEntry.get(), senhaEntry.get()))

    #Recebendo os dados resultados da query
    usuario = cursor.fetchone()
    if usuario:
        Window.destroy()

        # Agora é a janela principal que vai abrir caso o login esteja correto

        dadosConexao = (
            "Driver={SQLite3 ODBC Driver};Server=localhost;Database=C:\\Users\\João Pedro\\Desktop\\Python SQL\\Projetos_Compras.db")
        conexao = pyodbc.connect(dadosConexao)
        cursor = conexao.cursor()
        conexao.execute("SELECT * FROM Produtos")
        print("Conectado com sucesso!")

        def listaDados():

            # Limpa os valores da treeview
            for i in treeview.get_children():
                treeview.delete(i)

            cursor.execute("SELECT * FROM Produtos")
            valores = cursor.fetchall()

            # Adiciona os valores na treeview
            for valor in valores:
                treeview.insert("", "end", values=(valor[0], valor[1], valor[2], valor[3]))

        window = Tk()
        window.title("Cadastro de Produtos")

        window.configure(bg="white", )

        # Deixando a janela em tela cheia
        window.attributes("-fullscreen", True)

        Label(window, text="Nome do Produto: ", font="Arial 16", fg="black", bg="white").grid(row=0, column=2, padx=10,
                                                                                              pady=10)
        nomeProduto = Entry(window, font="Arial 16")
        nomeProduto.grid(row=0, column=3, padx=10, pady=10)

        Label(window, text="Descrição do Produto: ", font="Arial 16", fg="black", bg="white").grid(row=0, column=5,
                                                                                                   padx=10, pady=10)
        descricaoProduto = Entry(window, font="Arial 16")
        descricaoProduto.grid(row=0, column=6, padx=10, pady=10)

        Label(window, text="Produtos", font="Arial 16", fg="blue", bg="white").grid(row=2, column=0, columnspan=10,
                                                                                    padx=10, pady=10)

        def cadastrar():
            # Criando uma nova janela para cadastrar um novo produto
            windowCadastrar = Toplevel(window)
            windowCadastrar.title("Cadastrar Produto")

            windowCadastrar.configure(bg="grey")

            larguraJanela = 400
            alturaJanela = 250

            # obtem a largura e a altura da tela do computador
            larguraTela = windowCadastrar.winfo_screenwidth()
            alturaTela = windowCadastrar.winfo_screenheight()

            posx = (larguraTela // 2) - (larguraJanela // 2)
            posy = (alturaTela // 2) - (alturaJanela // 2)

            # Define a posição da janela
            windowCadastrar.geometry('{}x{}+{}+{}'.format(larguraJanela, alturaJanela, posx, posy))

            for i in range(5):
                windowCadastrar.grid_rowconfigure(i, weight=1)
            for i in range(2):
                windowCadastrar.grid_columnconfigure(i, weight=1)

            Label(windowCadastrar, text="Nome do Produto:", font=("Arial", 12), bg="Grey").grid(row=0, column=0,
                                                                                                padx=10, pady=10,
                                                                                                stick="W")
            NomeProduto = Entry(windowCadastrar, font="Arial 12", relief=GROOVE)
            NomeProduto.grid(row=0, column=1, padx=10, pady=10)  # relief é para adicionar borda

            Label(windowCadastrar, text="Descrição do Produto:", font=("Arial", 12), bg="Grey").grid(row=1, column=0,
                                                                                                     padx=10, pady=10,
                                                                                                     stick="W")
            Descricao = Entry(windowCadastrar, font="Arial 12", relief=GROOVE)
            Descricao.grid(row=1, column=1, padx=10, pady=10)

            Label(windowCadastrar, text="Preço do Produto:", font=("Arial", 12), bg="Grey").grid(row=2, column=0,
                                                                                                 padx=10, pady=10,
                                                                                                 stick="W")
            Preco = Entry(windowCadastrar, font="Arial 12", relief=GROOVE)
            Preco.grid(row=2, column=1, padx=10, pady=10)

            def salvar():

                # Cria uma tupla com os valores dos campos de texto
                novoproduto = (NomeProduto.get(), Descricao.get(), Preco.get())
                cursor.execute("INSERT INTO Produtos(NomeProduto, Descricao, Preco) values (?, ?, ?)", novoproduto)
                conexao.commit()  # Gravando no bd
                print("Dados cadastrados com sucesso!")
                windowCadastrar.destroy()
                # Chama a função para listar os valores na treeview
                listaDados()

            Button(windowCadastrar, text="Salvar", font="Arial 12", command=salvar).grid(row=3, column=0, columnspan=2,
                                                                                         padx=10, pady=10, stick="NSEW")
            Button(windowCadastrar, text="Cancelar", font="Arial 12", command=windowCadastrar.destroy).grid(row=4,
                                                                                                            column=0,
                                                                                                            columnspan=2,
                                                                                                            padx=10,
                                                                                                            pady=10,
                                                                                                            stick="NSEW")

        # Cria um botão para adicionar novos dados
        adicionar = Button(window, text="Novo", command=cadastrar, font="Arial 26").grid(row=4, column=0, columnspan=4,
                                                                                         stick="NSEW", pady=5)

        # Define o estilo da Treeview
        style = ttk.Style(window)
        style.theme_use("default")
        style.configure("mystyle.Treeview", font=("Arial 14"))
        # Criando a Treeview
        treeview = ttk.Treeview(window, style="mystyle.Treeview")
        treeview = ttk.Treeview(window, style="mystyle.Treeview", columns=("ID", "NomeProduto", "Descricao", "Preco"),
                                show="headings", height=20)

        treeview.heading("ID", text="ID")
        treeview.heading("NomeProduto", text="Nome do Produto")
        treeview.heading("Descricao", text="Descrição do Produto")
        treeview.heading("Preco", text="Preço do Produto")
        # A primeira coluna, identificada como "#0"
        # A opção "stretch=NO" indica que a coluna não deve esticar para preencher o espaço
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("ID", width=100)
        treeview.column("NomeProduto", width=300)
        treeview.column("Descricao", width=500)
        treeview.column("Preco", width=200)

        treeview.grid(row=3, column=0, columnspan=10, stick="NSEW")

        listaDados()

        def editarDados(event):
            # Obtém o item selecionado na treeview
            itemSelecionado = treeview.selection()[0]

            # Obtém os valores do item selecionado
            valoresSelecionados = treeview.item(itemSelecionado)['values']

            winEdicao = Toplevel(window)
            winEdicao.title("Editar Produto")

            winEdicao.configure(bg="grey")

            larguraJanela = 500
            alturaJanela = 200

            # obtem a largura e a altura da tela do computador
            larguraTela = winEdicao.winfo_screenwidth()
            alturaTela = winEdicao.winfo_screenheight()

            posx = (larguraTela // 2) - (larguraJanela // 2)
            posy = (alturaTela // 2) - (alturaJanela // 2)

            # Define a posição da janela
            winEdicao.geometry('{}x{}+{}+{}'.format(larguraJanela, alturaJanela, posx, posy))

            for i in range(5):
                winEdicao.grid_rowconfigure(i, weight=1)
            for i in range(2):
                winEdicao.grid_columnconfigure(i, weight=1)

            Label(winEdicao, text="Nome do Produto:", font=("Arial", 16), bg="Grey").grid(row=0, column=0, padx=10,
                                                                                          pady=10, stick="W")
            NomeProdutoEdicao = Entry(winEdicao, font="Arial 16", relief=GROOVE, bg="Grey",
                                      textvariable=StringVar(value=valoresSelecionados[1]))
            NomeProdutoEdicao.grid(row=0, column=1, padx=10, pady=10)  # relief é para adicionar borda

            Label(winEdicao, text="Descrição do Produto:", font=("Arial", 16), bg="Grey").grid(row=1, column=0, padx=10,
                                                                                               pady=10, stick="W")
            DescricaoEdicao = Entry(winEdicao, font="Arial 16", relief=GROOVE, bg="Grey",
                                    textvariable=StringVar(value=valoresSelecionados[2]))
            DescricaoEdicao.grid(row=1, column=1, padx=10, pady=10)

            Label(winEdicao, text="Preço do Produto:", font=("Arial", 16), bg="Grey").grid(row=2, column=0, padx=10,
                                                                                           pady=10, stick="W")
            PrecoEdicao = Entry(winEdicao, font="Arial 16", relief=GROOVE, bg="Grey",
                                textvariable=StringVar(value=valoresSelecionados[3]))
            PrecoEdicao.grid(row=2, column=1, padx=10, pady=10)

            def salvarEdicao():

                # Obtém os novos valores do item selecionado no Treeview
                nomeproduto = NomeProdutoEdicao.get()
                novaDescricao = DescricaoEdicao.get()
                novoPreco = PrecoEdicao.get()

                treeview.item(itemSelecionado, values=(valoresSelecionados[0], nomeproduto, novaDescricao, novoPreco))

                cursor.execute(
                    "UPDATE Produtos SET NomeProduto = ?, Descricao = ?, Preco = ? WHERE ID = ?, (nomeproduto, novaDescricao, novoPreco, valoresSelecionados[0]")

            conexao.commit()  # Gravando no BD

            print("Dados alterados com sucesso!")

            winEdicao.destroy

            def deletarregistro():
                # Recupera o id do registro selecionado na treeview
                itemselecionado = treeview.selection()[0]
                id = treeview.item(itemselecionado)['values'][0]

                # deleta o registro do bd
                cursor.execute("DELETE FROM Produtos WHERE id = ?", (id))
                conexao.commit()

                winEdicao.destroy
                # atualiza dados
                listaDados()

            Button(winEdicao, text="Alterar", font="Arial 12", command=salvarEdicao).grid(row=4, column=0, padx=20,
                                                                                          pady=20)
            Button(winEdicao, text="Deletar", font="Arial 12", command=deletarregistro, bg="red", fg="white").grid(
                row=4, column=1, padx=20, pady=20)

        # Adiciona o evento de duplo clique na Treeview para editar os dados do produto
        treeview.bind("<Double-1>", editarDados)

        # Configurando a janela para utilizar a barra de menus criada
        menuBar = Menu(window)
        window.configure(menu=menuBar)
        # Cria o menu chamado Arquivo
        menuArquivo = Menu(menuBar, tearoff=0)  # tearoff é para desabilitar ou habilitar a linha pontilhada do menu
        menuBar.add_cascade(label="Arquivo", menu=menuArquivo)

        # Cria uma opção no menu "Arquivo" chamada "Cadastrar"
        menuArquivo.add_command(label="Cadastrar", command=cadastrar)
        # Cria uma opção no menu "Arquivo" chamada "Sair"
        menuArquivo.add_command(label="Sair", command=window.destroy)

        def limparDados():
            for i in treeview.get_children():
                treeview.delete(i)

        def filtrarDados(nomeProduto, descricaoProduto):
            # Se os campos estão vazios
            if not nomeProduto.get() and not descricaoProduto.get():
                listaDados()
                # Se estiverem vazios, não faz nada
                return
            sql = "SELECT * FROM Produtos"
            params = []
            if nomeProduto.get():
                # Junta o comando sql com o where para adiconar uma condição de filtro para buscar
                # valores de produtos com o padrão digitado.
                sql += " WHERE NomeProduto LIKE ?"
                # Os símbolos indicam que não faz diferença se o valor começa com o que foi digitado ou termina.
                params.append('%' + nomeProduto.get() + '%')

            if descricaoProduto.get():
                if nomeProduto.get():
                    sql += " AND"
                else:
                    sql += " WHERE"
                sql += " Descricao LIKE ?"
                params.append('%' + descricaoProduto.get() + '%')

            cursor.execute(sql, tuple(params))
            produtos = cursor.fetchall()

            # Limpa treeview
            limparDados()

            # Preenche treeview com dados filtrados
            for dado in produtos:
                treeview.insert('', 'end', values=(dado[0], dado[1], dado[2], dado[3]))

        # Associa um evento de liberação de tecla('KeyRelease') ao widget de entrada de texto
        # chamado 'nome_produto'. Quando esse evento ocorrer, a função lambda definida será executada.
        # A função lambda recebe um objeto de evento 'e' como argumento e chama outra função chamada filtrarDados.
        # O objetivo disso é permitir que o usuário filtre os dados mostrados no programa com base no que foi
        # digitado no campo 'nome_produto'. Quando o usuário digita algo no campo 'nome_produto' e solta a tecla, a função filtrarDados é executada.
        nomeProduto.bind('<KeyRelease>', lambda e: filtrarDados(nomeProduto, descricaoProduto))

        def deletar():
            # Recupera o id do registro selecionado na treeview
            itemselecionado = treeview.selection()[0]
            id = treeview.item(itemselecionado)['values'][0]

            # deleta o registro do bd
            cursor.execute("DELETE FROM Produtos WHERE id = ?", (id))
            conexao.commit()

            # atualiza dados
            listaDados()

        deletar = Button(window, text="Deletar",
                         command=deletar,
                         font="Arial 26").grid(row=4,
                                               column=4,
                                               columnspan=4,
                                               stick="NSEW",
                                               pady=5,
                                               padx=5)

        window.mainloop()

        cursor.close()
        conexao.close()

    else:
        mensagem = Label(Window,
                         text = "Nome de usuário ou senha incorretos",
                         fg="red",
                         bg="white")
        mensagem.grid(row=3,
                      column=0,
                      columnspan=2)
#Criando a janela para login
Window = Tk()
Window.title("Tela de Login")

#Definindo a cor de fundo da janela
Window.configure(bg = "white")

larguraJanela = 450
alturaJanela = 300

#obtem a largura e a altura da tela do computador
larguraTela = Window.winfo_screenwidth()
alturaTela = Window.winfo_screenheight()

posx = (larguraTela // 2) - (larguraJanela // 2)
posy = (alturaTela // 2) - (alturaJanela // 2)

#Define a posição da janela
Window.geometry('{}x{}+{}+{}'.format(larguraJanela, alturaJanela, posx, posy))

#columnspan = quantas colunas vai ocupar no grid, ou seja, vai ficar entre elas
#por exemplo, entre 2 colunas, fica no meio da tela, como feito no primeiro Label abaixo.
#pady = espaçamento
label = Label(Window,
              text="Tela de Login",
              font="Arial 25",
              fg="blue",
              bg="white")
label.grid(row=0,
           column=0,
           columnspan=2,
           pady=20)

#stick = onde o label será ocupado, ele preenche as laterais ou em cima e embaixo do label
#esticando ele, stick = esticar.
name = Label(Window,
             text="Nome de usuário",
             font="Arial 19 bold",
             bg="white")
name.grid(row=1,
          column=0,
          stick="e")

senha = Label(Window,
              text="Senha",
              font="Arial 19 bold",
              bg="white")
senha.grid(row=2,
           column=0,
           stick="e")

nameEntry = Entry(Window, font="Arial 14")
nameEntry.grid(row=1,
               column=1,
               pady=10)

senhaEntry = Entry(Window, font="Arial 14", show="*")
senhaEntry.grid(row=2,
                column=1,
                pady=10)

btnEntrar = Button(Window,
                   text="Entrar",
                   font="Arial 14",
                   command=verifica)
btnEntrar.grid(row=4,
               column = 0,
               columnspan=2,
               padx=20,
               pady=10,
               stick="NSEW")

btnEntrar = Button(Window,
                   text="Sair",
                   font="Arial 14",
                   command=Window.destroy)
btnEntrar.grid(row=5,
               column = 0,
               columnspan=2,
               padx=20,
               pady=10,
               stick="NSEW")

for i in range(5):
    Window.grid_rowconfigure(i, weight=1)
for i in range(2):
    Window.grid_columnconfigure(i, weight=1)


#Inicia a janela do tkinter
Window.mainloop()
