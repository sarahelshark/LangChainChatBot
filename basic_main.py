# Simple&Clean chatloop using OpenAi & LangChain, printing results directly in the console, no frontend 
# this is the core logic that will be extended in main.py (ex productDescription_deprecated.py)

from dotenv import load_dotenv 

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
load_dotenv()


#istanziare il modello per poterci interagire 
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=300, 
)

chat_history = []  # lista per memorizzare la conversazione  > step due sarà embeddare nel vector store  e implementare RAG

# Set an initial system message (optional)
system_message = SystemMessage(content="You are a helpful AI assistant.")
chat_history.append(system_message)  # Add system message to chat history

# Chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))  # Add user message

    # Get AI response using history
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))  # Add AI message

    print(f"AI: {response}")


print("---- Message History ----")
print(chat_history)
