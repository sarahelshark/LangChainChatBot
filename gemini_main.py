import os
import constants

from models import GeminiPro

                                  

if __name__ == constants.main:
    os.environ[constants.googleApplicationCredentials] = constants.alpeniteVertexai
    
    response = GeminiPro.get_response("You are a helpful AI assistant, you reply in the same language as the user.")
    # Print the response
    print("GeminiPro:")
    print(response)
    print("")
    myinput = ""
    
while myinput != "exit":
    print("Me:")
    myinput = input()
    print("")

    print("GeminiPro: ")
    response = GeminiPro.get_response(myinput)
    print(response)
    print("")
