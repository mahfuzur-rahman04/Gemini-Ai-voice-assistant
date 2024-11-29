# Gemini-Ai-voice-assistant
A voice assistant project that integrates Gemini AI and OpenWeatherMap API to create an interactive voice-based experience. The assistant can greet the user, play background music, and even ask for the user's name while using APIs for more interactive features.

# Features:
Wake-Up Tone: Plays a tone or greeting to notify the user the assistant is active.
Background Music: Plays continuous background music for ambiance.
User Interaction: Prompts the user for their name (though not used directly in the code).
Weather Info: Fetches weather data using the OpenWeatherMap API.

# Table of Contents:
1. Prerequisites
2. Installation
3. API Key Setup
4. Creating Audio Files
5. Running the Code
6. Troubleshooting

# Prerequisites:
Before you can run this project, ensure the following prerequisites are installed on your system:

###Python 3.x
pip (Python's package installer)

# Installation
## Windows:
1. Install Python:
    Download Python from the official Python website.
    During installation, make sure to check "Add Python to PATH".

2. Install Dependencies: Open Command Prompt and navigate to your project directory. Then run:

###pip install -r requirements.txt

3. Install Additional Software (for handling MP3 files):
    Install FFmpeg. This is needed for handling MP3 files in your project.

# macOS

1. Install Python:
    You can install Python using Homebrew if it's not already installed:

    brew install python

2. Install Dependencies: Open Terminal and navigate to your project directory. Then run:

    pip install -r requirements.txt

3. Install Additional Software (for handling MP3 files):

    Install FFmpeg via Homebrew:

    brew install ffmpeg

# Linux (Ubuntu/Debian)

1. Install Python: Python should be pre-installed, but if not, you can install it via:

    sudo apt-get install python3

2. Install Dependencies: Open your terminal and navigate to the project directory. Then run:

    pip install -r requirements.txt

3. Install Additional Software (for handling MP3 files): Install FFmpeg:

    sudo apt-get install ffmpeg

# API Key Setup

To connect to Gemini AI and OpenWeatherMap, you will need to create API keys for each service.
1. Gemini AI API Key:

    Visit Gemini AI to create an account.
    After signing in, generate an API key by following their API documentation.
    Store your API key securely.

2. OpenWeatherMap API Key:

    Go to OpenWeatherMap.
    Sign up for an account if you don’t have one.
    Go to the API section and generate an API key for weather data.
    Store your API key securely.

# Creating Audio Files

For the voice assistant to function, you will need three MP3 audio files:

1. 1.mp3 – This will be the "Wake-up tone" or greeting sound when the assistant is activated.
2. 2.mp3 – Background music or additional ambient sound to play while the assistant is active.
3. 3.mp3 – A prompt (optional) for asking the user’s name (though not used directly in the code).

You can create these audio files using any sound creation tool or download royalty-free sounds online. Make sure the MP3 files are named 1.mp3, 2.mp3, and 3.mp3, and are placed in your project directory.

# Running the Code

Once you have the dependencies installed, and the API keys set up, you can run the voice assistant.

 1. Set Up Environment Variables: Store your Gemini AI and OpenWeatherMap API keys in environment variables for security.

# On Windows:
"Replace the API keys with your Gemini and OpenWeatherMap keys in the provided code."

set GEMINI_API_KEY=your_gemini_api_key
set OWM_API_KEY=your_openweathermap_api_key

# On macOS/Linux:

export GEMINI_API_KEY=your_gemini_api_key
export OWM_API_KEY=your_openweathermap_api_key

2. Run the Assistant: Once the environment variables are set, run the main Python script:

    python main.py

Troubleshooting

   1. Missing Dependencies: If you get errors related to missing libraries, ensure you’ve installed all the required packages listed in requirements.txt. Run pip install -r requirements.txt again.

   2. API Key Errors: Make sure your API keys are correct. If you're getting "Invalid API Key" errors, double-check your keys and try again.

   3. MP3 File Issues: If the assistant isn't playing audio files, ensure that your MP3 files are properly named and placed in the project directory.


This README is designed to guide users through the setup process for your Gemini AI Voice Assistant project. It covers everything from installing dependencies to creating the required audio files and running the assistant.

