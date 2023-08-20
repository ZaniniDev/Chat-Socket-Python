from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/procurar_respostas_chatbot', methods=['POST'])
def procurar_respostas_chatbot():
    data = request.json

    if not data:
        return jsonify({'error': 'Nenhum JSON recebido'}), 400
    
    identificador_aluno = data.get('identificador_aluno')
    identificador_robo = data.get('identificador_robo')
    mensagem_aluno = data.get('mensagem_aluno')
    plataforma_chatbot = data.get('plataforma_chatbot')
    tokenchatbot = data.get('tokenchatbot')

    # Aqui você pode adicionar a lógica do seu chatbot para processar os dados
    
    resposta = f"Olá, aluno {identificador_aluno}! Você disse: '{mensagem_aluno}'"

    return jsonify({'resposta_chatbot': resposta})

if __name__ == '__main__':
    app.run(debug=True)