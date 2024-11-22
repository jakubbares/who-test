import azure.cognitiveservices.speech as speechsdk
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

def real_time_speech_to_text():
    
    AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
    # Set up the subscription info
    subscription_key = AZURE_SPEECH_KEY
    service_region = AZURE_SPEECH_REGION

    # Create a Speech Config instance
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    speech_config.speech_recognition_language = "en-US"  # Set the language to English, adjust if needed

    # Configure audio input directly by device ID (device_index)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # Create the recognizer with the specified audio input device
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Define a function to handle recognition results
    def handle_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"recognized: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            print(f"recognizing: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f"NoMatch: No speech could be recognized")
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            print(f"Canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")

    # Connect event handler for recognized speech
    speech_recognizer.recognizing.connect(handle_result)
    #speech_recognizer.recognized.connect(handle_result)

    # Start continuous recognition
    print("Listening and recognizing...")
    speech_recognizer.start_continuous_recognition_async()

    # Keep the program running to listen to audio
    try:
        while True:
            pass  # Run until manually stopped
    except KeyboardInterrupt:
        # Stop recognition on exit
        print("\nStopping real-time speech recognition...")
        speech_recognizer.stop_continuous_recognition_async()


real_time_speech_to_text()