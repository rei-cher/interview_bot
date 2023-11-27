import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from secret_key import openapi_key
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import (AIMessage,HumanMessage,SystemMessage)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

st.title("Interview Prep AI")


key = st.sidebar.text_input("OpenAI API Key ", type="password")


if not key:
    st.info("Please add your API key to continue")
    st.stop()

os.environ['OPENAI_API_KEY'] = key

chat = ChatOpenAI(temperature=0.6)

system_template = """You are an interviewer, asking interview questions for an entry level data analyst job. 
                You are to serve the role of a {role} and ask questions to assess abilities for the job. Ask only one question
                If questions are specific make sure to provide enough context so that it can be answered thoroughly. 

                You can use the following steps to create a question : 
                1. Clarify your role in the interview 
                2. What do you want to know about the person giving the interview, which is the intent of your question.
                3. Develop a question based on that intent.

                Provide BOTH the question and the intent.
                  """


system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template= "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

chain = LLMChain(llm=chat,prompt=chat_prompt)

if "message" not in st.session_state:
    st.session_state.message = []

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if inp := st.chat_input("Type here"):
    with st.chat_message("user"):
        st.markdown(inp)

    st.session_state['message'].append({'role': 'user', 'content': inp})

response = chain.run(role='Technical Interviewer', text=inp)

with st.chat_message("assistant"):
    st.markdown(response)
st.session_state['message'].append({'role': 'assistant', 'content': response})

