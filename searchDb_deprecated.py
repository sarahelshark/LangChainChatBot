import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import SystemMessage
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# import sqlite3
from langdetect import detect

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORGANIZATION")

if not api_key:
    raise ValueError("API key not found in environment variables.")

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2, #risposta accurata vicina allo 0, risposta creativa va verso 1
    max_tokens=300,
    openai_api_key=api_key,
    openai_organization=organization,
)

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

system_message = SystemMessage(content="""
You are a multilingual digital assistant specializing in generating product descriptions for the users and in searching products in a connected e-commerce database. 
Your capabilities include:
1. Searching for products by name, description, or price.
2. Providing details about found products.
3. Handling requests in multiple languages related to products.

Always respond in the same language as the user's input, even when you're giving the results of your search in the italian database, in that case you'll need to translate the results in the language of the user input. If you don't understand a request, politely ask for clarification in the user's language.
To end the conversation, the user can write 'exit' in any language.
""")

db = SQLDatabase.from_uri("sqlite:///fakeEcommerce.db")

query_template = """
Given the following user request in any language, generate a SQL query to search for products in the database:
{user_input}

The schema of the 'products' table is as follows:
- id: INTEGER (primary key)
- name: TEXT
- description: TEXT
- price: NUMERIC(10, 2)
- image_url: TEXT

Guidelines for query generation:
1. For text searches in name or description, use the LIKE operator with wildcards.
   Example: WHERE description LIKE '%wireless%' OR name LIKE '%wireless%'
2. For price comparisons, use appropriate operators (<, >, =).
   Example: WHERE price < 100
3. If the user asks for all products, use: SELECT * FROM products
4. If the user specifies multiple criteria, combine them with AND/OR appropriately.
5. Use LOWER() to make the search case-insensitive.
   Example: WHERE LOWER(description) LIKE LOWER('%wireless%')
6. Always limit the results to 5 products to avoid overly long responses, but inform user how many results are left outside, and if they ask, provide the the missing results only.

Return only the SQL query, without explanations.
if there are errors in the query, please do not print the wrong query, in that case you should apologize and ask to try again in different terms.
"""

query_prompt = PromptTemplate.from_template(query_template)
query_chain = (
    {"user_input": RunnablePassthrough()}
    | query_prompt
    | llm.bind(stop=["\nHuman:", "\nAI:"])
    | StrOutputParser()
)

response_template = """
Based on the user's request:
{user_input}

And the query results:
{query_results}

Provide a response in the same language as the user's input that summarizes the search results, in the same language.
If results were found, list the products with their names, prices, and a brief description, if not specified only the name, and be ready if they ask for more details to promptly give it to them.
If no results were found, politely inform the user and suggest trying different search terms.
If there was an error executing the query, apologize to the user and ask them to try a different request.

Detected language: {detected_language}
Response:
"""

response_prompt = PromptTemplate.from_template(response_template)
response_chain = (
    {"user_input": RunnablePassthrough(), "query_results": RunnablePassthrough(), "detected_language": RunnablePassthrough()}
    | response_prompt
    | llm
    | StrOutputParser()
)

def is_search_query(text):
    search_keywords = {
        'en': ["search", "find", "look for", "where", "products", "price", "description", "contains", "includes", "with", "without", "less than", "more than", "cheap", "expensive", "similar to", "like"],
        'it': ["cerca", "trova", "cerca", "dove", "prodotti", "prezzo", "descrizione", "contiene", "include", "con", "senza", "meno di", "più di", "economico", "costoso", "simile a", "come"],
        'es': ["buscar", "encontrar", "busca", "donde", "productos", "precio", "descripción", "contiene", "incluye", "con", "sin", "menos de", "más de", "barato", "caro", "similar a", "como"],
        'fr': ["chercher", "trouver", "cherche", "où", "produits", "prix", "description", "contient", "inclut", "avec", "sans", "moins de", "plus de", "bon marché", "cher", "similaire à", "comme"],
        'de': ["suchen", "finden", "suche", "wo", "produkte", "preis", "beschreibung", "enthält", "beinhaltet", "mit", "ohne", "weniger als", "mehr als", "günstig", "teuer", "ähnlich wie", "wie"]
    }
    
    detected_lang = detect(text)
    if detected_lang not in search_keywords:
        detected_lang = 'en'  # Default to English if language not supported
    
    return any(keyword in text.lower() for keyword in search_keywords[detected_lang])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload.'}), 400
        
        user_message = data.get('message', '')
        detected_language = detect(user_message)
        
        if user_message.lower() == 'exit':
            exit_messages = {
                'en': "Thank you for using the product search assistant. Goodbye!",
                'it': "Grazie per aver utilizzato l'assistente di ricerca prodotti. Arrivederci!",
                'es': "Gracias por usar el asistente de búsqueda de productos. ¡Adiós!",
                'fr': "Merci d'avoir utilisé l'assistant de recherche de produits. Au revoir!",
                'de': "Vielen Dank, dass Sie den Produktsuche-Assistenten verwendet haben. Auf Wiedersehen!"
            }
            return jsonify({'content': exit_messages.get(detected_language, exit_messages['en'])})
        
        if is_search_query(user_message):
            query = query_chain.invoke(user_message)
            print(f"Generated SQL query: {query}")
            
            try:
                results = db.run(query)
                print(f"Query results: {results}")
                
                if not results.strip():
                    results = "No results found."
                
                response = response_chain.invoke({
                    "user_input": user_message,
                    "query_results": results,
                    "detected_language": detected_language
                })
            except Exception as e:
                print(f"Error executing query: {str(e)}")
                response = f"I'm sorry, there was an error executing the search. Could you try rephrasing your request? Error: {str(e)}"
        else:
            if not conversation.memory.chat_memory.messages:
                conversation.memory.chat_memory.add_message(system_message)
            
            response = conversation.predict(input=user_message)
        
        return jsonify({'content': response})
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    conversation.memory.clear()
    conversation.memory.chat_memory.add_message(system_message)
    return jsonify({'message': 'Conversation reset successfully'})

if __name__ == '__main__':
    app.run(debug=True)