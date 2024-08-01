from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

# Define prompt templates (no need for separate Runnable chains)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a comedian who tells jokes about {topic}."),
        ("human", "Tell me {joke_count} jokes."),
    ]
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = prompt_template | model | StrOutputParser()
# chain = prompt_template | model  
# without the output parser we get the full result, with the output parser we get only the content

# Run the chain
result = chain.invoke({"topic": "lawyers", "joke_count": 3})

# Output
print(result)

# la Chain ottimizza il codice, rendendolo più pulito e leggibile 
# (invece che hardcoding ogni passaggio di prompt e model), 
# inoltre permette di creare un chatbot che può ricordare la 
# conversazione passata

# there are 3 ways to manage the chains flow
# 1. extended chains : consequentially
# 2. parallel chains : run tasks in parallel, at the end you can also add a merge of the results
# 3. branching chains: kick off some actions and based on the results of those actions, follow this chain path etc
