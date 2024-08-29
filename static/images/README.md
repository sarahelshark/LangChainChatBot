

# E-commerce Digital Assistant with LangChain and OpenAI
---



## Overview
This project implements a digital assistant for e-commerce product descriptions and product search using Flask, LangChain, and OpenAI's GPT models. The assistant can generate product descriptions in Italian, perform translations, and help users find specific products.


---

## Setup Instructions

### 1. Virtual Environment Setup
1. **Create a virtual environment:**
   ```bash
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

### 5. Usage Instructions
- **Description Generator:**
  - Start a conversation by greeting the assistant.
  - Provide product information to generate descriptions.
  - Ask for translations of generated descriptions.
  - Type `exit` to end the conversation.
  - Use the "Reset Conversation" button to start a new chat session.

- **Product Search:**
  - Start a conversation by greeting the assistant and asking about its skills.
  - Ask the assistant to help find a specific product by description, price, or name, in a European language.
  - Type `exit` to end the conversation.
  - Use the "Reset Conversation" button to start a new chat session.

### 6. Work in Progress
- **File:** `test-integration.py`
- **Goal:** Integrate the description generator/translator and product search/purchase advice into a single application with an enhanced user interface.

### 7. Notes
- This project uses environment variables for API keys and other sensitive information. Make sure to keep your `.env` file secure and never commit it to version control.

---
