from flask import Flask, jsonify, request, abort
import estrutura_interesses as i

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def ola():
    return "servidor do tinder"

@app.route("/pessoas", methods=['GET'])
def todas_pessoas():
    return i.todas_as_pessoas()

@app.route("/pessoas", methods=['POST'])
def adiciona_pessoa():
    dic_enviado = request.json
    i.adiciona_pessoa(dic_enviado)
    return "ok"

"http://localhost:5003/pessoas/1"
@app.route("/pessoas/<int:id_pessoa>", methods=['GET'])
def pessoa_por_id(id_pessoa):
    pessoa = i.localiza_pessoa(id_pessoa)
    return pessoa

# Estrutura de dados para armazenar informações
pessoas = []
interesses = {}
matches = {}

# Rota para obter a lista de todas as pessoas
@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    return jsonify(pessoas)

# Rota para adicionar uma pessoa
@app.route('/pessoas', methods=['POST'])
def add_pessoa():
    data = request.get_json()
    pessoas.append(data)
    return 'Pessoa adicionada com sucesso', 201

# Rota para obter informações de uma pessoa específica
@app.route('/pessoas/<int:pessoa_id>', methods=['GET'])
def get_pessoa(pessoa_id):
    for pessoa in pessoas:
        if pessoa['id'] == pessoa_id:
            return jsonify(pessoa)
    abort(404)  # Pessoa não encontrada, retorna 404

# reseta a lista de pessoas
@app.route('/reseta', methods=['POST'])
def reseta_pessoas():
    pessoas.clear()
    return 'Lista de pessoas resetada com sucesso', 200

# Rota para sinalizar interesse em outra pessoa
@app.route('/sinalizar_interesse/<int:pessoa_id1>/<int:pessoa_id2>', methods=['PUT'])
def sinalizar_interesse(pessoa_id1, pessoa_id2):
    if pessoa_id1 not in interesses:
        interesses[pessoa_id1] = []
    interesses[pessoa_id1].append(pessoa_id2)
    return 'Interesse registrado com sucesso', 201

# Rota para remover interesse em outra pessoa
@app.route('/sinalizar_interesse/<int:pessoa_id1>/<int:pessoa_id2>', methods=['DELETE'])
def remover_interesse(pessoa_id1, pessoa_id2):
    if pessoa_id1 in interesses and pessoa_id2 in interesses[pessoa_id1]:
        interesses[pessoa_id1].remove(pessoa_id2)
        return 'Interesse removido com sucesso', 200
    abort(404)  # Pessoa ou interesse não encontrados, retorna 404

# Rota para obter lista de interesses de uma pessoa
@app.route('/interesses/<int:pessoa_id>', methods=['GET'])
def get_interesses(pessoa_id):
    if pessoa_id in interesses:
        return jsonify(interesses[pessoa_id])
    abort(404)  # Pessoa não encontrada, retorna 404

# Rota para obter lista de matches de uma pessoa
@app.route('/matches/<int:pessoa_id>', methods=['GET'])
def get_matches(pessoa_id):
    if pessoa_id in interesses:
        matches[pessoa_id] = [pessoa for pessoa in interesses[pessoa_id] if pessoa in interesses and pessoa_id in interesses[pessoa]]
        return jsonify(matches[pessoa_id])
    return jsonify([])

if __name__ == '__main__':
    app.run(host='localhost', port=5003, debug=True)
