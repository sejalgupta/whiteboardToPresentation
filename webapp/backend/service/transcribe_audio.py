import os
from deepgram import DeepgramClient, PrerecordedOptions
from .config import DEEPGRAM_API_KEY

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

def transcribe_audio(filename: str, mimetype: str) -> str:
    print("Transcribing audio file: ", filename)
    with open(filename, 'rb') as audio:
        source = {'buffer': audio}
        options = PrerecordedOptions(
            model="nova",
            smart_format=True,
            summarize="v2",
        )
        url_response = deepgram.listen.prerecorded.v("1").transcribe_file(
            source, options
        )
        return url_response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']