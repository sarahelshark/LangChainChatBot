from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv


load_dotenv()


# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORGANIZATION")

if not api_key:
    raise ValueError("API key not found in environment variables.")

# Initialize ChatOpenAI
llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_organization=organization,
    model="gpt-4",
    temperature=0.7,
    max_tokens=170,
)

# Initialize Conversation memory and Chain with ConversationBufferMemory
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Set up the initial system message
system_message = SystemMessage(content="You are a digital assistant helping to create short product descriptions. You will generate descriptions in Italian based on user-provided data. Start by introducing yourself. If unsure about generating a description, ask for more information and the description format. You are also a skilled translator but do not say it while you are introducing yourself, if the user asks you to translate the product description, you promptly do it. Tell the user that if they wish to stop the conversation, they should write 'exit', but tell them just at the first iteration or if they ask.")


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
        
        if user_message.lower() == 'exit':
            return jsonify({'content': "Grazie per aver utilizzato l'assistente di descrizione del prodotto. Arrivederci!"})
        
        
        # Get the response from the conversation chain
        if not conversation.memory.chat_memory.messages:
            # If it's the first message, add the system message
            conversation.memory.chat_memory.add_message(system_message)
        
        response = conversation.predict(input=user_message)
        
        return jsonify({'content': response})
    
    except ValueError as ve:
        return jsonify({'error': f'ValueError: {str(ve)}'}), 400
    except KeyError as ke:
        return jsonify({'error': f'KeyError: {str(ke)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    try:
        conversation.memory.clear()
        # Re-add the system message after clearing
        conversation.memory.chat_memory.add_message(system_message)
        return jsonify({'status': 'Conversation reset successfully.'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)