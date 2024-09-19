import logging
from datetime import datetime
import uuid
import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader

# helpers for vectorization functions
def generate_session_info():
    session_uid = str(uuid.uuid4())
    session_timestamp = datetime.now().isoformat()
    return session_uid, session_timestamp

def split_text_into_documents(full_text, session_uid, session_timestamp):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_text(full_text)
    documents = [Document(page_content=text, metadata={"session_uid": session_uid, "session_timestamp": session_timestamp}) for text in texts]
    return documents

def handle_vectorstore(index_path, documents, embeddings, model_type, session_uid, session_timestamp):
    try:
        # Verifica e crea la cartella dell'indice se non esiste
        if not os.path.exists(index_path):
            os.makedirs(index_path, exist_ok=True)
            logging.info(f"Created directory for {model_type} vector store at {index_path}")

        if os.path.exists(index_path):
            vectorstore = FAISS.load_local(index_path, embeddings)
            logging.info(f"Loaded existing vector store for {model_type}")
            vectorstore.add_documents(documents)
            logging.info(f"Added new session (UID: {session_uid}) to existing vector store for {model_type}")
        else:
            vectorstore = FAISS.from_documents(documents, embeddings)
            logging.info(f"Created new vector store for {model_type} with session UID: {session_uid}")

        vectorstore.save_local(index_path)
        logging.info(f"Data for {model_type} (UID: {session_uid}) vectorized and stored successfully.")
        return session_uid, session_timestamp
    except Exception as e:
        logging.error(f"Error in vectorizing and storing data: {e}")
        return None, None

# /helpers for vectorization functions

# vectorization functions
def vectorize_and_store_chat_history(chat_history, model_type, embeddings):
    if not chat_history:
        logging.info(f"No chat history to save for {model_type}")
        return None, None

    session_uid, session_timestamp = generate_session_info()

    if model_type == 'chatgpt':
        full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
    elif model_type == 'gemini':
        full_text = "\n".join(chat_history)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    full_text = f"\n{full_text}"
    documents = split_text_into_documents(full_text, session_uid, session_timestamp)
    
    index_path = f"faiss_index_{model_type}"
    
    # Creazione della cartella per l'indice vettoriale se non esiste
    if not os.path.exists(index_path):
        os.makedirs(index_path, exist_ok=True)
        
    return handle_vectorstore(index_path, documents, embeddings, model_type, session_uid, session_timestamp)

def vectorize_and_store_uploaded_docs(upload_folder, index_folder, embeddings):
    if not os.path.exists(upload_folder):
        logging.error(f"Upload folder does not exist: {upload_folder}")
        return

 # Creazione della cartella per l'indice se non esiste
    index_path = os.path.join(index_folder)
    if not os.path.exists(index_path):
        os.makedirs(index_path, exist_ok=True)
        logging.info(f"Created directory for uploaded documents at {index_path}")

    documents = []

    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            if filename.endswith('.txt'):
                loader = TextLoader(file_path,encoding=None)
            elif filename.endswith('.csv'):
                loader = CSVLoader(file_path)
            elif filename.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                logging.warning(f"Unsupported file type: {filename}")
                continue

            doc = loader.load()
            documents.extend(doc)
        except Exception as e:
            logging.error(f"Error processing file {filename}: {str(e)}")

    if not documents:
        logging.info("No documents to process")
        return

    session_uid, session_timestamp = generate_session_info()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    for doc in texts:
        doc.metadata["session_uid"] = session_uid
        doc.metadata["session_timestamp"] = session_timestamp

    return handle_vectorstore(index_path, texts, embeddings, 'uploaded_docs', session_uid, session_timestamp)

# /vectorization functions