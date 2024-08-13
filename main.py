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
from datetime import datetime

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

def vectorize_and_store_chat_history(chat_history, model_type):
    if not chat_history:
        print(f"No chat history to save for {model_type}")
        return

    if model_type == 'chatgpt':
        full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
    elif model_type == 'gemini':
        full_text = "\n".join(chat_history)
    else:
        print(f"Unknown model type: {model_type}")
        return

    # Aggiungi un timestamp al testo per differenziare le sessioni
    full_text = f"Session {datetime.now().isoformat()}\n{full_text}"

    embeddings = openai_embeddings
    text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    texts = text_splitter.split_text(full_text)

    # Carica il vector store esistente se esiste, altrimenti creane uno nuovo
    index_path = f"faiss_index_{model_type}"
    try:
        vectorstore = FAISS.load_local(index_path, embeddings)
        print(f"Loaded existing vector store for {model_type}")
    except Exception:
        vectorstore = FAISS.from_texts(texts, embeddings)
        print(f"Created new vector store for {model_type}")

    # Aggiungi i nuovi testi al vector store esistente
    vectorstore.add_texts(texts)
    vectorstore.save_local(index_path)
    print(f"Chat history for {model_type} vectorized and stored successfully.")

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
        model_choice = data.get('model', 'chatgpt')

        if user_message.lower() == 'exit':
            if model_choice == 'chatgpt' and chatgpt_history:
                vectorize_and_store_chat_history(chatgpt_history, 'chatgpt')
                chatgpt_history = [system_message]
            elif model_choice == 'gemini' and gemini_history:
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
        
        conversations = [{"id": i, "content": result.page_content} for i, result in enumerate(results)]
        
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


@app.route('/api/delete_conversation', methods=['POST'])
def delete_conversation():
    try:
        data = request.get_json()
        model_type = data.get('model', 'chatgpt')
        conversation_id = data.get('id')

        if model_type not in ['chatgpt', 'gemini']:
            return jsonify({'error': 'Invalid model type specified.'}), 400

        embeddings = openai_embeddings
        index_path = f"faiss_index_{model_type}"
        vectorstore = FAISS.load_local(index_path, embeddings)

        # Recupera tutte le conversazioni
        query = "Mostra tutte le conversazioni"
        results = vectorstore.similarity_search(query, k=vectorstore.index.ntotal)

        # Rimuovi la conversazione specificata
        if 0 <= conversation_id < len(results):
            del results[conversation_id]

            # Ricrea il vector store con le conversazioni rimanenti
            texts = [result.page_content for result in results]
            new_vectorstore = FAISS.from_texts(texts, embeddings)
            new_vectorstore.save_local(index_path)

            return jsonify({'status': 'Conversation deleted successfully.'})
        else:
            return jsonify({'error': 'Invalid conversation ID.'}), 400

    except Exception as e:
        return jsonify({'error': f'Error deleting conversation: {str(e)}'}), 500

if __name__ == '__main__':
    # Set up Gemini credentials
    os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
    app.run(debug=True)