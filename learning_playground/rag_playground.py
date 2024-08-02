# Retrieval Augmented Generation (RAG)
# all the models we are using actually have a constraint on how much knowledge they already have 
# this feature might cause problems when we have specialized documents to be processed or need real-time info 
# to overcome this aspect, you need to give these llms some additional information to help them generate better responses
# this is done through RAG
#
# Critical components when working with RAG:
# - Retriever: takes the embedded question to be compared with the embeddings of the documents in the vector store
# - Vector Store: Store embeddings 
# - Embeddings: a numerical way to represent the documents in the vector store 
# - LLM embedder: Convert text to embeddings
# - Chunks: about 1k of TOKENS, the splitted document to be converted to embeddings and vice versa
# - Tokens: the individual words or phrases that the model uses to generate responses

# examples are divided in 2 parts, as follows: 
# 1. the first one consists of the PDf or external info source process to be stored in the vector store
# 2. the second one is the actual RAG process, starting from the prompt by user up to the very last response outtput 

# 1.
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Define the directory containing the text file and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "odyssey.txt")
persistent_directory = os.path.join(current_dir, "db", "faiss_index")

# Check if the FAISS vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")
    
    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )
    
    # Try different encodings
    encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            # Read the text content from the file with specific encoding
            loader = TextLoader(file_path, encoding=encoding)
            documents = loader.load()
            print(f"Successfully loaded the file with {encoding} encoding.")
            break
        except UnicodeDecodeError:
            print(f"Failed to decode with {encoding} encoding. Trying next...")
    else:
        raise RuntimeError("Unable to decode the file with any of the attempted encodings.")

    # Split the document into chunks (there are diff chunking strategies, this is one)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200) #the chunk overlaps helps with the chunk limit, better performance reuslts: common values are 200-400 
    docs = text_splitter.split_documents(documents)
    #...or chunks, call it whatever you prefer 
    
    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")
    print(f"Sample chunk:\n{docs[0].page_content}\n")
    
    # Create embeddings (there are diff options, now we ose the OpenAIEmbeddings class )
    print("\n--- Creating embeddings ---")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"  # this is the cheapest one
    )
    print("\n--- Finished creating embeddings ---")
    
    # Create the vector store
    print("\n--- Creating vector store ---")
    db = FAISS.from_documents(docs, embeddings)
    print("\n--- Finished creating vector store ---")
    
    # Persist the vector store
    db.save_local(persistent_directory)
else:
    print("Vector store already exists. No need to initialize.")
    print(f"Persistent directory: {persistent_directory}")

#2

# Define the persistent directory
persistent_directory = os.path.join(current_dir, "db", "faiss_index")

# Define the embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load the existing vector store with the embedding function
db = FAISS.load_local(persistent_directory, embeddings)
#set allow_dangerous_deserialization: bool = True, if you want to load the vector store from a remote source

# Define the user's question
query = "Who is Odysseus' wife?"

# Retrieve relevant documents based on the query (there are different possibilities when it comes to working with retrievers )
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.4},  #returns key closest document: in this case top 3 similar results 3=3k tokens llms limit is generally around 8k  
)
relevant_docs = retriever.invoke(query)

# Display the relevant results with metadata
print("\n--- Relevant Documents ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")
    if doc.metadata:
        print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")