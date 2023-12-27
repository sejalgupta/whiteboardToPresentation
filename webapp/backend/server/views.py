import os
from server import app
from flask import request, jsonify
from flask_cors import CORS
from service.transcribe_audio import transcribe_audio
from service.presentation.presentation_converter import create_presentation

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORS(app)

@app.route('/api/uploadAudio', methods=['POST'])
def uploadAudio():
    '''
    The api endpoint to upload audio file to the server
    '''
    if request.method != 'POST':
        return False
    
    print("Form data:", request.form)
    topic = request.form.get('topic', '')
    if topic == '':
        topic = 'multiplying_fractions'
    role = request.form.get('role', '')
    if role == '':
        role = 'teacher for sixth grade math'
    text_context = request.form.get('text_context', '')
    if text_context == '':
        text_context = 'I am trying to teach about multiplying fractions. I need to create a lesson plan for tomorrow.'
    presentation_length = request.form.get('length', '', type=int)
    if presentation_length == '':
        presentation_length = 10
    
    # get the audio blob. TODO: pass the audio blob to deepgram without saving it to server
    if "audioBlob" in request.files:
        audio_file = request.files['audioBlob']
        audio_file.save(audio_file.filename)
        transcription = transcribe_audio(audio_file.filename, "audio/webm")
        print("Transcribed text: ", transcription)
    else:
        transcription = ""
        print("No audio file uploaded. Using empty string as transcription.")

    relative_file_path = f"static/out/{topic}.pptx"
    pres_save_path = os.path.join(ROOT_DIR, relative_file_path)
    # TODO: the transcription is not being used in the create_presentation function yet
    create_presentation(topic, role, text_context, transcription, presentation_length, pres_save_path)
    return jsonify({
        'transcript': transcription,
        'presentation': relative_file_path
    })