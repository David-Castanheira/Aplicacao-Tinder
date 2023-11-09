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

def adiciona_pessoa(dic_pessoa):
    with engine.connect() as con:    
        sql_criar = '''INSERT INTO Pessoa (id,nome,sexo, busca_homem, busca_mulher) 
                                   VALUES (:id,:nome,:sexo,:busca_homem,:busca_mulher)'''
        sexo = dic_pessoa.get("sexo")
        if sexo == "mulher":
            sexo = "M"
        if sexo == "homem":
            sexo = "H"
        buscando = dic_pessoa.get("buscando",[])
        busca_homem = ("homem" in buscando)
        busca_mulher = ("mulher" in buscando)
        con.execute(sql_criar, nome=dic_pessoa['nome'], id=dic_pessoa['id'], 
                               sexo=sexo, busca_homem=busca_homem, busca_mulher=busca_mulher)
# Versão mais complexa
# def todas_as_pessoas():
#     with engine.connect() as con:    
#         statement = text ("""SELECT * FROM Pessoa""")
#         rs = con.execute(statement) 
#         lista = []
#         while (True): 
#             pessoa = rs.fetchone()
#             if pessoa == None:
#                 break
#             lista.append(dict(pessoa))
#         return lista

# Versão mais simples
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
        statement = text ("""SELECT * FROM Pessoa WHERE id = :id_desejado""")
        rs = con.execute(statement, id_desejado = id_pessoa)
        lista_linhas = rs.fetchall()
        return dict(lista_linhas[0])

class IncompatibleError(Exception):
    pass

       
    

def reseta():
    with engine.connect() as con:    
        statement = text ("""DELETE FROM Pessoa""")
        rs = con.execute(statement)
        statement = text ("""DELETE FROM Interesse""")
        rs = con.execute(statement)
    




