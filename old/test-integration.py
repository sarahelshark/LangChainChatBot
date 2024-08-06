from dotenv import load_dotenv
import os
# Carica le variabili d'ambiente
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage, trim_messages, AIMessage
#from langchain_community.chains import ConversationChain deprecato!!! preferire from langchain_core.chat_history import (BaseChatMessageHistory,InMemoryChatMessageHistory,)
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Configura l'API di OpenAI
api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORGANIZATION")
# Verifica che l'API key sia stata impostata
if not api_key:
    raise ValueError("OPENAI_API_KEY non trovato nell'ambiente")


#istanziare il modello 
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=300,
    openai_api_key=api_key,
    openai_organization=organization,
)


memory = ConversationBufferMemory()
#conversation = ConversationChain(model=model, memory=memory, verbose=True)
from langchain_core.chat_history import (
    BaseChatMessageHistory, #Abstract base class for storing chat message history.
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(model, get_session_history)

#We now need to create a config that we pass into the runnable every time. This config contains information that is not part of the input directly, but is still useful. In this case, we want to include a session_id. This should look like:
config = {"configurable": {"session_id": "abc2"}}
response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Bob")],
    config=config,
)

print(response.content )

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)
print(response.content )



#https://python.langchain.com/v0.2/docs/tutorials/chatbot/ Right now, all we've done is add a simple persistence layer around the model. We can start to make the more complicated and personalized by adding in a prompt template.


trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

trimmer.invoke(messages)
print(messages)

#Prompt Templates help to turn raw user information into a format that the model can work with.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.  Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="what math problem did i ask")],
        "language": "English",
    }
)
print(response.content)

response = chain.invoke(
    {"messages": [HumanMessage(content="hi! I'm bob")], "language": "Spanish"}
)

print(response.content)

response = chain.invoke(
    {"messages": [HumanMessage(content="Can you tell me a joke")], "language": "French"}
)

print(response.content)


   