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
    