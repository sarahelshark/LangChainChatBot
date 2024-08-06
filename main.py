# flask imports
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS

import os
from dotenv import load_dotenv 

import constants
from models import GeminiPro

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
system_message = SystemMessage(content="You are a helpful AI assistant")
chat_history.append(system_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global chatgpt_history
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400
        
        user_message = data.get('message', '')
        model_choice = data.get('model', 'chatgpt')  # Default to ChatGPT if not specified
        
        if user_message.lower() == 'exit':
            print("---- Message History ----")
            print(chatgpt_history)
            return jsonify({'content': "Grazie per aver utilizzato l'assistente AI. Arrivederci!"})
        
        if model_choice == 'chatgpt':
            print("---- ChatGPT mode ----")
            # ChatGPT logic
            # Add user message to chat history
            chatgpt_history.append(HumanMessage(content=user_message))
            # Get AI response using history
            result = model.invoke(chatgpt_history)
            response = result.content
            # Add AI message to chat history
            chatgpt_history.append(AIMessage(content=response))
        elif model_choice == 'gemini':
            # Gemini logic
            print("---- Gemini mode ----")
            response = GeminiPro.get_response(user_message)
        else:
            return jsonify({'error': 'Invalid model choice.'}), 400
        
        return jsonify({'content': response})
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global chatgpt_history
    try:
        chatgpt_history = [system_message]
        return jsonify({'status': 'Conversation reset successfully.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    # Set up Gemini credentials
    os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
    app.run(debug=True)