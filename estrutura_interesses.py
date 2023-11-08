database = {} #um dicionário, que tem a chave interesses para o controle
#dos interesses (que pessoa se interessa por que outra), e pessoas para o controle de pessoas (quem sao as pessoas e quais sao os dados pessoais de cada pessoa no sistema)
#voce pode controlar as pessoas de outra forma se quiser, nao precisa mudar nada
#do seu código para usar essa váriavel
database['interesses'] = { 
    100: [101, 102, 103],
    200: [100]
}

database['PESSOA'] = [] #esse voce só faz se quiser guardar nessa lista os dicionários das pessoas

#em todo esse codigo que estou compartilhando, as variaveis interessado, alvo de interesse, pessoa, pessoa1 e pessoa2 sao sempre IDs de pessoas
class  IncompatibleError(Exception):
    pass

class NotFoundError(Exception):
    pass

class AlreadyRegistered(Exception):
    pass

def todas_as_pessoas():
    return database['PESSOA']

def adiciona_pessoa(dic_pessoa):
    database['PESSOA'].append(dic_pessoa)
    id_pessoa = dic_pessoa['id']
    database['interesses'][id_pessoa] = []

def localiza_pessoa(id_pessoa):
    for dic_pessoa in database['PESSOA']:
        if dic_pessoa['id'] == id_pessoa:
            return dic_pessoa
    raise NotFoundError
    
def reseta():
    database['PESSOA'] = []
    database['interesses'] = {}

def adiciona_interesse(id_interessado, id_alvo_de_interesse):
    pessoa1 = localiza_pessoa(id_interessado)
    pessoa2 = localiza_pessoa(id_alvo_de_interesse)
    
    if 'buscando' in pessoa1:
        if  pessoa2['sexo'] in pessoa1['buscando'] :
            database['interesses'][id_interessado].append(id_alvo_de_interesse)
        else:
            raise IncompatibleError
    else:
        database['interesses'][id_interessado].append(id_alvo_de_interesse)

    # if id_alvo_de_interesse not in database['interesses'][id_interessado]:
    #     database['interesses'][id_interessado].append(id_alvo_de_interesse)

def consulta_interesses(id_interessado):
   localiza_pessoa(id_interessado)
   return database['interesses'][id_interessado]
    
def remove_interesse(id_interessado,id_alvo_de_interesse):
    localiza_pessoa(id_interessado)
    localiza_pessoa(id_alvo_de_interesse)
    database['interesses'][id_interessado].remove(id_alvo_de_interesse)

#essa funcao diz se o 1 e o 2 tem match. (retorna True se eles tem, False se não)
#ela não está testada, só existe para fazer aquecimento para a próxima

def verifica_match(id1,id2):
    return True if id1 in database['interesses'][id2] and id2 in database['interesses'][id1] else False

    # isMatch = True
    # if id2 in database['interesses'][id1] and id1 in database['interesses'][id2]:
    #     return isMatch
    # else:
    #     return not isMatch
      
def lista_matches(id_pessoa):
    # 1° passo: Gera cada um dos matches e verifica se são correspondidos
    # 2° passo: Gera a lista de matches do id_pessoa, como [10, 20, 30]
    # 3° passo: Verifica se o id_pessoa está na lista do [10, 20, 30]
    
    lista_likes = consulta_interesses(id_pessoa)
    lista_matches = []
    for pessoa_receptora_match in lista_likes:
        likes_pessoa_fornecedora = consulta_interesses(pessoa_receptora_match)
        if id_pessoa in likes_pessoa_fornecedora:
            lista_matches.append(pessoa_receptora_match)
    return lista_matches

    # Tentativa de outra solução
    # listaMatches = {}
    # for pessoa in database['PESSOA']:
    #     listaMatches[pessoa['id']] = []
    # for id_pessoa in database['interesses']:
    #     for id_pessoa2 in id_pessoa:
    #         if verifica_match(id_pessoa, id_pessoa2):
    #             listaMatches[id_pessoa].append(id_pessoa2)
    # return listaMatches