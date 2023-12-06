import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
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
from langchain.memory import ConversationBufferWindowMemory
import json
from dotenv import load_dotenv

load_dotenv()

with open('dataset.json', 'r') as file:
    data = json.load(file)

st.title("Interview Round")

category = st.selectbox("Which type of questions do you want to attempt",
                        ['Technical', 'Behavioural', 'Culture Fit'])

while category is None:
    st.markdown('Please select question category')

# if not st.session_state.openai_key:
#     st.info("Please add your API key to continue")
#     st.stop()

os.environ['OPENAI_API_KEY'] = str(os.getenv("OPENAI_API_KEY"))

chat = ChatOpenAI(temperature=0.4)

system_template_q = """You are an interviewer, asking interview questions for an entry level data analyst job. 
                You are to serve the role of a {role} and ask questions to assess abilities for the job. Ask only one 
                question

                If questions are specific make sure to provide enough context so that it can be answered thoroughly. 
                You have to chose questions from this data : {data} depending on the role you have i.e ask only 
                questions of type matching your role. Do not repeat questions.

                Provide both the question and the intent behind it

                Use this history : {history} of chat if needed, where the content of user is human messages and the 
                assistant content is previous messages generated by you.
                  """

system_message_prompt_q = SystemMessagePromptTemplate.from_template(system_template_q)

human_template_q = "{text}"
human_message_prompt_q = HumanMessagePromptTemplate.from_template(human_template_q)

chat_prompt_q = ChatPromptTemplate.from_messages([system_message_prompt_q, human_message_prompt_q])

question_chain = LLMChain(llm=chat, prompt=chat_prompt_q)

system_template_f = """Provide  an critical assessment to the response : {response} to the question  : {question} of an 
    interview.
    You can use the following steps to guide your final assessment : 

         1. Is the answer in clear, concise wording? 
         2. Is the a good attempt to answer the question? 
         2. Is the tone of the answer professional and formal? 
         3. Does the answer satisfy the intent of the question? 
         4. Is the response of sufficient depth?
         5. Does the user mention the right key words in their answer
         6. Does the answer show curiosity to learn if the answer is unknown?
         7. Is the answer of a sufficient length?

    Your response MUST contain BOTH : 

    1. First give final assessments explaining how the response can be improved.
    2. Then provide an example improved response

    Give the response a score out of 100. Be critical. Do not be afraid to give 0 if the candidate's response does not 
    satisfy the intent, is not even related to the question. Answers that are too abrupt or short should also be marked
    poorly.
                  """

system_message_prompt_f = SystemMessagePromptTemplate.from_template(system_template_f)

human_template_f = "{text}"
human_message_prompt_f = HumanMessagePromptTemplate.from_template(human_template_f)

chat_prompt_f = ChatPromptTemplate.from_messages([system_message_prompt_f, human_message_prompt_f])

feedback_chain = LLMChain(llm=chat, prompt=chat_prompt_f)

if "message" not in st.session_state:
    st.session_state.message = []
    st.session_state.action = "Next"

for message in st.session_state.message:
    if message['role'] == "feedback" or "interviewer":
        name = "assistant"
    elif message['role'] == 'user':
        name = message['role']

    with st.chat_message(message["role"]):
        st.markdown(f"{message['role']} : {message['content']}")

if inp := st.chat_input("Type here"):
    with st.chat_message("user"):
        st.markdown(inp)
    st.session_state['message'].append({'role': 'user', 'content': inp})

question = None

if st.session_state.message == [] or st.session_state.action != "Feedback":
    response = question_chain.run(role=category, data=data, history=st.session_state['message'][-3:], text=inp)

    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.action = "Feedback"
    st.session_state['message'].append({'role': 'interviewer', 'content': response})
    question = response

if st.session_state.message[-1]['role'] == "user" and st.session_state.action == "Feedback":
    feedback = feedback_chain.run(question=question, response=inp, history=st.session_state['message'][-3:], text=inp)

    with st.chat_message("assistant"):
        st.markdown(feedback)
        st.session_state.action = st.radio(label="Would you like to do?", options=["Next", "Repeat"], index=None)
    st.session_state['message'].append({'role': 'feedback', 'content': feedback})
