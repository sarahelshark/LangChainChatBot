import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

project_id = "alpenite-vertexai"
location = "us-central1"
vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-pro")
chat = model.start_chat(response_validation=False)

def get_response(prompt: str) -> str:
  
  def get_chat_response(chat: ChatSession, prompt: str)-> str:
      try:
        response = chat.send_message(prompt)
        return response.text
      except Exception as e:
        print(f"An error occurred: {e}")
        return 'skip'

  return get_chat_response(chat, prompt)

