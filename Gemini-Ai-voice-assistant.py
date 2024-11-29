import datetime
import random
import os
import time
import vlc
import pygame
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import webbrowser
import wikipedia
import requests
import google.generativeai as genai
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl

# Initialize Pygame for audio playback
pygame.mixer.init()

# Global variables
current_mode = "basic"  # Start in basic mode
activationWords = ['shadow']
tts_type = 'google'  # Use 'google' or 'local'
player = None  # Global variable for the music player instance

# Configure Gemini AI API
genai.configure(api_key='********')  # Replace with actual API key
model = genai.GenerativeModel('gemini-pro')

# Class for storing person information
class Person:
    def __init__(self):
        self.name = ''

    def set_name(self, name):
        self.name = name

person_obj = Person()

# Path to the desktop and audio files
desktop_path = os.path.expanduser("~/Desktop")
audio_file_path = os.path.join(desktop_path, "1.mp3")
music_file_path = os.path.join(desktop_path, "2.mp3")
ask_name_audio_file_path = os.path.join(desktop_path, "3.mp3")

# Function to generate and save audio file for the wakeup tone
def generate_audio(text, file_path):
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)
    print(f"Audio file saved to {file_path}")

# Generate the wakeup tone if it doesn't already exist
if not os.path.isfile(audio_file_path):
    generate_audio("Hello, how can I assist you today?", audio_file_path)

# Function to play the audio file
def play_audio(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")

# Function to play additional music
def play_music(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing music: {e}")

# Function to convert text to speech and play it
def engine_speak(audio_string):
    if tts_type == 'google':
        audio_string = str(audio_string)
        print(audio_string)
        tts = gTTS(text=audio_string, lang='en')
        r = random.randint(1, 20000000)
        audio_file = f'audio{r}.mp3'
        tts.save(audio_file)

        try:
            song = AudioSegment.from_mp3(audio_file)
            play(song)
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            os.remove(audio_file)
    elif tts_type == 'local':
        # Implement local TTS if needed
        pass

# Function to record audio from the microphone
def record_audio(ask=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, duration=1.2)
        if ask:
            print(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(f"Recognized Speech: {voice_data}")  # Debugging line
        except sr.UnknownValueError:
            voice_data = None
        except sr.RequestError:
            voice_data = None
    return voice_data

# Function to check if specific terms are in the voice data
def there_exists(terms, voice_data):
    return any(term in voice_data.lower() for term in terms) if voice_data else False

# Function to get the current location based on IP address
def get_location():
    try:
        response = requests.get("http://ipinfo.io/json")
        data = response.json()
        location = data.get("city", "Unknown") + ", " + data.get("region", "Unknown") + ", " + data.get("country", "Unknown")
        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return "Unknown location"

# Function to get weather information based on location using OpenWeatherMap API
def get_weather(location):
    try:
        api_key = '********'  # Replace with actual OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location, 'appid': api_key,
            'units': 'metric'  # Use 'imperial' for Fahrenheit
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The current weather in {location} is {weather_description} with a temperature of {temperature}°C."
        else:
            return "Unable to retrieve weather information"
    except Exception as e:
        print(f"Error getting weather: {e}")
        return "Unable to retrieve weather information"

# Function to respond to commands based on current mode
def respond(voice_data):
    global player
    print(f"Received voice data: {voice_data}")  # Debugging line
    flag = 0

    if there_exists(['hey', 'hi', 'hello'], voice_data):
        greetings = ['hey, how can I help you?', 'hey, what\'s up?', 'I\'m listening', 'how can I help you?', 'hello']
        greet = random.choice(greetings)
        engine_speak(greet)
        flag = 1

    if there_exists(['what is your name', 'what\'s your name', 'tell me your name', 'who are you'], voice_data):
        engine_speak('My name is Python-Based AI Voice Assistant')
        flag = 1

    if there_exists(["what is today's date", "what day is today", "date"], voice_data):
        today = datetime.date.today()
        engine_speak(today.strftime("%B %d, %Y"))
        flag = 1

    if there_exists(["who made you", "who created you"], voice_data):
        engine_speak("I was made by Shaharaf Tanvir, Mahfuzur Rahman, and Abdul Hamid Fahim.")
        flag = 1

    if there_exists(["what is the objective of your creation", "can you clarify the purpose of your existence"], voice_data):
        engine_speak("I was developed to assist with everyday tasks, support individuals with disabilities or those who are lonely, help troubleshoot problems in emergencies, and provide entertainment.")
        flag = 1

    if there_exists(["what is today's time", "what time is it", "time"], voice_data):
        now = datetime.datetime.now()
        engine_speak(now.strftime("%I:%M:%S %p"))
        flag = 1

    if there_exists(["search for"], voice_data):
        search_term = voice_data.split("for")[-1].strip()
        url = f"https://google.com/search?q={search_term}"
        webbrowser.open(url)
        engine_speak(f"Here is what I found for {search_term} on Google")
        flag = 1

    if there_exists(["youtube", "play a song"], voice_data):
        search_term = voice_data.split("play a song", 1)[-1].strip()
        song_play(search_term)
        flag = 1

    if there_exists(["search wikipedia", "tell me about"], voice_data):
        search_term = voice_data.split("about")[-1].strip()
        try:
            definition = wikipedia.summary(search_term, sentences=2)
            engine_speak(definition)
        except wikipedia.exceptions.DisambiguationError as e:
            engine_speak(f"Your query is ambiguous. Please be more specific. Here are some options: {e.options}")
        except wikipedia.exceptions.PageError:
            engine_speak(f"Sorry, I couldn't find anything about {search_term}")
        except Exception as e:
            engine_speak(f"An error occurred: {e}")
        flag = 1

    if there_exists(["what is the weather in"], voice_data):
        location = voice_data.split("what is the weather in")[-1].strip()
        if location:
            weather_info = get_weather(location)
            engine_speak(weather_info)
            flag = 1
        else:
            engine_speak("Sorry, I didn't hear a location. Can you please specify the location?")

    if there_exists(["what is the weather today"], voice_data):
        location = get_location()
        weather_info = get_weather(location)
        engine_speak(weather_info)
        flag = 1

    if there_exists(["stop"], voice_data):
        stop_music()
        flag = 1

    if there_exists(["exit", "quit", "goodbye"], voice_data):
        engine_speak(f"Bye, thank you for using our system, {person_obj.name}")
        exit()

    if flag == 0:
        engine_speak(f"Sorry, {person_obj.name}, I did not hear you clearly. Can you please repeat?")

# Function to handle Gemini AI responses
def gemini_api(voice_data):
    print(f"Gemini API request: {voice_data}")  # Debugging line
    if there_exists(["exit", "quit", "goodbye"], voice_data):
        engine_speak(f"Bye, thank you for using our system, {person_obj.name}")
        exit()
    else:
        response = model.generate_content(f"{voice_data} - reply in a short and simple way", stream=True)
        response_note = ''
        for chunk in response:
            print(chunk.text)
            response_note += chunk.text
        engine_speak(response_note)

# Function to play a song from YouTube
def song_play(song_name):
    global player
    print(f"Searching for song: {song_name}")  # Debugging line
    videos_search = VideosSearch(song_name, limit=1)
    result = videos_search.result()

    if result['result']:
        first_video_result = result['result'][0]
        video_link = first_video_result['link']

        ydl_opts = {
            'format': 'bestaudio/best', 'quiet': True, 'extract_flat': 'audio', 'postprocessors': [{
                'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192',
            }],
            'outtmpl': '/tmp/temp_audio.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=False)
            audio_url = info_dict.get('url', None)

        if audio_url:
            try:
                player = vlc.MediaPlayer(audio_url)
                player.play()
                while player.is_playing():
                    time.sleep(1)
            except Exception as e:
                print(f"Error playing audio: {e}")
                engine_speak("Sorry, I'm having trouble playing the song.")
        else:
            engine_speak(f"Sorry, I couldn't find anything about {song_name} on YouTube.")
    else:
        engine_speak(f"Sorry, I couldn't find any results for {song_name}.")

# Function to stop the currently playing music
def stop_music():
    global player
    if player and player.is_playing():
        player.stop()
        engine_speak("Music stopped.")
    else:
        engine_speak("No music is currently playing.")

# Function to switch modes
def switch_mode(voice_data):
    global current_mode

    if 'advanced' in voice_data.lower():
        current_mode = "advanced"
        engine_speak("Switched to advanced mode.")
    elif 'basic' in voice_data.lower():
        current_mode = "basic"
        engine_speak("Switched to basic mode.")
    else:
        engine_speak("Invalid mode. Please say 'advanced mode' or 'basic mode'.")

# Main loop
if __name__ == "__main__":
    print("Listening for activation words...")
    while True:
        voice_input = record_audio(ask="Say something...")
        if there_exists(activationWords, voice_input):
            play_audio(audio_file_path)  # Play the wakeup tone
            play_music(music_file_path)  # Play additional music
            voice_data = record_audio("Listening...")
            if voice_data:
                if there_exists(["mode", "switch mode", "change mode"], voice_data):
                    print(f"Attempting to switch mode: {voice_data}")  # Debugging line
                    switch_mode(voice_data)
                else:
                    if current_mode == "advanced":
                        gemini_api(voice_data)
                    elif current_mode == "basic":
                        respond(voice_data)
                    else:
                        engine_speak("Invalid mode. Please say 'advanced mode' or 'basic mode' to switch.")
        else:
            print("Activation word not detected.")
