import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os

# Creating Recogniser() class object
recog1 = spr.Recognizer()
mc = spr.Microphone()

# Function to capture voice and recognize text
def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        audio = recog.listen(source)
        recognized_text = recog.recognize_google(audio)
        return recognized_text
    except spr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except spr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# Map user-friendly language names to language codes
language_map = {
    'Hindi': 'hi',
    'Telugu': 'te',
    'Kannada': 'kn',
    'Tamil': 'ta',
    'Malayalam': 'ml',
    'Bengali': 'bn'
}

# Get target language from the user
target_language_input = input("Enter the target language (e.g., 'Hindi', 'Telugu', 'Tamil'): ").strip()

# Check if the target language is valid
if target_language_input not in language_map:
    print(f"Invalid language: {target_language_input}. Exiting.")
else:
    target_language_code = language_map[target_language_input]

    # Capture voice and process it
    with mc as source:
        print("Speak now for language detection and translation...")
        MyText = recognize_speech(recog1, source)

    if MyText:
        print(f"Recognized Text: {MyText}")

        # Create a Translator object
        translator = Translator()

        # Detect the language of the recognized text
        detected_language = translator.detect(MyText).lang
        print(f"Detected Language: {detected_language}")

        try:
            # Ensure the 'outputs' directory exists
            if not os.path.exists('outputs'):
                os.makedirs('outputs')

            # Translate the text to the target language
            text_to_translate = translator.translate(MyText, src=detected_language, dest=target_language_code)
            translated_text = text_to_translate.text
            print(f"Translated Text in {target_language_input}: {translated_text}")

            # Generate audio for the translated text
            speak = gTTS(text=translated_text, lang=target_language_code, slow=False)
            audio_file = f"outputs/captured_voice_{target_language_input}.mp3"
            speak.save(audio_file)
            print(f"Audio saved as {audio_file}")
            os.system(f"start {audio_file}")  # For Windows; use 'open' for macOS or 'xdg-open' for Linux
        except Exception as e:
            print(f"An error occurred during translation: {e}")
    else:
        print("No speech input detected. Exiting.")