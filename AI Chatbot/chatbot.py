#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer
from datetime import datetime
import random
import openai
api_key = "Insert your OpenAI Playgrounds API key here"  
openai.api_key = api_key

#Technovate!

def chat_with_bot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002", 
        prompt=prompt,
        max_tokens=150  
    )
    return response.choices[0].text

# Create a chatbot instance
#chatbot = ChatBot('EmergencyBot')

# Create a new trainer for the chatbot
#trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on the English language
#trainer.train('chatterbot.corpus.english')

# Define a function to simulate emergency response
def emergency_response(user_input):
    # Check if the user's input indicates an emergency
    emergency_keywords = ['help', 'emergency', '911', 'fire', 'police', 'medical']
    for keyword in emergency_keywords:
        if keyword in user_input.lower():
            # Generate a random emergency response message
            emergency_responses = [
                "I'm contacting emergency services for you. Please stay on the line.",
                "I'm here to help. Can you please provide your location?",
                "This is an emergency. I'm alerting the appropriate authorities."
            ]
            return random.choice(emergency_responses)
    
    # If no emergency keywords are detected, provide a standard response
        else:
             user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("AI Assistant: Goodbye!")
            break
        prompt = f"You: {user_input}\nAI Assistant:"
        response = chat_with_bot(prompt)
        print("AI Assistant:", response.strip())


# Main loop for the chatbottest
