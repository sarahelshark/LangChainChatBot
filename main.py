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


#imports for vectorization 
#chatgpt & langchain imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
#gemini &  vertexai imports
#from langchain_community.embeddings import VertexAIEmbeddings deprecatedpip install -U langchain-google-vertexai
from langchain_google_vertexai import VertexAIEmbeddings
from google.auth import load_credentials_from_file
from google.cloud import aiplatform


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
chatgpt_history = []
system_message = SystemMessage(content="You are a helpful AI assistant")
chatgpt_history.append(system_message)


# Inizializzare le embeddings per Gemini
##### placeholder for Gemini embeddings
gemini_embeddings = []

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
        
        # funzione per vettorializzare e salvare la storia della chat, supporta entrambi i modelli 
        def vectorize_and_store_chat_history(chat_history, model_type):
         # Converti la storia della chat direttamente in un unico documento di testo
         if model_type == 'chatgpt':
           full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
         elif model_type == 'gemini':
             full_text = "\n".join(chat_history)
         # Dividi il testo in chunks
         text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=50)
         texts = text_splitter.split_text(full_text)
         # Crea embeddings
         embeddings = OpenAIEmbeddings() if model_type == 'chatgpt' else gemini_embeddings
         # Crea e salva il vector store
         vectorstore = FAISS.from_texts(texts, embeddings)
         #  Salva il vector store su disco con un nome specifico per il modello
         vectorstore.save_local(f"faiss_index_{model_type}")
         print(f"Chat history for {model_type} vectorized and stored successfully.")
        
        if user_message.lower() == 'exit':
            print("---- Message History ----")
            print(chatgpt_history)
            
            # Serialize each message in the history & convert to JSON  <<< non serve più
            # serialized_history = [serialize_message(msg) for msg in chatgpt_history]
            # json_gpt_data = json.dumps(serialized_history) 
            # print('chatGPT conversation history converted to json', json_gpt_data)
            
            if model_choice == 'chatgpt':
            # Vettorializza e salva la storia della chat
             vectorize_and_store_chat_history(chatgpt_history, 'chatgpt')
             chatgpt_history = [system_message]
            else:
                vectorize_and_store_chat_history(gemini_history, 'gemini')
                gemini_history = []
            
            
            return jsonify({'content': "Grazie per aver utilizzato l'assistente AI. Arrivederci!👋"})
   
                
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
            gemini_history.append(user_message)
            response = GeminiPro.get_response(user_message)
            gemini_history.append(response)
        else:
            return jsonify({'error': 'Invalid model choice.'}), 400
        
        return jsonify({'content': response})
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
# Helper function to serialize messages <<< non serve più
#def serialize_message(message):
#    return {
#        'type': type(message).__name__,
#        'content': message.content
#    }

@app.route('/api/get_old_chats', methods=['GET'])
def get_old_chats():
    try:
        model_type = request.args.get('model', 'chatgpt')
        
        # Carica il vector store appropriato
        embeddings = OpenAIEmbeddings() if model_type == 'chatgpt' else gemini_embeddings
        vectorstore = FAISS.load_local(f"faiss_index_{model_type}", embeddings)
        
        # Esegui una query generica per ottenere tutte le conversazioni
        query = "Mostra tutte le conversazioni"
        results = vectorstore.similarity_search(query, k=5)  # Recupera le top 5 conversazioni
        
        # Formatta i risultati
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
        else:
            gemini_history = []
            
        return jsonify({'status': f'{model_type.capitalize()} conversation reset successfully.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    # Set up Gemini credentials
    os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
    app.run(debug=True)