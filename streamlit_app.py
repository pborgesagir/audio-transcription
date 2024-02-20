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

# Function to split and transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    # Convert MP3 to WAV using temporary files
    audio_segment = AudioSegment.from_file_using_temporary_files(audio_file)
    # Define the length for each split (e.g., 30 seconds)
    chunk_length_ms = 30000  # 30 seconds in milliseconds
    chunks = make_chunks(audio_segment, chunk_length_ms)
    full_text = ""
    
    for i, chunk in enumerate(chunks):
        with io.BytesIO() as audio_stream:
            chunk.export(audio_stream, format="wav")
            audio_stream.seek(0)
            with sr.AudioFile(audio_stream) as source:
                audio_data = recognizer.record(source)
                try:
                    # Transcribe audio to text for the current chunk
                    text = recognizer.recognize_google(audio_data, language='pt-BR')
                    full_text += text + " "
                except sr.UnknownValueError:
                    st.write(f"Chunk {i+1} could not be transcribed.")
                except sr.RequestError as e:
                    st.write(f"Could not request results from Google Speech Recognition service; {e}")
    return full_text

# Function to make chunks from audio_segment
def make_chunks(audio_segment, chunk_length_ms):
    """
    Splits the audio segment into smaller chunks of a specified length.
    Returns a list of audio chunks.
    """
    return [audio_segment[i:i + chunk_length_ms] for i in range(0, len(audio_segment), chunk_length_ms)]

# Streamlit app layout
st.title('Transcrição de MP3 para texto')
audio_file = st.file_uploader("Faça o upload do arquivo em formato MP3", type=['mp3'])

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


