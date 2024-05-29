from conversation.speech_to_text import listen
from conversation.text_to_speech import speak
from llms_connectors.openai_connector import get_openai_client, chat
from google_calendar_api.read_calendar import read_calendar
from utils.read_params import read_params
from conversation.text_to_text import agentic_answer

"""
   Current issues:
   1. Long latency
   2. Appointments are suggested even though they are not long enough for the treatment 
   3. Sometimes the mike doesnt turn off and Listening goes on forever
"""

if __name__ == "__main__":
    parameters = read_params()
    
    print(parameters['prompts']['welcome_message'])
    speak(parameters['prompts']['welcome_message'])
    
    # Initial conversation history for the OpenAI model
    conversation_history = [
        {"role": "system", 
        "content": parameters["prompts"]["conversation_initial_prompt"]}
    ]
    user_data = {}

    openai_client = get_openai_client()

    while True:
        user_input = listen()
        if user_input:
            Sandra_response = agentic_answer(conversation_history, user_input, openai_client)
            # Print the last message in conversation which is supposed to be SAndra's. 
            print(f"Sandra: {Sandra_response}")
            speak(Sandra_response)
            
            if Sandra_response == "End conversation":
                break
        