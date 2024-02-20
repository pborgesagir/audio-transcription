import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io


# Set the page configuration
st.set_page_config(
    page_title='Transcrição de áudios - SERCOM',
    layout='wide',
    page_icon="https://media.licdn.com/dms/image/C4D0BAQHXylmAyGyD3A/company-logo_200_200/0/1630570245289?e=2147483647&v=beta&t=Dxas2us5gteu0P_9mdkQBwJEyg2aoc215Vrk2phu7Bs",
    initial_sidebar_state='auto'
)

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
st.title('Transcrição de MP3 para texto')
audio_file = st.file_uploader("Faça o uploadload do arquivo em formato MP3", type=['mp3'])

if audio_file is not None:
    st.audio(audio_file, format='audio/mp3')
    if st.button('Transcreva'):
        with st.spinner('Transcrevendo...'):
            try:
                text = transcribe_audio(audio_file)
                st.success("Transcrição com sucesso 🥳")
                st.write(text)
            except Exception as e:
                st.error(f"Error during transcription: {e}")

