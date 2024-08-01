from dotenv import load_dotenv
load_dotenv()# Carica le variabili d'ambiente, l'import da classe ChatOpenAI la prende automaticamente da .env (vedi dentro base.py)
from langchain_openai import ChatOpenAI

#istanziare il modello per poterci interagire 
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=300, 
)
#questi imports + istanza del modello sono validi per tutti i successivi esempi, mi limiterò ad inserire solo il codice che cambia

##### 1 Esempio di utilizzo del modello basic ############################################################################################################
# Invoke the model with a message   - .invoke() method is used to send a message to the model and get a response
result = model.invoke("What is 81 divided by 9?")
print("Full result:")
print(result)
print("Content only:")
print(result.content)
# ... cleaner version of the previous code
query = "tell me a joke"
result = model.invoke(query)
print(result.content)


##### 2 Esempio di utilizzo del modello in una conversazione ############################################################################################################
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

#l'array messages contiene i messaggi che si scambiano tra l'utente e l'AI, quindi la conversazione tra i due
# esistono 3 tipi di messaggi: 

# SystemMessage:
#   Message for priming AI behavior, usually passed in as the FIRST of a sequenc of input messages.> the broad context for the conversation. 

# HumanMessagse:
#   Message from a human to the AI model.

# AIMessage:
#   Message from an AI.

messages = [
    SystemMessage(content="Solve the following math problems, you are a math genius!"),
    HumanMessage(content="What is 81 divided by 9?"),
    AIMessage(content="81 divided by 9 is 9."),
    HumanMessage(content="What is 10 times 5?"),
]
# Invoke the model with messages
result = model.invoke(messages)
print(f"Answer from AI: {result.content}")

#creare una conversazione e registrarla dentro messages[] è essenziale per poter sviluppare un chatbot che sia in grado di ricordare 
#la conversazione passata ed elaborare ulteriori richieste.


##### 3 REAL-TIME CONVERSATION WITH USER  ############################################################################################################
from langchain.schema import AIMessage, HumanMessage, SystemMessage
#langchain.schema instead of langchain_core.messages 

chat_history = []  # Use a list to store messages

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

##### 4 SAVING THE HISTORY OF THE ENTIRE CONVERSATION  OVER TO THE CLOUD  ############################################################################################################
#see cloud_example.py
