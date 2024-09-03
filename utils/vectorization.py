import logging
from datetime import datetime
import uuid
import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

def vectorize_and_store_chat_history(chat_history, model_type, embeddings):
    if not chat_history:
        logging.info(f"No chat history to save for {model_type}")
        return None, None

    session_uid = str(uuid.uuid4())
    session_timestamp = datetime.now().isoformat()

    if model_type == 'chatgpt':
        full_text = "\n".join([f"{type(msg).__name__}: {msg.content}" for msg in chat_history])
    elif model_type == 'gemini':
        full_text = "\n".join(chat_history)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    full_text = f"\n{full_text}"

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_text(full_text)
    documents = [Document(page_content=text, metadata={"session_uid": session_uid, "session_timestamp": session_timestamp}) for text in texts]

    index_path = f"faiss_index_{model_type}"

    try:
        if os.path.exists(index_path):
            vectorstore = FAISS.load_local(index_path, embeddings)
            logging.info(f"Loaded existing vector store for {model_type}")
            vectorstore.add_documents(documents)
            logging.info(f"Added new session (UID: {session_uid}) to existing vector store for {model_type}")
        else:
            vectorstore = FAISS.from_documents(documents, embeddings)
            logging.info(f"Created new vector store for {model_type} with session UID: {session_uid}")

        vectorstore.save_local(index_path)
        logging.info(f"Chat history for {model_type} (UID: {session_uid}) vectorized and stored successfully.")
        return session_uid, session_timestamp
    except Exception as e:
        logging.error(f"Error in vectorizing and storing chat history: {e}")
        return None, None