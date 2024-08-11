
# E-commerce Digital Assistant with LangChain and OpenAI
## !!!! Important note on dependencies.txt
1. To install all the project dependencies, after having set the environment (see below), run:
   ```
   pip install -r dependencies.txt
   ```
2. The previous dependencies work only with the **legacy version** of langchain, specifically used in all the **_deprecated.py** files. 

   To access the latest version implementation (0.2x) you should change directory
 `cd ./learning_playground` and simply update the pip & langchain dependencies to the latest updates  
 - `python.exe -m pip install --upgrade pip` 
 - `pip install --upgrade langchain`

3. If any error occurs when installing the specific versions, try following the **step-by-step guide** listed below
4. you can use the ***.env_sample*** and ***gitignore_sample.txt*** simply by renaming them and replacing the secret values

 


## 1 > productDescription_deprecated.py 
This project implements a digital assistant for e-commerce product descriptions using Flask, LangChain, and OpenAI's GPT models. The assistant generates product descriptions in Italian based on user input and can also perform translations.

### Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the environment:
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`


3. Create a `.env` file in the project root with your OpenAI API key & flask SECRET_KEY :
   ```
   OPENAI_API_KEY="your_api_key_here"
   OPENAI_ORGANIZATION="your_organization_id_here"
   OPENAI_PROJECT = "your_open_ai_project"

   SECRET_KEY = "your_flask_secret_key"
   ```

### Project Structure

- `productDescription_deprecated.py`: Flask application with chat API endpoints ()
- `main.js`: Client-side JavaScript for handling user interactions
- `index.html`: HTML template for the chat interface

### Running the Application


1. Start the Flask server:
   ```
   python productDescription_deprecated.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to interact with the assistant.

### Features

- Generate product descriptions in Italian
- Translate product descriptions on request
- Maintain conversation context using LangChain's ConversationChain
- Reset conversation functionality

### Usage

- Start a conversation by greeting the assistant
- Provide product information to generate descriptions
- Ask for translations of generated descriptions
- Type 'exit' to end the conversation
- Use the "Reset Conversation" button to start a new chat session

### Dependencies

- Flask
- Flask-CORS
- LangChain
- OpenAI API

### Note

This project uses environment variables for API keys and other sensitive information. Make sure to keep your `.env` file secure and never commit it to version control.




## 2 > productDescription_deprecated.py
This project implements a digital assistant for e-commerce product search using Flask, LangChain, and OpenAI's GPT models. The setup is the same, you will just need to run the App you already used for the product description generator, after having typed 'exit' on the flask UI and started a new terminal.

1. Create the database:
   ```
   python create_db.py
   ```
2. Check if the db is populated
   ```
   python check_db.py
   ```
3. Start the Flask server:
   ```
   python productDescription_deprecated.py
   ```
4.  Open a web browser and navigate to `http://localhost:5000` to interact with the assistant.

### Project Structure

- `searchDB_deprecated.py`: Flask application with chat API endpoints ()
- `create_db.py`: Script to create and populate a SQLite database with sample products
- `check_db.py`: Script to check if the SQLite db is correctly populated
- `main.js`: Client-side JavaScript for handling user interactions
- `index.html`: HTML template for the chat interface

### Features

- Search queries from the user input
- european languages are supported
- Maintain conversation context using LangChain's ConversationChain.
- Reset conversation functionality.
- Integration with a SQLite database for product information.

## Usage

- Start a conversation by greeting the assistant and ask them what they skills are.
- Type 'exit' to end the conversation.
- ask to help you find a specific product by description, price or name, in a european language 
- Use the "Reset Conversation" button to start a new chat session.


## Dependencies

- Flask
- Flask-CORS
- LangChain
- OpenAI API
- SQLite3


## 3 > test-integration.py => work in progress
This project implements a digital assistant for e-commerce. This app will include the first two features in a single app: 

`description generator/translator + product search/purchase advice`
+ the UI will be enhanced
