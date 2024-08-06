# flask imports
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS

import os
from dotenv import load_dotenv 

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
load_dotenv()


# Initialize Flask app
app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)


# Initialize the model
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=300, 
)

# Initialize chat history
chat_history = []
system_message = SystemMessage(content="You are a helpful AI assistant.")
chat_history.append(system_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400
        
        user_message = data.get('message', '')
        
        if user_message.lower() == 'exit':
            print("---- Message History ----")
            print(chat_history)
            return jsonify({'content': "Grazie per aver utilizzato l'assistente di descrizione del prodotto. Arrivederci!"})
        
        # Add user message to chat history
        chat_history.append(HumanMessage(content=user_message))
        
        # Get AI response using history
        result = model.invoke(chat_history)
        response = result.content
        
        # Add AI message to chat history
        chat_history.append(AIMessage(content=response))
        
        return jsonify({'content': response})
    
    except ValueError as ve:
        return jsonify({'error': f'ValueError: {str(ve)}'}), 400
    except KeyError as ke:
        return jsonify({'error': f'KeyError: {str(ke)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global chat_history
    try:
        chat_history = [system_message]
        return jsonify({'status': 'Conversation reset successfully.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)