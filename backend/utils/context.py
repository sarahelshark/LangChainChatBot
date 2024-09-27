import logging
from datetime import datetime
import os
from langchain_community.vectorstores import FAISS
# Configura il logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def create_enhanced_context(model_type, embeddings, max_context_length=3000):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chat_index_path = os.path.join(current_dir, 'db', f'faiss_index_{model_type}')
    upload_index_path = os.path.join(current_dir, 'db', 'faiss_index_uploaded_docs')

    conversations = []

    # Load chat history vector store
    if os.path.exists(os.path.join(chat_index_path, "index.faiss")):
        try:
            chat_vectorstore = FAISS.load_local(chat_index_path, embeddings, allow_dangerous_deserialization=True)
            logging.info(f"Loaded vector store for {model_type}")
            chat_docs = chat_vectorstore.docstore._dict
            for doc_id, doc in chat_docs.items():
                session_uid = doc.metadata.get("session_uid")
                session_timestamp = doc.metadata.get("session_timestamp")
                conversations.append({
                    "content": doc.page_content,
                    "timestamp": session_timestamp
                })
        except Exception as e:
            logging.error(f"Error loading vector store for {model_type}: {str(e)}", exc_info=True)
    else:
        logging.info(f"No vector store found for {model_type}")

    # Load uploaded documents vector store
    if os.path.exists(os.path.join(upload_index_path, "index.faiss")):
        try:
            upload_vectorstore = FAISS.load_local(upload_index_path, embeddings, allow_dangerous_deserialization=True)
            logging.info(f"Loaded vector store for uploaded documents")
            upload_docs = upload_vectorstore.docstore._dict
            for doc_id, doc in upload_docs.items():
                session_uid = doc.metadata.get("session_uid")
                session_timestamp = doc.metadata.get("session_timestamp")
                conversations.append({
                    "content": doc.page_content,
                    "timestamp": session_timestamp
                })
        except Exception as e:
            logging.error(f"Error loading vector store for uploaded documents: {str(e)}", exc_info=True)
    else:
        logging.info(f"No vector store found for uploaded documents")

    # Sort conversations by timestamp in descending order
    conversations.sort(key=lambda x: x["timestamp"], reverse=True)

    # Create the context from previous conversations and uploaded documents until the length limit is reached
    context = ""
    for conversation in conversations:
        if len(context) + len(conversation["content"]) > max_context_length:
            break
        context += conversation["content"] + "\n"

    print(f"Enhanced context created with length: {len(context)}")
    logging.debug(f"Enhanced context content: {context}")
    return context