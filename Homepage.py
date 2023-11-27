import streamlit as st

st.set_page_config(page_icon='resumeicon.png', layout='wide', page_title='Interview Preparation : Getting Started')

st.sidebar.markdown("Navigate using the options above")
key = st.sidebar.text_input("OpenAI API Key ", type="password")

if "openai_key" not in st.session_state:
    st.session_state.openai_key = key

if not key and not st.session_state.openai_key:
    st.sidebar.info("Please add your API key to continue")
    st.stop()


st.title("""AI Interview Preparation Tool : Getting Started""")
st.title("Recommended Steps : ")

st.markdown("""\n1. Please upload your resume in the sidebar on your left.
               \n\n2. If you are applying for a specific job , please add job description in the text box below.
               \n\n3. For started we recommend navigating to the Introduction Round , here your AI assistant will debrief you
                on the interview and answer your queries related to the interview.
               \n\n4. Next, we recommend having a go with a low stakes Warmup Round to get you in the right flow for the 
               actual interview round.
               \n\n5. Navigate to the Interview Round to get started with your practice interviews.\n\n""")


st.sidebar.file_uploader("**Please upload your resume**", type='pdf')


st.text_area(label="**Write your job description here**",height=300)