from sqlalchemy import create_engine
from sqlalchemy.sql import text

# para rodar esse arquivo, instale a versão 1.4 do sqlalchemy
# python -m pip install sqlalchemy==1.4

class NotFoundError(Exception):
    pass


engine = create_engine('sqlite:///tinder.db')

#criar a tabela
with engine.connect() as con:    
    create_pessoas = """
    CREATE TABLE IF NOT EXISTS Pessoa (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        sexo TEXT,
        busca_homem BOOL,
        busca_mulher BOOL
    )
    """
    #seria melhor sexo ser ENUM (H, M)    
    rs = con.execute(create_pessoas)
    create_interesses = """
    CREATE TABLE IF NOT EXISTS Interesse (
        id_interessado INTEGER,
        id_alvo INTEGER,
        FOREIGN KEY (id_interessado) REFERENCES Pessoas(id),
        FOREIGN KEY (id_alvo) REFERENCES Pessoas(id)
    )
    """    
    rs = con.execute(create_interesses)
#i.adiciona_pessoa({'nome':'fernando','id':1})
# maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}

class Erro(Exception):
    pass

def adiciona_pessoa(dic_pessoa):
    if len(dic_pessoa.keys()) == 2:
        adiciona_pessoa_old(dic_pessoa)
        return
    if len(dic_pessoa.keys()) == 4:
        adiciona_pessoa_new(dic_pessoa)
        return
    raise Erro
    
def adiciona_pessoa_old(dic_pessoa):
    with engine.connect() as con:    
        sql_criar = '''INSERT INTO Pessoa (id,nome,sexo, busca_homem, busca_mulher) 
                                   VALUES (:id,:nome,:sexo,:busca_homem,:busca_mulher)'''
        con.execute(sql_criar, nome=dic_pessoa['nome'], id=dic_pessoa['id'], 
                                sexo=None, 
                                busca_homem=None,
                                busca_mulher=None)

def adiciona_pessoa_new(dic_pessoa):
    with engine.connect() as con:    
        sql_criar = '''INSERT INTO Pessoa (id,nome,sexo, busca_homem, busca_mulher) 
                                   VALUES (:id,:nome,:sexo,:busca_homem,:busca_mulher)'''
        sexo = dic_pessoa["sexo"] # Homem, Mulher
        if sexo == "mulher":
            sexo = "M"
        if sexo == "homem":
            sexo = "H"
        buscando = dic_pessoa["buscando"]
        busca_homem = ("homem" in buscando)
        busca_mulher = ("mulher" in buscando)
        con.execute(sql_criar, nome=dic_pessoa['nome'], id=dic_pessoa['id'], 
                               sexo=sexo, busca_homem=busca_homem, busca_mulher=busca_mulher)

def todas_as_pessoas():
    with engine.connect() as con:    
        statement = text ("""SELECT * FROM Pessoa""")
        rs = con.execute(statement) 
        lista_linhas = rs.fetchall()
        resposta = []
        for linha in lista_linhas:
            resposta.append(dict(linha))
        return resposta

def localiza_pessoa(id_pessoa):
    with engine.connect() as con:    
        statement = text ("""SELECT * FROM pessoa WHERE id = :id_desejado """)
        rs = con.execute(statement, id_desejado=id_pessoa) 
        lista_linhas = rs.fetchall()
        if len(lista_linhas) == 0:
            raise NotFoundError
        return dict(lista_linhas[0])

class IncompatibleError(Exception):
    pass

#adiciona_interesse(id1,id2) : marca que 1 quer falar com 2
#consulta_interesses(id1)    : devolve a lista de todos os interesses de 1
#remove_interesse(id1,id2)   : marca que 1 não quer mais falar com 2

def adiciona_interesse(id1, id2):
    with engine.connect() as con:    
        sql_criar = '''INSERT INTO Interesse (id_interessado,id_alvo) 
        VALUES (:id_interessado,:id_alvo)'''
        con.execute(sql_criar, 
            id_interessado = id1,
            id_alvo = id2)

def consulta_interesses(id_pessoa):
    with engine.connect() as con:    
        statement = text ("""select id_alvo from Interesse where id_interessado = :id_interessado""")
        rs = con.execute(statement, id_interessado=id_pessoa) 
        lista_linhas = rs.fetchall()
        resposta = []
        for linha in lista_linhas: 
            resposta.append(dict(linha)['id_alvo']) #(3,) -dict-> {'id_alvo':3} 
            # -pegar chave id_alvo -> 3
        return resposta
    
def remove_interesse(id1, id2):
    with engine.connect() as con:
        sql_deletar = """DELETE FROM Interesse WHERE id_interessado = :id_interessado AND id_alvo = :id_alvo"""
        con.execute(sql_deletar, 
            id_interessado = id1, 
            id_alvo = id2)

def reseta():
    with engine.connect() as con:    
        statement = text ("""DELETE FROM Pessoa""")
        rs = con.execute(statement)
        statement = text ("""DELETE FROM Interesse""")
        rs = con.execute(statement)