import asyncio
import pyaudio
import wave
import requests
import argparse
import signal
import sys
import os

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
def get_api_token():
    token = os.getenv('HUGGINGFACE_API_TOKEN')
    if token is None:
        print("HUGGINGFACE_API_TOKEN environment variable is not set.")
        token = input("Please enter your Hugging Face API token: ")
    return token

headers = {"Authorization": f"Bearer {get_api_token()}"}
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_TOKEN']}"}

class AsyncAudioRecorder:
    def __init__(self):
        self.filename = None
        self.sample_rate = 48000
        self.channels = 2
        self.format = pyaudio.paInt16
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

    async def start_recording(self):
        self.frames = []
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=1024)
        print("Recording...")
        while True:
            data = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(data)
            if stop_event.is_set():
                break

    async def stop_recording(self):
        if self.stream and self.stream.is_active():
            print("Recording complete.")
            self.stream.stop_stream()
            self.stream.close()
            wf = wave.open(f"{self.filename}", "wb")
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            self.audio.terminate()

async def query(filename, language='en'):
    max_retries = 5
    attempt = 0
    while attempt < max_retries:
        with open(filename, "rb") as f:
            data = f.read()
        params = {'language': language} if language else {}
        response = requests.post(API_URL, headers=headers, data=data, params=params)
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                if 'estimated_time' in result:
                    wait_time = result['estimated_time'] + 5  # Adding some buffer time
                    print(f"Model is loading, retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Error in response: {result['error']}. Retrying in 5 seconds...")
                    time.sleep(5)
            else:
                return result
        else:
            print(f"Failed to query API: {response.status_code}. Retrying in 5 seconds...")
            time.sleep(5)
        attempt += 1
    raise Exception("Failed to obtain a successful response from the API after several attempts.")


stop_event = asyncio.Event()

async def main(filename, language=None):
    global recorder
    recorder = AsyncAudioRecorder()
    recorder.filename = filename
    await recorder.start_recording()
    await recorder.stop_recording()
    print("Querying the recorded file...")
    try:
        result = await query(filename, language)
    except:
        result = await query(filename, language)
    finally:
        result = await query(filename, language)

    print("Query Result:", result)

def signal_handler(signal, frame):
    print("Ctrl+C detected, stopping...")
    stop_event.set()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Async audio recorder.")
    parser.add_argument('-f', '--filename', required=True, help='Filename to save the recording.')
    parser.add_argument('-l', '--language', help='Language for audio translation, please use a two char country code like "en" (optional, does not work properly).')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(args.filename, args.language))
    finally:
        loop.close()
