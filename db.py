import sqlite3





def nome_tirar_lista(lista):

    nome_sem_lista = ''
    for i in lista:
        nome_sem_lista += i + " "

    return nome_sem_lista.strip()


def numero_tirar_lista(lista):

    return lista[0]


def procurar_estoque(nome):
    mostrar = """select nome_produto, quantidade_produto, preco_produto from tbl_estoque where nome_produto = ?"""
    cursor.execute(mostrar, (nome,))
    return cursor.fetchone()

def mostrar_tbl_funcionarios():
    tbl_funcionario = ("""select nome_funcionario, cpf_funcionario, senha_funcionario, perfil_funcionario from tbl_funcionarios""")
    cursor.execute(tbl_funcionario)
    return cursor.fetchall()
def procurar_funcionario(nome):
    mostrar = """select nome_funcionario from tbl_funcionarios where nome_funcionario = ?"""
    cursor.execute(mostrar, (nome,))
    return cursor.fetchone()

def procurar_cpf_funcionario(cpf):
    mostrar = """select nome_funcionario, cpf_funcionario, senha_funcionario, perfil_funcionario from tbl_funcionarios where cpf_funcionario = ?"""
    cursor.execute(mostrar, (cpf,))
    return cursor.fetchone()
def procurar_senha_funcionario(nome):
    mostrar = """select senha_funcionario from tbl_funcionarios where nome_funcionario = ?"""
    cursor.execute(mostrar, (nome,))
    return cursor.fetchone()

def procurar_perfil_funcionario(nome):
    perfil_usuario = ("""select perfil_funcionario from tbl_funcionarios where nome_funcionario = ?""")
    cursor.execute(perfil_usuario,(nome,))
    return cursor.fetchall()

def cadastrar_funcionario(nome_funcionario, cpf_funcionario, senha, perfil):

    inserir = ("""insert into tbl_funcionarios (nome_funcionario, cpf_funcionario, senha_funcionario, perfil_funcionario) values(?,?,?,?)""")

    cursor.execute(inserir, (nome_funcionario, cpf_funcionario, senha, perfil))
    conexao.commit()



def excluir_cadastro_funcionario(cpf):
    excluir = """delete from tbl_funcionarios where cpf_funcionario= ?"""
    cursor.execute(excluir,(cpf,))
    conexao.commit()

def mostrar_estoque():

    #declarando a variável nome_produto para receber o comando, para procurar na tabela o nome do produto
    nome_produto = """SELECT nome_produto, codigo, quantidade_produto, quantidade_minima, preco_produto FROM tbl_estoque"""
    #Mandando o comando para o banco de dados

    cursor.execute(nome_produto)

    estoque = cursor.fetchall()
    if estoque:

        #Selecionando as colunas
        return estoque

    if not estoque:
        return 'Estoque vazio'


def cadastrar_produto(nome_produto, codigo, quantidade_produto, quantidade_minima, preco_produto):
    cadastrar_sql = ("""insert into tbl_estoque (nome_produto, codigo, quantidade_produto, quantidade_minima, preco_produto) values(?,?,?,?,?) """)
    if procurar_estoque(nome_produto):
        return 'Produto já cadastrado'
    else:
        cursor.execute(cadastrar_sql, (nome_produto, codigo, quantidade_produto, quantidade_minima, preco_produto,))

        conexao.commit()


def mostrar_linha_tabela(nome_produto):
    # Procurar o nome do produto

    nome_sql = "SELECT nome_produto FROM tbl_estoque WHERE nome_produto = ?"
    cursor.execute(nome_sql, (nome_produto,))
    nome = cursor.fetchone()
    nome = nome_tirar_lista(nome)
    print(f'Nome: {nome}')



    # Procurar a quantidade do produto

    quantidade_sql = "SELECT quantidade_produto FROM tbl_estoque WHERE nome_produto = ?"
    cursor.execute(quantidade_sql, (nome_produto,))
    quantidade = cursor.fetchone()
    quantidade = numero_tirar_lista(quantidade)

    print(f'Quantidade: {quantidade}')

    # Procurar o preço do produto

    preco_sql = "SELECT preco_produto FROM tbl_estoque WHERE nome_produto = ?"
    cursor.execute(preco_sql, (nome_produto,))

    preco = cursor.fetchone()
    preco = numero_tirar_lista(preco)

    print(f'Preço: {preco}')

    conexao.commit()

def procurar_codigo_produto(codigo):
    procura_codigo = ('''select codigo from tbl_estoque''')
    cursor.execute(procura_codigo)
    procura_codigo = cursor.fetchall()

    existe = False
    if procura_codigo:
        for i in procura_codigo:

            if codigo == i[0]:

                existe = True

    return existe

def alterar_nome(nome_novo,nome_produto):
    nome_sql = ('''update tbl_estoque set nome_produto = ? where nome_produto = ?''')
    cursor.execute(nome_sql, (nome_novo,nome_produto,))

    conexao.commit()

def alterar_preco(preco_novo, nome_produto):
    nome_sql = ('''update tbl_estoque set preco_produto = ? where nome_produto = ?''')
    cursor.execute(nome_sql, (preco_novo,nome_produto))
    conexao.commit()

def alterar_quantidade(quantidade_nova, nome_produto):
    nome_sql = ('''update tbl_estoque set quantidade_produto = ? where nome_produto = ?''')
    cursor.execute(nome_sql, (quantidade_nova, nome_produto))
    conexao.commit()

def alterar_codigo_barras(nome_produto, codigo_barras):
    alterar_codigo = ("""update tbl_estoque set codigo = ? where nome_produto = ?""")
    cursor.execute(alterar_codigo, (codigo_barras, nome_produto,))
    conexao.commit()


def alterar_quantidade_minima(quantidade_minima, nome_produto):
    alterar_quantidade = ("""update tbl_estoque set quantidade_minima = ? where nome_produto = ?""")

    cursor.execute(alterar_quantidade,(quantidade_minima, nome_produto,))
    conexao.commit()

#------------Excluir Produto--------------------


def excluir_produto(nome_produto_excluido):

    if procurar_estoque(nome_produto_excluido):
        excluir_produto = ("""delete from tbl_estoque where nome_produto= ?""")
        cursor.execute(excluir_produto,(nome_produto_excluido,))
        conexao.commit()
        return 'Produto excluído'
    else:
        return 'Produto não encontrado'


#Conectando com o banco
conexao = sqlite3.connect('banco.db', check_same_thread=False)
cursor = conexao.cursor()


#cursor.execute("""insert into tbl_funcionarios (nome_funcionario, cpf_funcionario, senha_funcionario, perfil_funcionario) values (?,?,?,?)""", ('administrador', 12345678911,'12345', 'adm'))

#Criando a tabela tbl_produtos


#cursor.execute("""drop table tbl_estoque""")
cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_estoque (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome_produto VARCHAR not null unique,
                codigo integer not null unique,
                quantidade_produto real not null,
                quantidade_minima real not null,
                preco_produto real not null)""")

#Criando a tabela tbl_funcionarios

#cursor.execute("drop table tbl_funcionarios")
cursor.execute("CREATE TABLE IF NOT EXISTS tbl_funcionarios("
                   "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                   "nome_funcionario VARCHAR NOT NULL,"
                   "cpf_funcionario INT NOT NULL unique,"
                   "senha_funcionario VARCHAR NOT NULL,"
                   "perfil_funcionario VARCHAR NOT NULL)")


#Salvando alterações
conexao.commit()




