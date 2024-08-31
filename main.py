from langchain_openai import OpenAIEmbeddings
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap5
from flask_cors import CORS

import os
from dotenv import load_dotenv 
import logging
from datetime import datetime

import constants
from models import GeminiPro

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
load_dotenv()

# Imports per la vettorializzazione
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import uuid
from langchain.schema import Document


# Initialize Flask app
app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

# Inizializzazione dei modelli
# Set up Gemini credentials
os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
# Set up chatgpt model
chatgpt_model = ChatOpenAI(model="gpt-4", temperature=0.7, max_tokens=300)
openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

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
            # mostra se non ci sono ancora delle conversazioni attive
            if not chat_history:
                logging.info(f"No chat history to save for {model_type}")
                return
            
            # Genera un UID per questa sessione di chat
            session_uid = str(uuid.uuid4())
            # genera un timestamp per questa sessione di chat
            session_timestamp = datetime.now().isoformat()   
            
            # Converti la storia della chat direttamente in un unico documento di testo
            if model_type == 'chatgpt':
                full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
                embeddings = openai_embeddings
            elif model_type == 'gemini':
                full_text = "\n".join(gemini_history)
                embeddings = openai_embeddings
             
            # Aggiungi un UID e timestamp al testo per differenziare le sessioni
            full_text = f"\n{full_text}"
            
            # Dividi il testo in chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
            texts = text_splitter.split_text(full_text) 
            # Crea documenti con metadati che includono l'UID della sessione
            documents = [Document(page_content=text, metadata={"session_uid": session_uid, "session_timestamp":session_timestamp}) for text in texts]
    
            # Definisci il percorso per il vector store
            index_path = f"faiss_index_{model_type}"   
            
            # Verifica se il percorso esiste
            if os.path.exists(index_path):
             # Se esiste, carica il vector store esistente e aggiungi i nuovi document
             try:
                 vectorstore = FAISS.load_local(index_path, embeddings)
                 logging.info(f"Loaded existing vector store for {model_type}")
                 vectorstore.add_documents(documents)
                 logging.info(f"Added new session (UID: {session_uid}) to existing vector store for {model_type}")
             except Exception as e:
                  print(f"Error loading or updating existing vector store: {e}")
                  print("Creating a new vector store...")
                  vectorstore = FAISS.from_documents(documents, embeddings)
                  print(f"Created new vector store for {model_type} with session UID: {session_uid}")
            else:
                 # Se non esiste, crea un nuovo vector store
                 vectorstore = FAISS.from_documents(documents, embeddings)
                 print(f"Created new vector store for {model_type} with session UID: {session_uid}")
            
            # Salva il vector store
            vectorstore.save_local(index_path)
            print(f"Chat history for {model_type} (UID: {session_uid}) vectorized and stored successfully.")
            return session_uid, session_timestamp
    
            
        
        if user_message.lower() == 'exit':
            if model_choice == 'chatgpt':
                vectorize_and_store_chat_history(chatgpt_history, 'chatgpt')
                chatgpt_history = [system_message]
            else:
                vectorize_and_store_chat_history(gemini_history, 'gemini')
                gemini_history = []
            
            return jsonify({'content': "Grazie per aver utilizzato l'assistente AI. Arrivederci!👋"})
   
        if model_choice == 'chatgpt':
            logging.info("-------ChatGPT mode-------")  
            chatgpt_history.append(HumanMessage(content=user_message))
            result = chatgpt_model.invoke(chatgpt_history)
            # result = chatgpt_model.predict(chatgpt_history) è deprecato, msg di errore:deprecation.py:139: LangChainDeprecationWarning: The method `BaseChatModel.predict` was deprecated in langchain-core 0.1.7 and will be removed in 0.3.0. Use invoke instead.
            response = result.content
            chatgpt_history.append(AIMessage(content=response))
            
        elif model_choice == 'gemini':
            logging.info("-------Gemini mode-------")  
            # Logica per Gemini
            gemini_history.append(f"User: {user_message}")
            response = GeminiPro.get_response(f"User: {user_message}")
            gemini_history.append(f"AI: {response}")
            
        else:
            return jsonify({'error': 'Invalid model choice.'}), 400
        
        return jsonify({'content': response})
    
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/delete_conversation', methods=['POST'])
def delete_conversations():
    try:
        # Estrai i dati JSON dalla richiesta
        data = request.get_json()
        model_type = data.get('model_type')
        uids_to_delete = data.get('uids_to_delete')

        # Assicurati che entrambi i parametri siano forniti
        if not model_type or not uids_to_delete:
            return {"error": "model_type and uids_to_delete are required"}, 400

        embeddings = openai_embeddings
        index_path = f"faiss_index_{model_type}"

        if not os.path.exists(index_path):
            logging.info(f"No vector store found for {model_type}")
            return {"error": f"No vector store found for {model_type}"}, 404

        # Carica il vector store esistente
        vectorstore = FAISS.load_local(index_path, embeddings)
        logging.info(f"Loaded existing vector store for {model_type}")

        # Trova gli ID da eliminare dal vector store basandoti su uids_to_delete
        ids_to_delete = []
        for doc_id, doc in vectorstore.docstore._dict.items():
            if doc.metadata.get("session_uid") in uids_to_delete:
                ids_to_delete.append(doc_id)

        if not ids_to_delete:
            logging.info("No matching documents found to delete.")
            return {"error": "No matching documents found to delete"}, 404

        # Elimina i vettori dal vector store usando gli ID
        vectorstore.delete(ids=ids_to_delete)

        # Salva il vector store aggiornato
        vectorstore.save_local(index_path)

        logging.info(f"Successfully deleted conversations with UIDs: {uids_to_delete}")
        return {"success": True}, 200

    except Exception as e:
        logging.info(f"Error during deletion process: {e}")
        return {"error": str(e)}, 500
    
@app.route('/api/get_old_chats', methods=['GET'])
def get_old_chats():
    
    try:
        model_type = request.args.get('model', 'chatgpt')
        
        if model_type not in ['chatgpt', 'gemini']:
            return jsonify({'error': 'Invalid model type specified.'}), 400
        
        embeddings = openai_embeddings
        vectorstore = FAISS.load_local(f"faiss_index_{model_type}", embeddings)
    
        # Esegui una query generica per ottenere tutte le conversazion
        query = "Mostra tutte le conversazioni"
        results = vectorstore.similarity_search(query, k=5)  # Recupera le top 5 conversazioni
        # Crea una lista di dizionari con `session_uid` come ID e `page_content` come contenuto
        conversations = []
        for result in results:
        # Cerca il session_uid originale nel documento
         session_uid = None
         session_timestamp = None
         for doc_id, doc in vectorstore.docstore._dict.items():
            if doc.page_content == result.page_content:
                session_uid = doc.metadata.get("session_uid")
                session_timestamp=doc.metadata.get("session_timestamp")
                break
        
        # Aggiungi i dati della conversazione alla lista da passare a fe 
        conversations.append({
            "id": session_uid,  # Passa `session_uid` al frontend
            "content": result.page_content,
            "timestamp": session_timestamp
        })
        
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
        logging.error(f'Unexpected error: {str(e)}')
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
