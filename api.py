# app.py
import azure.cognitiveservices.speech as speechsdk
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

# Set up Azure Speech Configuration
subscription_key = "ccf9c92017b24dcc9f8873769a2e527c"
region = "eastus"
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
speech_config.speech_recognition_language = "en-US"

async def recognize_and_stream(websocket: WebSocket):
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    async def send_text(result):
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            await websocket.send_text(result.text)

    recognizer.recognized.connect(lambda evt: asyncio.create_task(send_text(evt.result)))
    recognizer.start_continuous_recognition()

    try:
        while True:
            # Keep the connection open to continue streaming
            await websocket.receive_text()
    except Exception as e:
        print("WebSocket connection closed:", e)
    finally:
        recognizer.stop_continuous_recognition()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await recognize_and_stream(websocket)