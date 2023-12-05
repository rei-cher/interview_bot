from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from dotenv import load_dotenv

def get_major(text):
    load_dotenv()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunk = text_splitter.split_text(text)

    embedding = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunk, embedding)
    docs_major = knowledge_base.similarity_search("What is a major in the file")
    docs_skills = knowledge_base.similarity_search("What are the skills in the file")
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    role = chain.run(input_documents = docs_major, question = "What is a major in the file")
    skills = chain.run(input_documents = docs_skills, question = "What are the skills in the file")
    return role,skills