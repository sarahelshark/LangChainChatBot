# ***Dev Guide __ Basic Digital Assistant***

***LangChain and OpenAI / Gemini***

### Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the environment:
   ```
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
   ```
3. Create a `.env` file in the project root with your OpenAI API key & flask SECRET_KEY :
   ```
   OPENAI_API_KEY="your_api_key_here"
   OPENAI_ORGANIZATION="your_organization_id_here"
   OPENAI_PROJECT = "your_open_ai_project"

   SECRET_KEY = "your_flask_secret_key"
   ```
### dependencies.txt
1. To install all the project dependencies, after having set the environment (previous paragraph), run:
   ```
   pip install -r dependencies.txt
   ```
3. If any error occurs when installing the specific versions, try following the **step-by-step guide** listed below.
4. You can use the ***.env_sample*** and ***gitignore_sample.txt*** simply by renaming them and replacing the secret values
5. You can use ***your-credentials.json*** to fill it with your vertexAi secret values, and finally rename it 

### Project Structure (Backend folder)

- `main.js`: Client-side JavaScript for handling user interactions
- `index.html`: HTML template for the chat interface
- `main.py`: Server-side Python script for handling API requests
- `utils/`:
  - `context.py`: Functions for creating enhanced context from chat history & uploaded documents
  - `vectorization.py`: Functions for vectorizing and storing chat history and uploaded documents
  - `helpers.py`: Helper functions for session management and text splitting (to be implemented)
- `faiss_index_chatgpt/`: Directory for storing FAISS index files for ChatGPT
- `faiss_index_gemini/`: Directory for storing FAISS index files for Gemini
- `faiss_index_uploaded_docs/`: Directory for storing FAISS index files for uploaded documents
- `uploads/`: Directory for storing uploaded documents

### Running the Application
1. python main.py
2. Open the development server directly from the terminal (e.g.`http://localhost:5000`) to interact with the assistant.

### Features
- Basic chatbot interaction
- Reset of conversation
- Memory of the conversations in a vector store & retrieval augmented generation
- Reset conversation functionality
- Delete conversation
- Upload of .pdf, .txt, . csv files, enhancing the context of the llm

### Usage
- Start a conversation by greeting the assistant
- Type 'exit' to end the conversation and store it with a session uid and timestamp
- Use the "Reset Conversation" button to start a new chat session, the conversation is not saved
- Switch between the chatGPT and gemini models
- Easily delete the undesired conversations both visually and on the vector store by clicking on the X button 
- Upload short documents (.pdf, .txt, . csv files), in order to generate more accurate responses

### Dependencies
- Flask
- Flask-CORS
- LangChain
- OpenAI API

### Note
This project uses environment variables for API keys and other sensitive information. Make sure to keep your `.env`, `.json` file secure and ***never*** commit it to version control.

