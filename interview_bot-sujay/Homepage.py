import streamlit as st
from secret_key import openapi_key
import os
import whisper

# Whisper model initialization
model = whisper.load_model("base")

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

st.set_page_config(page_icon='rex.png', layout='wide', page_title='Interview Preparation : Getting Started')

st.sidebar.markdown("Navigate using the options above")

if "openai_key" not in st.session_state:
    st.session_state.openai_key = openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key
llm = OpenAI()

st.title("Interview AI Tool : Getting Started")
st.header("Recommended Steps : ")

st.markdown("""\n1. Please upload your **resume** in the sidebar on your **left**.
               \n\n2. If you are applying for a specific job, please add **job description** in the text box **below**.
               \n\n3. For starters we recommend navigating to the **Introduction Round** ...
               \n\n5. Navigate to the **Interview Round** to get started with your practice interviews.\n\n""")

st.sidebar.header("Resume")
resume = st.sidebar.file_uploader(label="**Upload your Resume/CV PDF file**", type='pdf')

# Voice input for interview preparation
voice_input = st.sidebar.file_uploader("Upload your voice input for interview preparation", type=['mp3', 'wav'])

if voice_input is not None:
    audio = whisper.load_audio(voice_input)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(fp16 = False)
    result = model.transcribe(mel, options)
    st.session_state["Voice Transcription"] = result["text"]
    st.sidebar.write("Transcribed Text:", result["text"])

st.session_state["Resume Info"] = "I am a Data Analyst with experience in Machine Learning"

st.header("Job Details")

st.session_state["Job Description"] = st.text_area(label="**Write your job description here**", height=300)

