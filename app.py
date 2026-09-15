

from db import mostrar_estoque, procurar_estoque, cursor, conexao, mostrar_linha_tabela, procurar_funcionario, \
    procurar_senha_funcionario, procurar_perfil_funcionario, cadastrar_produto, alterar_nome, alterar_quantidade, \
    alterar_preco, nome_tirar_lista, excluir_produto, cadastrar_funcionario, procurar_cpf_funcionario, \
    mostrar_tbl_funcionarios, excluir_cadastro_funcionario, alterar_codigo_barras, alterar_quantidade_minima, \
    procurar_codigo_produto
from flask import Flask, request, render_template, flash, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'


#-------------Verifica Login ---------------------------
def verificar_login():
    if 'usuario' not in session:
        return False
    return  True

#-------------------Verifica se não é adm-----------------
def verificar_login_adm():
    if verificar_login() is True:

        if session['perfil'] != 'adm':
            return False



#-----------------Index.html------------------------


@app.route('/')
def inicio():

    return render_template('index.html')


#----------------Sair------------------------------


@app.route('/sair')
def sair():
    session.clear()
    return render_template('index.html')

@app.route('/entrar', methods=['POST'])
def entrar():

    #Trazendo nome e senha inseridos pelo usuário
    nome = request.form["nome"].lower()
    senha = request.form["senha"]
    try:
        cpf = int(request.form['cpf'])
    except:
        flash('Existem campos não preenchidos')
        return render_template('index.html')
    #Verificando se funcionário existe e se a senha está correta


    if procurar_cpf_funcionario(cpf) and procurar_cpf_funcionario(cpf)[0] == nome and procurar_cpf_funcionario(cpf)[2] == senha:
        perfil = procurar_cpf_funcionario(cpf)[3]

        session['usuario'] = nome
        session['perfil'] = perfil

        #Se perfil do funcionário for adm irá abrir a página estoque_admin.html
        if procurar_cpf_funcionario(cpf)[3]== 'adm':
            flash('')
            return render_template("estoque_admin.html")

        else:#Caso, perfil do usuário seja comum
            return render_template('estoque_comum.html')
    else:

        #Mostrar ao usuário erro
        flash('Usuário, Senha ou Cpf estão incorretos')

        #Carregar a página novamente
        return render_template('index.html')


#---------------------------estoque_admin.html------------------------------


@app.route("/criar_conta")

def pagina_criar_conta():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:

        return render_template("criar_conta.html")


#-----------------------------Criar Conta----------------------


@app.route('/criar_conta', methods = ["POST"])
def criar_conta():

    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        nome = request.form["nome"].lower().split()
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        try:
            perfil = request.form["perfil"]
        except:
            flash('Perfil do usuário não foi preenchido')
            return render_template('criar_conta.html')
        contador = 0
        nome = nome_tirar_lista(nome)
        nome_passou = False
        cpf_passou = False
        senha_passou = False

        if nome and senha and confirmar_senha and perfil and cpf:

            #----------------Se nome tiver mais de duas letras-------------------------

            for i in nome:
                contador += 1


            if contador > 2:
                nome_passou = True


            #--------Se cpf tiver mais de 11 digítos----------------------
            contador = 0
            for i in cpf:
                contador += 1

            if contador >= 11:
                cpf_passou = True


            #-------------Se senha tiver mais de 5 digítos-----------------------------

            contador = 0
            for i in senha:
                contador += 1

            if contador >= 5:
                senha_passou = True


            if nome_passou == True and senha_passou == True and cpf_passou == True:
                if senha == confirmar_senha:


                    #-------------------------Cpf já cadastrado---------------------

                    if procurar_cpf_funcionario(cpf):
                        flash('Cpf já cadastrado')
                        return render_template('criar_conta.html',)


                    #-------------------------Usuário não cadastrado------------------------------


                    else:

                        #-----------------Cadastrar Funcionário-----------------------

                        cadastrar_funcionario(nome, cpf, senha, perfil)
                        return render_template('estoque_admin.html')
                else:
                    flash('Senha e confirmar senha não são iguais')
                    return render_template('criar_conta.html',)


            if not nome_passou == True:
                flash('Número minímo de caracteres não atingido em nome')
                return render_template('criar_conta.html')

            if not cpf_passou == True:
                flash('Número minímo de caracteres não atingido no cpf')
                return render_template('criar_conta.html')

            if not senha_passou == True:
                flash('Número minímo de caracteres não atingido em senha')
                return render_template('criar_conta.html')

        else:
            flash('Existe campos não preenchidos')
            return render_template('criar_conta.html')


#---------------------Visualizar Cadastro de Funcionários-----------------------


@app.route('/visualizar_cadastro_funcionario')
def visualizar_cadastro():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        flash(mostrar_tbl_funcionarios())
        return render_template('visualizar_cadastro_funcionario.html')


#-------------------Excluir Cadastro Funcionario página--------------------------


@app.route('/excluir_cadastro_funcionario_pagina')
def excluir_cadastro_funcionario_pagina():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        return render_template('excluir_cadastro_funcionario.html')

#-------------Visualizar Cadastro de funcionarios--------------------------

@app.route('/visualizar_cadastro_cpf_funcionario', methods = ['post'])
def visualizar_cadastro_cpf():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        cpf = request.form['cpf']
        nome = request.form['nome']

        if procurar_cpf_funcionario(cpf) and nome:
            if procurar_cpf_funcionario(cpf)[0] == nome and procurar_cpf_funcionario(cpf):
                funcionario = procurar_cpf_funcionario(cpf)
                flash(funcionario)
                return render_template('/excluir_cadastro_funcionario.html', nome = nome, cpf = cpf)
            else:
                return render_template('excluir_cadastro_funcionario.html', mensagem = 'Nome ou cpf estão incorretos')

        else:
            return render_template('excluir_cadastro_funcionario.html', mensagem = 'Existem campos não preenchidos')


#-------------------------Excluir cadastro de funcionario--------------------------

@app.route('/excluir_cadastro_funcionario', methods = ['post'])
def excluir_cadastro_funcionario_funcao():

    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:

        nome = request.form['nome_funcionario'].lower().split()
        cpf = request.form['cpf_funcionario']

        nome = nome_tirar_lista(nome)



        if procurar_cpf_funcionario(cpf)[0] == nome and procurar_cpf_funcionario(cpf)[1]:
            mensagem = f'Cadastro do(a) funcionário(a) {procurar_cpf_funcionario(cpf)[0]} foi excluído com sucesso'
            excluir_cadastro_funcionario(cpf)
            return render_template('/excluir_cadastro_funcionario.html', mensagem = mensagem)

        else:

            mensagem = 'Nome ou cpf estão incorretos'
            return render_template('/excluir_cadastro_funcionario.html', mensagem = mensagem)





#--------------------Estoque Admin----------------------

@app.route('/estoque_admin')
def estoque_admin():

    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        return render_template('estoque_admin.html')

#--------------------Cadastro de produtos----------------------

@app.route('/cadastrar_produto',methods = ["POST"])
def cadastro_produtos():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:

        nome = request.form['nome_produto_cadastrar'].lower().split()#transformando em lista para tirar os espaços entre as palavras
        quantidade_minima = float(request.form['quantidade_minima_cadastrar'])
        quantidade_produto = float(request.form['quantidade_produto_cadastrar'])
        preco_produto = float(request.form['preco_produto_cadastrar'])
        codigo_produto = int(request.form['codigo_produto_cadastrar'])

        contador = 0  # Criando a variável

        # Tirando a lista do nome
        for i in nome:
            if contador == 0:
                nome_produto = i

            else:
                nome_produto = nome_produto + ' ' + i

            contador += 1

        #Contando as letras do nome_produto
        contador_letras = 0
        for i in nome_produto:
            contador_letras += 1

        # Procura no estoque se já foi cadastrado o produto

        if procurar_estoque(nome_produto):
            flash('Produto já cadastrado')
            return render_template('/estoque_admin.html')

        else:

            if quantidade_produto > 0 and preco_produto > 0 and contador_letras > 1 and codigo_produto > 0 and quantidade_minima > 0:

                if procurar_codigo_produto(codigo_produto) is False:
                    cadastrar_produto(nome_produto, codigo_produto, quantidade_produto, quantidade_minima, preco_produto )
                    flash(f'{nome_produto} cadastrado')
                    return render_template('/estoque_admin.html', )
                else:
                    flash('Código do produto já cadastrado')
                    return render_template('/estoque_admin.html')
            else:
                flash(f'Quantidade e preço do produto tem que ser maiores que zero')
                return render_template('/estoque_admin.html')


#-------------------Editar Produtos-----------------------------------


@app.route('/escolha_update', methods = ['POST'])
def escolha_update():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        nome = request.form['nome_produto_antigo'].lower().split()
        escolha = request.form['botao']


        nome_produto = nome_tirar_lista(nome)

        if procurar_estoque(nome_produto):
            flash(mostrar_linha_tabela(nome_produto))
            if escolha == 'novo_nome':
                return render_template('/estoque_admin.html', escolha = 'novo_nome',nome_produto = nome_produto)

            if escolha == 'nova_quantidade':
                return render_template('/estoque_admin.html', escolha = 'nova_quantidade',nome_produto = nome_produto)

            if escolha == 'novo_preco':
                return render_template('/estoque_admin.html', escolha = 'novo_preco', nome_produto = nome_produto)

            if escolha == 'novo_codigo':
                return render_template('estoque_admin.html', escolha = 'novo_codigo', nome_produto = nome_produto)

            if escolha == 'nova_quantidade_minima':
                return render_template('estoque_admin.html', escolha='nova_quantidade_minima', nome_produto=nome_produto)
        else:
            flash('Produto não encontrado')
            return render_template('/estoque_admin.html')
#------------------Alterar Produto--------------------------


@app.route('/alterar_produto', methods = ['POST'])
def alterar_produto():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        nome_antigo = request.form['nome_produto'].lower().split()

        nome_antigo = nome_tirar_lista(nome_antigo)


        if 'nome_novo' in request.form:
            novo_nome = request.form['nome_novo'].lower().split()
            novo_nome = nome_tirar_lista(novo_nome)
            if novo_nome != '':
                alterar_nome(novo_nome, nome_antigo)
                flash(f'Nome alterado com sucesso')

                return  render_template('estoque_admin.html')
            else:
                flash('Preencha o campo')
                return render_template('estoque_admin.html')
        elif 'quantidade_nova' in request.form:

            quantidade = float(request.form['quantidade_nova'])

            if quantidade >= 0:
                alterar_quantidade(quantidade, nome_antigo)
                flash('Quantidade alterada com sucesso')
                return render_template('estoque_admin.html')
            else:
                flash('Quantidade tem que ser superior a 0')
                return  render_template('estoque_admin.html')


        elif 'preco_novo' in request.form:
            preco = float(request.form['preco_novo'])
            if preco > 0:

                alterar_preco(preco, nome_antigo)
                flash('Preço alterado com sucesso')
                return render_template('estoque_admin.html')

            else:
                flash('Preço tem que ser superior a 0')
                return render_template('estoque_admin.html')

        elif 'codigo_novo' in request.form:
            codigo = int(request.form['codigo_novo'])
            if codigo >= 0:
                if procurar_codigo_produto(codigo) is False:
                    alterar_codigo_barras(nome_antigo, codigo)
                    flash('Código alterado com sucesso')
                    return render_template('estoque_admin.html')

                else:
                    flash('Código do produto já cadastrado')
                    return render_template('estoque_admin.html')

            else:
                flash('Código tem que ser superior a 0')
                return render_template('estoque_admin.html')

        elif 'nova_quantidade_minima' in request.form:

            quantidade_minima = float(request.form['nova_quantidade_minima'])

            if quantidade_minima >= 0:
                alterar_quantidade_minima(quantidade_minima, nome_antigo)
                flash('Quantidade mínima alterada com sucesso')
                return render_template('estoque_admin.html')
            else:
                flash('Quantidade mínima tem que ser igual ou superior a 0')
                return  render_template('estoque_admin.html')
        else:

            flash('Preencha o campo')
            return render_template('estoque_admin.html')

#------------------Mostrar Estoque----------------------

@app.route('/mostrar_estoque_html')
def mostrar_estoque_html():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        if mostrar_estoque():
            estoque = mostrar_estoque()

            return render_template('/estoque_admin.html', estoque = estoque)



#-----------Excluir Produto-----------------


@app.route("/excluir_produto_html", methods = ['post'])
def excluir_produto_html():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:

        nome_produto = request.form['nome_produto_excluido'].lower().split()
        nome_produto = nome_tirar_lista(nome_produto)

        produto_excluido = excluir_produto(nome_produto)

        return render_template('/estoque_admin.html', produto_excluido = produto_excluido)


#----------------------Mostrar Avisos-----------------------------------

@app.route('/mostrar_avisos')
def mostrar_avisos():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if verificar_login_adm() is False:

        flash("Acesso só para administradores")
        return render_template('index.html')
    else:
        estoque = mostrar_estoque()
        aviso = ''
        if estoque != "Estoque vazio":
            for produto in estoque:
                if produto[3] >= produto[2]:

                    aviso += f"Nome:{produto[0]}, Código: {produto[1]}, Quantidade: {produto[2]}, Quantidade Mínima: {produto[3]}, Preço: R${produto[4]:.2f}<br><br>"
            if aviso:

                return render_template('estoque_admin.html', mensagem = 'Quantidade Mínima Atingida', avisos = aviso)
            else:
                return render_template('estoque_admin.html', mensagem = 'Sem Avisos')

        else:
            return render_template('estoque_admin.html', mensagem = 'Sem Avisos')

#--------------------------estoque_comum.html----------------------------


@app.route("/mostrar_estoque_comum")
def mostrar_estoque_comum():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    if mostrar_estoque():
        estoque = mostrar_estoque()

        return render_template('/estoque_comum.html', estoque = estoque)


#-----------------------Entrade de Produtos ------------------------------

@app.route('/entrada_produtos', methods =['post'])
def entrada_produtos():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    else:

        nome = request.form['nome'].lower().split()
        nome = nome_tirar_lista(nome)
        quantidade = float(request.form['quantidade'])

        if nome and quantidade:
            if procurar_estoque(nome):
                if quantidade > 0.001:

                    quantidade_antiga = procurar_estoque(nome)[1]
                    quantidade += quantidade_antiga
                    alterar_quantidade(quantidade, nome)
                    flash(f'Quantidade Antiga {quantidade_antiga}, Quantidade Nova: {quantidade}')
                    return render_template('estoque_comum.html')
                else:
                    flash('Quantidade tem que ser superior a 0.001')
                    return  render_template('estoque_comum.html')
            else:
                flash('Produto não encontrado')
                return render_template('estoque_comum.html')

        else:
            flash('Existem campos não preenchidos')
            return render_template('estoque_comum.html')


#-----------------Retirada de Produtos----------------------------


@app.route('/retirada_produtos', methods = ['post'])
def retirada_produtos():
    if verificar_login() is False:
        flash('Faça login primeiro')
        return render_template('index.html')

    else:

        nome = request.form['nome'].lower().split()
        nome = nome_tirar_lista(nome)
        quantidade = float(request.form['quantidade'])

        if nome and quantidade:
            if procurar_estoque(nome):
                if quantidade > 0.001:

                    quantidade_antiga = procurar_estoque(nome)[1]
                    if quantidade_antiga >= quantidade:
                        quantidade_nova = quantidade_antiga - quantidade
                        alterar_quantidade(quantidade_nova, nome)
                        flash(f'Quantidade Antiga {quantidade_antiga}, Quantidade Nova: {quantidade_nova}')
                        return render_template('estoque_comum.html')
                    else:
                        flash('Quantidade insuficiente em estoque')
                        return render_template('estoque_comum.html')
                else:
                    flash('Quantidade tem que ser superior a 0.001')
                    return render_template('estoque_comum.html')
            else:
                flash('Produto não encontrado')
                return render_template('estoque_comum.html')

        else:
            flash('Existem campos não preenchidos')
            return render_template('estoque_comum.html')

app.run(debug = True)

