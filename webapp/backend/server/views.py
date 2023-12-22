from server import app
from flask import request, jsonify
from flask_cors import CORS
from service.transcribe_audio import transcribe_audio

CORS(app)

@app.route('/api/uploadAudio', methods=['POST'])
def uploadAudio():
    '''
    The api endpoint to upload audio file to the server
    '''
    if request.method != 'POST':
        return False
    
    # get the audio blob
    audio_file = request.files['audioBlob']
    print("Received audio file: ", audio_file)
    transcription = transcribe_audio(audio_file)
    print("Transcribed text: ", transcription)
    return jsonify({'transcription': transcription})