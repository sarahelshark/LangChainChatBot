from langchain_openai import OpenAIEmbeddings
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

# Imports per la vettorializzazione
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Initialize Flask app
app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

# Inizializzazione dei modelli
chatgpt_model = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=300)
openai_embeddings = OpenAIEmbeddings()

# Initialize chat history
chatgpt_history = []
gemini_history = []
system_message = SystemMessage(content="You are a helpful AI assistant")
chatgpt_history.append(system_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global chatgpt_history
    global gemini_history
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400
        
        user_message = data.get('message', '')
        model_choice = data.get('model', 'chatgpt')  # Default to ChatGPT if not specified  

        def vectorize_and_store_chat_history(chat_history, model_type):
            # Converti la storia della chat direttamente in un unico documento di testo
            if model_type == 'chatgpt':
                full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
                embeddings = openai_embeddings
            elif model_type == 'gemini':
                full_text = "\n".join(gemini_history)
                embeddings = openai_embeddings
                
            # Dividi il testo in chunks
            text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=50)
            texts = text_splitter.split_text(full_text)
            
            # Crea e salva il vector store con FAISS
            vectorstore = FAISS.from_texts(texts, embeddings)
            vectorstore.save_local(f"faiss_index_{model_type}")
            print(f"Chat history for {model_type} vectorized and stored successfully.")
        
        if user_message.lower() == 'exit':
            if model_choice == 'chatgpt':
                vectorize_and_store_chat_history(chatgpt_history, 'chatgpt')
                chatgpt_history = [system_message]
            else:
                vectorize_and_store_chat_history(gemini_history, 'gemini')
                gemini_history = []
            
            return jsonify({'content': "Grazie per aver utilizzato l'assistente AI. Arrivederci!👋"})
   
        if model_choice == 'chatgpt':
            print("-------ChatGPT mode-------")  
            chatgpt_history.append(HumanMessage(content=user_message))
            result = chatgpt_model.invoke(chatgpt_history)
            response = result.content
            chatgpt_history.append(AIMessage(content=response))
            
        elif model_choice == 'gemini':
            print("-------Gemini mode-------")  
            # Logica per Gemini
            gemini_history.append(f"User: {user_message}")
            response = GeminiPro.get_response(f"User: {user_message}")
            gemini_history.append(f"AI: {response}")
            
        else:
            return jsonify({'error': 'Invalid model choice.'}), 400
        
        return jsonify({'content': response})
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
@app.route('/api/get_old_chats', methods=['GET'])
def get_old_chats():
    try:
        model_type = request.args.get('model', 'chatgpt')
        
        if model_type not in ['chatgpt', 'gemini']:
            return jsonify({'error': 'Invalid model type specified.'}), 400
        
        embeddings = openai_embeddings
        vectorstore = FAISS.load_local(f"faiss_index_{model_type}", embeddings)
        
        # Esegui una query generica per ottenere tutte le conversazioni
        query = "Mostra tutte le conversazioni"
        results = vectorstore.similarity_search(query, k=5)  # Recupera le top 5 conversazioni
        
        conversations = [result.page_content for result in results]
        
        return jsonify({'conversations': conversations})
    except Exception as e:
        return jsonify({'error': f'Errore nel recupero delle conversazioni: {str(e)}'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global chatgpt_history
    global gemini_history
    try:
        model_type = request.json.get('model', 'chatgpt')
        if model_type == 'chatgpt':
            chatgpt_history = [system_message]
        elif model_type == 'gemini':
            gemini_history = []
        else:
            return jsonify({'error': 'Invalid model type specified.'}), 400
           
        return jsonify({'status': f'{model_type.capitalize()} conversation reset successfully.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    # Set up Gemini credentials
    os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
    app.run(debug=True)

