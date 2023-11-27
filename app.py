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
