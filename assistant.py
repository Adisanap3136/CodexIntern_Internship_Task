import speech_recognition as sr
import pyttsx3
import requests
import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Capture voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return None

def get_weather(city):
    """Fetch current weather information for a given city."""
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temperature = response['main']['temp']
        description = response['weather'][0]['description']
        return f"The temperature in {city} is {temperature}°C with {description}."
    else:
        return "City not found."

def get_time():
    """Get the current time."""
    now = datetime.datetime.now()
    return now.strftime("The time is %I:%M %p")

def assistant_main():
    """Main loop for the personal assistant."""
    speak("Hello! I am your personal assistant. How can I help you?")
    while True:
        command = recognize_speech()
        if command:
            print(f"You said: {command}")
            if "weather" in command:
                speak("Which city?")
                city = recognize_speech()
                if city:
                    speak(get_weather(city))
            elif "time" in command:
                speak(get_time())
            elif "exit" in command or "quit" in command:
                speak("Goodbye! Have a nice day.")
                break
            else:
                speak("I can help with weather and time. What else would you like?")
        else:
            continue

# Run the assistant
if __name__ == "__main__":
    assistant_main()
