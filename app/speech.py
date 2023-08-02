from fastapi import APIRouter, File, UploadFile, HTTPException
from app.config import Config
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import tempfile
from playsound import playsound
from fastapi import Form
from fastapi.responses import StreamingResponse
import io
import base64

load_dotenv()

polly_client= Config()
speechrouter = APIRouter()

@speechrouter.get('/voices')
def getAvailableVoices():
    try:
        response = polly_client.describe_voices(LanguageCode='en-US')
        selected_voices = response['Voices'][3:5]

        # Assign aliases to the selected voices
        selected_voices[0]['Name'] = 'Tolu'
        selected_voices[1]['Name'] = 'Ade'
        
        return {"voices": selected_voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching voices: {str(e)}")


@speechrouter.get('/nigeria')
def assignVoice():
    try:
        response = polly_client.describe_voices(LanguageCode='en-US')
        
        # Get the first two voices from the response
        selected_voices = response['Voices'][:2]

        # Assign aliases to the selected voices
        selected_voices[0]['Name'] = 'Rhoda'
        selected_voices[1]['Name'] = 'Ada'
        
        return {"voices": selected_voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching voices: {str(e)}")

@speechrouter.get('/hause')
def houseVoice():
    try:
        response = polly_client.describe_voices(LanguageCode='en-US')
        
        # Get the first two voices from the response
        selected_voices = response['Voices'][5:7]

        # Assign aliases to the selected voices
        selected_voices[0]['Name'] = 'Yakubu'
        selected_voices[1]['Name'] = 'Anifa'
        
        return {"voices": selected_voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching voices: {str(e)}")


@speechrouter.post('/text')
def textUpload(text_to_read: str = Form(...), voice_id: str = Form(...)):
    try:
        # Perform text-to-speech conversion using Polly
        response = polly_client.synthesize_speech(
            Text=text_to_read,
            VoiceId=voice_id,
            OutputFormat="mp3"
        )

        # Get the speech data from the response
        speech_data = response['AudioStream'].read()

        # Encode the audio data as Base64
        base64_audio_data = base64.b64encode(speech_data).decode('utf-8')

        # Return the Base64-encoded audio data
        return {"audio": base64_audio_data}

    except Exception as e:
        return {"error": str(e)}


@speechrouter.post('/pdf')


def upload_pdf(pdf_file: UploadFile = File(...)):
    # Save the uploaded PDF to a temporary file
    with open(pdf_file.filename, 'wb') as f:
        f.write(pdf_file.file.read())

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_file.filename)

    # Convert the extracted text to speech using Amazon Polly
    voice_id = 'Joanna'  # You can use any voice available in your region
    audio_file = convert_text_to_speech(extracted_text, voice_id)

    # Play the audio
    playsound(audio_file)

    # Return a response
    return {"message": "Text converted to speech and played successfully!"}

def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def convert_text_to_speech(text, voice_id):
    response = polly_client.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        OutputFormat='mp3'
    )

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
        tmp_file.write(response['AudioStream'].read())
        return tmp_file.name



@speechrouter.get('/yoruba')
def getAvailableVoices():
    response = polly_client.describe_voices(LanguageCode='en-US')
    available_voices = [
        {"label": voice['Name'], "id": voice['Id']} for voice in response['Voices']
    ]
    return {"voices": available_voices}
