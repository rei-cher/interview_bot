<<<<<<< HEAD
import streamlit as st
import requests
from google.cloud import aiplatform
import keys
#some random changes
#some random changes
# Set up Google Cloud credentials (replace 'your_credentials.json' with your actual credentials file)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_credentials.json"

# Set up Vertex AI endpoint (replace 'your_model_endpoint' with your actual model endpoint)
MODEL_ENDPOINT = keys.ENDPOINT
OPENAI_API = keys.APIKEY

title_placeholder = st.empty()
message = st.chat_message("ai")
answer = st.chat_input("Your answer")

# Streamlit app
def main():
    title_placeholder.title("Data Analyst Prep Interview Bot")
    interview()

    

def interview(): 
    
    # Initialize conversation history
    conversation_history = [{'role': 'system', 'content': 'You are an interview bot. You are asking a user questions that are coorelate with the Data Analyst Job. You have to ask one question at a time."'}]

    # Generate a question
    question = generate_question(conversation_history)
    
    message.write(question)
    if answer:    
        message.write(f"Your answer: {answer}")
        # # Get user's response
        # response_key = f"{answer}_response"
        # user_response = st.text_input(f"{answer}, {question}", key=response_key)
    

        # # Validate user's response
        # validation_result = validate_response(user_response)
        # #st.success(validation_result['feedback'])
    
        # if validation_result['is_valid']:
        #     # Add user's response to the conversation history
        conversation_history.append({"role": "user", "content": answer})

        # Generate a question
        question = generate_question(conversation_history)        
        message.write(f"{question}")

# def generate_question(conversation_history):
#     # Use Vertex AI language model to generate a question based on the conversation history
#     # Replace 'your_model_endpoint' with your actual model endpoint
#     # You may need to adjust the input format based on your model's requirements
#     model_input = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])
    
#     prediction = predict_vertex_ai(model_input)

#     question = prediction['content'].strip()

#     return question

# def predict_vertex_ai(input_text):
#     # Set up Vertex AI client
#     aiplatform.init(project=keys.PROJECTID, location=keys.LOCATION)

#     # Make a prediction request to the deployed language model
#     endpoint = MODEL_ENDPOINT
#     model = aiplatform.Predictor(endpoint)

#     prediction = model.predict([{"content": input_text}])

#     return prediction['predictions'][0]

# def validate_response(conversation_history):
#     # Use Vertex AI language model to analyze and validate the response
#     # This is a simplified example; you may need to customize based on your requirements
#     model_input = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])

#     prediction = predict_vertex_ai(model_input)

#     # You may need to customize the validation logic based on the Vertex AI response
#     is_valid = True if prediction['is_valid'] else False

#     feedback = prediction['feedback']

#     return {'is_valid': is_valid, 'feedback': feedback}

def generate_question(conversation_history):
    # Use ChatGPT API (LaMDA) to generate a question based on the conversation history
    prompt = "\n".join(item['content'] for item in conversation_history)  # Use the entire conversation as context
    question = get_chatgpt_response(prompt)
    return question

def get_chatgpt_response(prompt):
    # Set up headers with the OpenAI API key
    headers = {
        'Authorization': f'Bearer {OPENAI_API}',
        'Content-Type': 'application/json',
        'Openai-Model': 'gpt-4',
    }

    # Set up the data payload
    data = {
        'messages': [{'role': 'system', 'content': 'You are an interview bot. You are asking a user questions that are coorelate with the Data Analyst Job. You have to ask one question at a time. Wait for the user\'s response. Start with the general questions. And after an each question, increment the difficulty.'}, {'role': 'user', 'content': prompt}],
    }

    # Make a POST request to the ChatGPT API
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    # Print the response content for debugging
    # print(response.content)

    # Check for potential errors
    if response.status_code != 200:
        raise ValueError(f"Error from OpenAI API: {response.content}")

    # Parse the response and extract the generated message
    response_data = response.json()

    # Check for 'choices' in the top-level response or within 'data' field
    choices = response_data.get('choices') or response_data.get('data', {}).get('choices')

    if choices:
        generated_message = choices[0].get('message', {}).get('content')
        if generated_message is not None:
            return generated_message

    raise ValueError("Unexpected response structure")

def validate_response(response):
    
    if response and response.strip():
        return {'is_valid': True, 'feedback': 'Response received'}
    else:
        return {'is_valid': False, 'feedback': 'Please provide a response'}


if __name__ == "__main__":
    main()
=======
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

>>>>>>> 165305ed72825eeb97817a571413a4efae85bc06
