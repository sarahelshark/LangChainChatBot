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


# Prompt Template Docs:
#   https://python.langchain.com/v0.2/docs/concepts/#prompt-templateshttps://python.langchain.com/v0.2/docs/concepts/#prompt-templates
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
#PROMPT TEMPLATES are passed to the MODEL to perform a specific task or to generate a specific OUTPUT
#you might want to pass INPUTS to the prompt template 
#(how? through the replacement of the desired input values in the string interpolation of the prompt template, 
# after the method .invoke() is called)    

# PART 1: Create a ChatPromptTemplate using a template string
template = "Tell me a joke about {topic}."
prompt_template = ChatPromptTemplate.from_template(template)

print("-----Prompt from Template-----")
prompt = prompt_template.invoke({"topic": "cats"})
print(prompt)

# # PART 2: Prompt with Multiple Placeholders
template_multiple = """You are a helpful assistant.
Human: Tell me a {adjective} story about a {animal}.
Assistant:"""
prompt_multiple = ChatPromptTemplate.from_template(template_multiple)
prompt = prompt_multiple.invoke({"adjective": "funny", "animal": "panda"})
print("\n----- Prompt with Multiple Placeholders -----\n")
print(prompt)


#PART 3: Prompt with System and Human Messages (Using Tuples)
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes."),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
print("\n----- Prompt with System and Human Messages (Tuple) -----\n")
print(prompt)

# # Extra Informoation about Part 3.
# # This does work:
# messages = [
#     ("system", "You are a comedian who tells jokes about {topic}."),
#     HumanMessage(content="Tell me 3 jokes."),
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic": "lawyers"})
# print("\n----- Prompt with System and Human Messages (Tuple) -----\n")
# print(prompt)


# This does NOT work:
#messages = [
#    ("system", "You are a comedian who tells jokes about {topic}."),
#    HumanMessage(content="Tell me {joke_count} jokes."),
#]
#prompt_template = ChatPromptTemplate.from_messages(messages)
#prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
#print("\n----- Prompt with System and Human Messages (Tuple) -----\n")
#print(prompt)

#### integrate the prompt with the chat model #######################################################################################

# PART 1: Create a ChatPromptTemplate using a template string
print("-----Prompt from Template-----")
template = "Tell me a joke about {topic}."
prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({"topic": "cats"})

# Access the content of the human message in the prompt  >> se voglio 'pulire' il prompt e mi serve solo il contenuto
# human_message_content = None
# for message in prompt.messages:
#     if isinstance(message, HumanMessage):
#         human_message_content = message.content
#         break
# Print the human message content
# print("Human message content:", human_message_content)

result = model.invoke(prompt)
print(prompt, " "," Model reply :", " ", result.content)

# PART 2: Prompt with Multiple Placeholders
print("\n----- Prompt with Multiple Placeholders -----\n")
template_multiple = """You are a helpful assistant.
Human: Tell me a {adjective} short story about a {animal}.
Assistant:"""
prompt_multiple = ChatPromptTemplate.from_template(template_multiple)
prompt = prompt_multiple.invoke({"adjective": "funny", "animal": "panda"})

result = model.invoke(prompt)
print(result.content)

# PART 3: Prompt with System and Human Messages (Using Tuples)
print("\n----- Prompt with System and Human Messages (Tuple) -----\n")
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes."),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
result = model.invoke(prompt)
print(result.content)


