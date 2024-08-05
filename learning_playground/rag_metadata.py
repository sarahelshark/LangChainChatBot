import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

# Custom TextLoader with encoding handling
class CustomTextLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings_to_try:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                print(f"Successfully loaded the file with {encoding} encoding.")
                return [Document(page_content=text, metadata={"source": os.path.basename(self.file_path)})]
            except UnicodeDecodeError:
                print(f"Failed to decode with {encoding} encoding. Trying next...")
        
        raise RuntimeError(f"Unable to decode {self.file_path} with any of the attempted encodings.")

# Define the directory containing the text files and the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
books_dir = os.path.join(current_dir, "books")
db_dir = os.path.join(current_dir, "db")

# Define the persistent directory
persistent_directory = os.path.join(current_dir, "romeo_juliet_metadata", "db", "faiss_index")

print(f"Books directory: {books_dir}")
print(f"Persistent directory: {persistent_directory}")

# Check if the FAISS vector store already exists
if not os.path.exists(persistent_directory):
    print("Persistent directory does not exist. Initializing vector store...")

    # Ensure the books directory exists
    if not os.path.exists(books_dir):
        raise FileNotFoundError(
            f"The directory {books_dir} does not exist. Please check the path."
        )

    # List all text files in the directory
    book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt")]

    # Read the text content from each file and store it with metadata
    documents = []
    for book_file in book_files:
        file_path = os.path.join(books_dir, book_file)
        #load books 
        loader = CustomTextLoader(file_path)
        book_docs = loader.load()
        for doc in book_docs:
            # Add metadata to each document indicating its source
            doc.metadata = {"source": book_file}
            documents.append(doc)
            
    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print("\n--- Document Chunks Information ---")
    print(f"Number of document chunks: {len(docs)}")

    # Create embeddings
    print("\n--- Creating embeddings ---")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    print("\n--- Finished creating embeddings ---")

    # Create the vector store and persist it
    print("\n--- Creating and persisting vector store ---")
    db = FAISS.from_documents(docs, embeddings)
    # Persist the vector store
    db.save_local(persistent_directory)
    print("\n--- Finished creating and persisting vector store ---")

else:
    print("Vector store already exists. No need to initialize.")
    print(f"Persistent directory: {persistent_directory}")
    
    
#2


# Define the persistent directory
persistent_directory = os.path.join(current_dir, "romeo_juliet_metadata", "db", "faiss_index")

# Define the embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load the existing vector store with the embedding function
db = FAISS.load_local(persistent_directory, embeddings)
#set allow_dangerous_deserialization: bool = True, if you want to load the vector store from a remote source


#define question
query = "How did Juliet Die?"

# Retrieve relevant documents based on the query
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 2, "score_threshold": 0.1},
)
relevant_docs = retriever.invoke(query)

# Display the relevant results with metadata
print("\n--- Relevant Documents ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")
    print(f"Source: {doc.metadata['source']}\n")
