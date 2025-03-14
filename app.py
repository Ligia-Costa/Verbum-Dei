from flask import Flask, request, render_template
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

API_ENDPOINT = 'https://bible-api.com/?random=verse/translation=almeida'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    nome = request.form.get('nome', None)

    if not nome:
        return render_template('index.html', erro="Para ter um versículo, você precisa informar seu nome!")

    response = requests.get(API_ENDPOINT)

    if response.status_code == 200:
        dados = response.json()
        versiculo_texto = dados["text"]  # Texto do versículo
        referencia = dados["reference"]  # Livro, capítulo e versículo

        # Traduzindo o texto para português se necessário
        tradutor = GoogleTranslator(source='auto', target='pt')
        versiculo_traduzido = tradutor.translate(versiculo_texto)

        return render_template('index.html', nome=nome, versiculo_texto=versiculo_traduzido, referencia=referencia)
    else:
        return render_template('index.html', erro="Erro no sistema! Não foi possível encontrar um versículo.")

if __name__ == '__main__':
    app.run(debug=True)