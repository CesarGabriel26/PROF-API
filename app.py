from flask import Flask, request
from flask_cors import CORS
from g4f.client import Client

app = Flask(__name__)
CORS(app)
Gptclient = Client()

historico_conversa = []

def ask_g4t():
  response = Gptclient.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=historico_conversa
  )

  return response.choices[0].message.content

def new_mesage(content ,is_bot = False, role = ''):

  if len(historico_conversa) > 50:
    historico_conversa.pop(0)
  
  return {"role": "assistant" if is_bot else role , "content": content}

@app.route('/ask', methods=['POST'])
def ask():
    # Obter a pergunta do corpo da requisição
    data = request.get_json()
    user_question = data.get('question', '')

    if not user_question:
        return {"error": "Pergunta não fornecida."}, 400

    # Adicionar a pergunta do usuário ao histórico da conversa
    historico_conversa.append(new_mesage(user_question, is_bot=False, role='user'))

    # Obter a resposta do modelo
    resposta = ask_g4t()

    # Adicionar a resposta do bot ao histórico da conversa
    historico_conversa.append(new_mesage(resposta, is_bot=True))

    # Retornar a resposta para o cliente
    return {"response": resposta}


if __name__ == "__main__":
    app.run()
