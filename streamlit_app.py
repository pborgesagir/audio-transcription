import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io

# Function to convert and transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with io.BytesIO() as audio_stream:
        # Convert MP3 to WAV
        audio_segment = AudioSegment.from_file_using_temporary_files(audio_file)
        audio_segment.export(audio_stream, format="wav")
        audio_stream.seek(0)
        with sr.AudioFile(audio_stream) as source:
            audio_data = recognizer.record(source)
            # Transcribe audio to text
            text = recognizer.recognize_google(audio_data, language='pt-BR')
            return text

# Streamlit app layout
st.title('MP3 to Text Transcription')
audio_file = st.file_uploader("Faça o uploadload do arquivo em formato MP3", type=['mp3'])

if audio_file is not None:
    st.audio(audio_file, format='audio/mp3')
    if st.button('Transcribe'):
        with st.spinner('Transcribing...'):
            try:
                text = transcribe_audio(audio_file)
                st.success("Transcrição Completa")
                st.write(text)
            except Exception as e:
                st.error(f"Error during transcription: {e}")

