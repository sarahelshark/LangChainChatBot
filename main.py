import os
from dotenv import load_dotenv 
import logging
from langchain_openai import OpenAIEmbeddings

from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils.vectorization import vectorize_and_store_chat_history
from utils.vectorization import vectorize_and_store_uploaded_docs
from utils.context import create_enhanced_context
import utils.constants as constants
from models import GeminiPro
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
load_dotenv()

# initialize the Flask app
app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

# constants
current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath('./uploads')
INDEX_FOLDER = os.path.abspath('./faiss_index_uploaded_docs')     
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'txt'}

# Ensure directories exist
os.makedirs(INDEX_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize models:
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


# function to check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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

        if user_message.lower() == 'exit':
            if model_choice == 'chatgpt':
                vectorize_and_store_chat_history(chatgpt_history, 'chatgpt', openai_embeddings)
                chatgpt_history = [system_message]
            else:
                vectorize_and_store_chat_history(gemini_history, 'gemini', openai_embeddings)
                gemini_history = []
            
            return jsonify({'content': "Grazie per aver utilizzato l'assistente AI. Arrivederci!👋"})
   
        # Recupera il contesto dalle conversazioni precedenti
        context = create_enhanced_context(model_choice, openai_embeddings)

        if model_choice == 'chatgpt':
            logging.info("-------ChatGPT mode-------")  
            # Aggiungi il contesto alla cronologia della chat
            chatgpt_history.insert(1, AIMessage(content=f"Context:\n{context}"))
            chatgpt_history.append(HumanMessage(content=user_message))
            result = chatgpt_model.invoke(chatgpt_history)
            response = result.content
            chatgpt_history.append(AIMessage(content=response))
            
        elif model_choice == 'gemini':
            logging.info("-------Gemini mode-------")  
            # Aggiungi il contesto alla cronologia della chat
            gemini_history.insert(0, f"Context:\n{context}")
            logging.info(f"Gemini history after adding context: {gemini_history}")
            gemini_history.append(f"User: {user_message}")
            response = GeminiPro.get_response(f"Context:\n{context}\nUser: {user_message}")
            gemini_history.append(f"AI: {response}")
            logging.info(f"Gemini response: {response}")
            
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
        # initialization of all variables to be used
        model_type = request.args.get('model', 'chatgpt')
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 3))
        
        if model_type not in ['chatgpt', 'gemini']:
            return jsonify({'error': 'Invalid model type specified.'}), 400
        
        # set the embeddings and vectorstore based on the model type
        embeddings = openai_embeddings
        vectorstore = FAISS.load_local(f"faiss_index_{model_type}", embeddings)
    
        # Get all documents from the vector store
        all_docs = vectorstore.docstore._dict

        # Create a dictionary 
        unique_conversations = {}

        for doc_id, doc in all_docs.items():
            session_uid = doc.metadata.get("session_uid")
            session_timestamp = doc.metadata.get("session_timestamp")
            
            if session_uid not in unique_conversations:
                unique_conversations[session_uid] = {
                    "id": session_uid,
                    "content": doc.page_content,
                    "timestamp": session_timestamp
                }
        
        # Convert the dictionary to a list and sort by timestamp (newest first)
        conversations = list(unique_conversations.values())
        conversations.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Apply pagination
        paginated_conversations = conversations[offset:offset + limit]
        
        return jsonify({'conversations': paginated_conversations})
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


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # After successful upload, vectorize and store the document
            session_uid, session_timestamp = vectorize_and_store_uploaded_docs(
                app.config['UPLOAD_FOLDER'],
                INDEX_FOLDER,
                openai_embeddings
            )
            
            if session_uid and session_timestamp:
                return jsonify({
                    'message': 'File successfully uploaded and processed',
                    'session_uid': session_uid,
                    'session_timestamp': session_timestamp
                }), 200
            else:
                return jsonify({'error': 'File uploaded but processing failed'}), 500
        except Exception as e:
            return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
