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

with open('dataset.json', 'r') as file:
    data = json.load(file)
    data = data[0:4]

st.title("Warm Up Round : Getting Comfortable with the Interview")

category = st.selectbox("Which type of questions do you want to practice?",
                        ['Technical', 'Behavioural', 'Culture Fit'])

while category is None:
    st.markdown('Please select question category')

if not st.session_state.openai_key:
    st.info("Please add your API key to continue")
    st.stop()

os.environ['OPENAI_API_KEY'] = st.session_state.openai_key

chat = ChatOpenAI(temperature=0.6)

memory = ConversationBufferMemory()

choose_question_template = """ Based on the action : {action} , choose a question from this 
"""

system_template_q = """You are to serve as the practice round before an interview. You are to assist the candidate get 
                comfortable with the interview format and type of questions.

                You are to serve the role of a {role} and ask questions to assess abilities for the job. Ask only one 
                question.

                The questions are to be chosen from this data : {data}

                It is essential that , if the action : {action} is "Next" , provide a  question you haven't given yet.
                If the action : {action} is "Repeat" , prompt the user to try to improve their response of the most     
                recent question.

                Use friendly language informing the user that this is just a warm up round 
                so they can feel free to make mistakes and learn from them.

                Provide both the question and the intent behind it. Also provide the {action}

                Use this history : {history} of chat if needed, where Human Messages are by the user and AI messages are   
                previous messages by the interviewer.

                You should think of the following before providing the response :
                1. What is the action?
                2. If the action is Repeat, what was the last/most recent interview question asked to the user?
                3. If the action is Next , make sure that you don't repeat the last question.


                  """

system_message_prompt_q = SystemMessagePromptTemplate.from_template(system_template_q)

human_template_q = "{text}"
human_message_prompt_q = HumanMessagePromptTemplate.from_template(human_template_q)

chat_prompt_q = ChatPromptTemplate.from_messages([system_message_prompt_q, human_message_prompt_q])

question_chain = LLMChain(llm=chat, prompt=chat_prompt_q)

system_template_f = """Provide an assessment to the response : {response} to the question  : {question} of an 
    interview.
    You can use the following steps to guide your final assessment : 
     1. What does the interviewee want to know about the candidate from the question i.e. the intent behind the question
     2. Compare the user's response to the ideal response/ it's ability to satisfy the intent of questions 
     3. Look for important keywords
     4. Figure out the pros and cons about the response.
     5. Is the response of sufficient depth? 

    Your response MUST provide the user tips on how they can improve their response, and a couple of improved responses 
    to help them better understand.

    Your role is to be a helpful assistant to provide useful tips to the user for them to improve their responses. Address  
    the user themselves in your response so it feels like a personal , friendly conversation. 

    Give a compact and precise response, preferably in bullet points so it is easy for the user to digest

                  """

system_message_prompt_f = SystemMessagePromptTemplate.from_template(system_template_f)

human_template_f = "{text}"
human_message_prompt_f = HumanMessagePromptTemplate.from_template(human_template_f)

chat_prompt_f = ChatPromptTemplate.from_messages([system_message_prompt_f, human_message_prompt_f])

feedback_chain = LLMChain(llm=chat, prompt=chat_prompt_f)

if "warmup_message" not in st.session_state:
    st.session_state.warmup_message = []
    st.session_state.action = "Next"

if "history" not in st.session_state:
    st.session_state.history = []

if "questions" not in st.session_state:
    st.session_state.questions = []

for message in st.session_state.warmup_message:
    if message['role'] == "user":
        name = "user"
        avatar = None
    else:
        name = "assistant"
        avatar = "rex.png"

    with st.chat_message(name, avatar=avatar):
        st.markdown(f"{message['content']}")

if inp := st.chat_input("Type here"):
    with st.chat_message("user"):
        st.markdown(inp)
    st.session_state['warmup_message'].append({'role': 'user', 'content': inp})

question = None

if st.session_state.action == "Next" or "Repeat" and (
        st.session_state.warmup_message == [] or st.session_state.warmup_message[-1]['role'] == "feedback"):
    response = question_chain.run(role=category, data=data, history=st.session_state.history[-4:],
                                  action=st.session_state.action, text=inp)

    with st.chat_message("assistant", avatar='rex.png'):
        st.markdown(response)
        st.session_state.action = "Feedback"
    st.session_state['warmup_message'].append({'role': 'interviewer', 'content': response})
    memory.save_context({"input": ""}, {"output": response})
    st.session_state['history'].append(memory.buffer_as_messages[-2:])
    question = response

if st.session_state.warmup_message[-1]['role'] == "user" and st.session_state.action == "Feedback":
    feedback = feedback_chain.run(question=question, response=inp, history=st.session_state.history[-4:], text=inp)

    with st.chat_message("assistant", avatar='rex.png'):
        st.markdown(feedback)
    st.session_state['warmup_message'].append({'role': 'feedback', 'content': feedback})
    memory.save_context({"input": inp}, {"output": feedback})
    st.session_state['history'].append(memory.buffer_as_messages[-2:])

if st.session_state.warmup_message[-1]['role'] == "feedback" and st.session_state.action == "Feedback":
    option = st.radio(label="Would you like to do?", options=["Next", "Repeat"], index=None)

st.markdown(st.session_state.history)