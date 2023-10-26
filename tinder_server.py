from flask import Flask, jsonify, request
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

if __name__ == '__main__':
    app.run(host='localhost', port=5003, debug=True)
