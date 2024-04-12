# **WhisperAudioTranscriber**

WhisperAudioTranscriber is an asynchronous audio recording and transcription tool built using Python. It utilizes the Hugging Face API, specifically leveraging the powerful capabilities of OpenAI's Whisper model. This tool is designed to capture audio input, transcribe or translate it in real-time, and handle audio streams efficiently with asynchronous programming.

## **Features:**
- **Asynchronous Audio Recording:** Captures audio through your device's microphone using PyAudio, handling streams in an asynchronous manner to ensure non-blocking operations.
- **Transcription and Translation:** Integrates with the Whisper model to provide real-time transcription and optional translation. Note: The translation feature is currently not working properly and requires additional configuration and testing.
- **Robust Error Handling:** Includes mechanisms to handle and retry API requests in case of errors like model loading times, ensuring reliable performance even during API downtimes or slow responses.
- **Secure Authentication:** Utilizes environment variables for API tokens to ensure security and ease of configuration across different environments.

## **Usage:**

***The tool requires the specification of an output filename and supports an optional language parameter for translation. It is designed to be interruptible, allowing the user to stop recording gracefully with a signal interruption (Ctrl+C).***

To use this script, run it from the command line with the following options:

usage: speech.py [-h] -f FILENAME [-l LANGUAGE]

Async audio recorder.

options:
-h, --help show this help message and exit
-f FILENAME, --filename FILENAME
Filename to save the recording.
-l LANGUAGE, --language LANGUAGE
Language for audio translation, please use a two char country code like "en"
(optional, does not work properly).


### Example Command
```bash
python speech.py -f output.wav -l en
```

This command will start the asynchronous audio recorder, save the recording to output.wav, and attempt to translate the audio to English.

## License
This project is released under the MIT License. For more details, see the [LICENSE](LICENSE) file in this repository.
