import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import whisper

# Whisper model initialization
model = whisper.load_model("base")

from secret_key import openapi_key
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_icon='rex.png', layout='wide')

st.title("Introduction Round : Getting Familiar")

# ... Existing content of the Introduction Round ...

if not st.session_state.openai_key:
    st.info("Please add your API key to continue")
    st.stop()

os.environ['OPENAI_API_KEY'] = st.session_state.openai_key
chat = ChatOpenAI(temperature=0.3)

# ... Existing logic for the introduction round ...

if "Voice Transcription" in st.session_state:
    query = st.session_state["Voice Transcription"]
    # You can now use 'query' in your chat logic as the user's input
    # Example: pass 'query' to your chat model or any other logic where it's needed


