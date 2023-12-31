import speech_recognition as sr
import pyttsx3
import random
import requests

# OpenAI API details
OPENAI_API_KEY = ""  # Replace with your OpenAI API key
OPENAI_API_URL = "https://api.openai.com/v1/engines/davinci/completions"

# Initialize the speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to generate a friendly response
def generate_response():
    responses = [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Hey, ready to help! What do you need?"
    ]
    return random.choice(responses)

# Function to handle commands
def handle_command(command):
    if "hello" in command:
        speak("Hi there! How can I help you?")
    elif "how are you" in command:
        speak("I'm just a program, but I'm doing great! Thanks for asking.")
    elif "thank you" in command:
        speak("You're welcome!")
    else:
        response = get_chatbot_response(command)
        speak(response)

# Function to interact with the ChatGPT API
def get_chatbot_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 50
    }
    response = requests.post(OPENAI_API_URL, json=data, headers=headers)

    try:
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0 and 'text' in response_json['choices'][0]:
            return response_json['choices'][0]['text'].strip()
        else:
            print("Unexpected response format:")
            print(response_json)
            return "Sorry, I couldn't generate a response at the moment."
    except Exception as e:
        print(f"Error handling response: {e}")
        return "Sorry, I encountered an error while generating a response."

# Function to listen to user input with a waking word
def listen():
    while True:
        with sr.Microphone() as source:
            print("Listening for 'Hey Assistant'...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            if "hey assistant" in command:
                speak(generate_response())  # Greet the user
                print("Now listening for queries...")
                break
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Request error: {e}")

    # Listen for queries continuously
    while True:
        with sr.Microphone() as source:
            print("Listening for queries...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            handle_command(command)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Request error: {e}")

if __name__ == "__main__":
    listen()
