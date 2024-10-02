# Basic Digital Assistant 
***LangChain and OpenAI / Gemini***

### Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. **Activate the environment:**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

### 2. Install Dependencies
To install the project dependencies:

1. **Install Flask, Flask-CORS, and python-dotenv:**
   ```bash
   pip install flask flask-cors python-dotenv
   ```

2. **Install LangChain and OpenAI packages:**
   ```bash
   pip install langchain langchain-openai
   pip install -qU langchain-openai
   ```

3. **Upgrade pip and LangChain dependencies:**
   ```bash
   python.exe -m pip install --upgrade pip
   pip install --upgrade langchain
   ```

4. **Install additional LangChain community tools:**
   ```bash
   pip install langchain_community
   ```

### 3. Configuration
Create a `.env` file in the project root directory with the following content, replacing the placeholder values with your actual API keys:

```plaintext
OPENAI_API_KEY="your_api_key_here"
OPENAI_ORGANIZATION="your_organization_id_here"
OPENAI_PROJECT="your_open_ai_project"
SECRET_KEY="your_flask_secret_key"
```

### 4. Project Structure and Running the Applications

#### **Description Generator**
- **File:** `productDescription_deprecated.py`
- **Functionality:** Generates product descriptions in Italian and performs translations upon request.
- **Run the Application:**
  ```bash
  python productDescription_deprecated.py
  ```
- **Access:** Open a web browser and navigate to [http://localhost:5000](http://localhost:5000).

#### **Product Search**
- **File:** `searchDB_deprecated.py`
- **Functionality:** Searches for products based on user input, supports multiple European languages.
- **Database Setup:**
  - **Create the database:**
    ```bash
    python create_db.py
    ```
  - **Check if the database is populated:**
    ```bash
    python check_db.py
    ```
- **Run the Application:**
  ```bash
  python productDescription_deprecated.py
  ```
- **Access:** Open a web browser and navigate to [http://localhost:5000](http://localhost:5000).

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

