# LANGCHAIN x OPENAI SETUP main.py copy 
### 1. First, you need to setup the virtual environment for your project

 ```powershell
 python -m venv venv
 ```

### 2. activate the environment
 ```powershell
 .\venv\Scripts\activate
 ```

### 3. install langchain dependencies
 ```powershell
 pip install langchain langchain-openai

 %pip install -qU langchain-openai
 ```
(might need to run an upgrade e.g. 
`python.exe -m pip install --upgrade pip`)
### 4. import the langchain wrapper to your main.py and instantiate your LLm

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAi()

```
the clause we just imported is a wrapper for the openai imports.

to instantiate our model, we create a variable to the ChatOpenAI clause
 


#  FEAT DETAILS

#### Overview
This script demonstrates how to use the LangChain framework to interact with OpenAI's GPT models for creating short product descriptions in Italian. The digital assistant is set up to guide the user through the process of generating these descriptions. The script includes both a one-time API request and an interactive loop for continuous user interaction.

#### Dependencies
- `langchain_openai`: For interacting with OpenAI models via LangChain.
- `requests`: For making HTTP requests to the OpenAI API.
- `json`: For handling JSON data.
- `os`: For accessing environment variables.
- `dotenv`: For loading environment variables from a `.env` file.

#### Setup

1. **Environment Variables**: 
   Create a `.env` file in the same directory with the following keys:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   OPENAI_ORGANIZATION=<your_openai_organization>
   OPENAI_PROJECT=<your_openai_project>
   ```

2. **Loading Environment Variables**: 
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Setting Up API Key and Other Parameters**:
   ```python
   api_key = os.getenv("OPENAI_API_KEY")
   organization = os.getenv("OPENAI_ORGANIZATION")
   project = os.getenv("OPENAI_PROJECT")
   ```

#### Initial API Request

1. **Setting Up Headers**:
   ```python
   headers = {
       'Content-Type': 'application/json',
       'Authorization': f"Bearer {api_key}",
       'OpenAI-Organization': organization,
       'Project': project,
   }
   ```

2. **Creating the Request Payload**:
   ```python
   data = {
       'model': "gpt-4o",
       'messages': [
           {"role": "system", "content": "You are an Italian digital assistant helping to create short product descriptions. ..."},
           {"role": "user", "content": "I love programming."}
       ],
       'temperature': 0.5,
       'max_tokens': 200
   }
   ```

3. **Making the POST Request**:
   ```python
   response = requests.post(base_url, headers=headers, json=data)
   ```

4. **Handling the Response**:
   ```python
   if response.status_code == 200:
       response_json = response.json()
       print(response_json['choices'][0]['message']['content'])
   else:
       print('Failed to make request')
       print('Status code:', response.status_code)
       print('Response:', response.text)
   ```

#### Interactive Loop

1. **Instantiating the Model**:
   ```python
   model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
   ```

2. **Defining the Interaction Function**:
   ```python
   def interact_with_openai():
       print("OpenAI:")
       response = model.invoke([HumanMessage(content="You are an Italian digital assistant helping to create short product descriptions. ...")])
       print(response.content)
       print("")
   ```

3. **Starting the Interaction Loop**:
   ```python
   myinput = ""
   while myinput.lower() != "exit":
       print("Me:")
       myinput = input()
       print("")
   
       if myinput.lower() == "exit":
           break
   
       print("OpenAI:")
       response = model.invoke([HumanMessage(content=myinput)])
       print(response.content)
       print("")
   
   interact_with_openai()
   ```

#### Explanation of Key Components

1. **Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key for authentication.
   - `OPENAI_ORGANIZATION`: The organization ID associated with your OpenAI account.
   - `OPENAI_PROJECT`: The project ID for tracking purposes.

2. **LangChain Model Instantiation**:
   - `ChatOpenAI` is used to instantiate the model with parameters like `model`, `temperature`, `max_tokens`, and others for customizing the behavior of the model.

3. **Request Headers**:
   - The headers include content type, authorization token, organization ID, and project ID necessary for making authenticated requests to the OpenAI API.

4. **Interaction Loop**:
   - The loop allows for continuous interaction with the model. It processes user input and generates responses until the user types "exit".

5. **Response Handling**:
   - The script extracts and prints only the content of the responses from the model, omitting any metadata.


The LangChain framework simplifies the process of interacting with OpenAI's powerful models, allowing for flexible and powerful AI-driven applications.




# CONVERSATIONAL MEMORY MECHANISM
## how to make the retrieval chain work
1. maintain the ocnversation history
2. update the conversation history by appending a new user message and the model responses to that
3. pass the conversation history in each request to the model 


Conversation History: A list called conversation_history is initialized with the system message to set the context.

Interaction Loop:
The initial assistant response is generated and added to the conversation history.
The loop continues to take user inputs, appends each input to the conversation history, and sends the updated history to the model.
The model's responses are also appended to the conversation history to maintain context.
This approach ensures that the assistant retains the context of the conversation and can provide more coherent and contextually aware responses.


dopo ho deciso di implementare questo programma in un finto db di prodotti, per poi fare interagire il llm con un db 



prototipo 2 
# E-commerce Digital Assistant with LangChain and OpenAI

This project implements a digital assistant for e-commerce product descriptions using Flask, LangChain, and OpenAI's GPT models. The assistant generates product descriptions in Italian based on user input and can also perform translations.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the environment:
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install flask flask-cors python-dotenv langchain-openai
   ```

4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_ORGANIZATION=your_organization_id_here
   ```

## Project Structure

- `main.py`: Flask application with chat API endpoints
- `create_db.py`: Script to create and populate a SQLite database with sample products
- `main.js`: Client-side JavaScript for handling user interactions
- `index.html`: HTML template for the chat interface

## Running the Application

1. Create the database:
   ```
   python create_db.py
   ```

2. Start the Flask server:
   ```
   python main.py
   ```

3. Open a web browser and navigate to `http://localhost:5000` to interact with the assistant.

## Features

- Generate product descriptions in Italian
- Translate product descriptions on request
- Maintain conversation context using LangChain's ConversationChain
- Reset conversation functionality
- Integration with a SQLite database for product information

## Usage

- Start a conversation by greeting the assistant
- Provide product information to generate descriptions
- Ask for translations of generated descriptions
- Type 'exit' to end the conversation
- Use the "Reset Conversation" button to start a new chat session

## Dependencies

- Flask
- Flask-CORS
- LangChain
- OpenAI API
- SQLite3

## Note

This project uses environment variables for API keys and other sensitive information. Make sure to keep your `.env` file secure and never commit it to version control.

To use this new feature, users can ask questions like:

"Cerca prodotti con prezzo inferiore a 100 euro"
"Trova tutti i laptop nel database"
"Quali prodotti hanno una descrizione che include la parola 'wireless'?"


NEXT: 
>to create a memory chain also for the search functionality, to keep memory of the interaction just like in the 'product description' feature
> to support a wider range of languages (optimized queries)