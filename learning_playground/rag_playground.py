#Retrieval Augmented Generation (RAG)
# all the models we are using actually have a constraint on how much knowledge they already have 
#  this feature might cause problems when we have specialized documents to be processed or need real-time info 
#   to overcome this aspect, you need to give these llms some additional information to help them generate better responses
#     this is done through RAG
#
# Critical components when working with RAG:
#  - Retriever: takes the embedded question to be compared with the embeddings of the documents in the vector store
#  - Vector Store: Store embeddings 
#  - Embeddings: a numerical way to represent the documents in the vector store 
#  - LLM embedder: Convert text to embeddings
#  - Chunks: about 1k of TOKENS, the splitted document to be converted to embeddings and vice versa
#  - Tokens: the individual words or phrases that the model uses to generate responses

# examples are divided in 2 parts, as follows: 
# 1. the first one consists of the PDf or external info source process to be stored in the vector store
# 2. the second one is the actual RAG process, starting from the prompt by user up to the very last response outtput 
