from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables
load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

HF_TOKEN = os.getenv("HF_TOKEN")

st.title("Joke Generator...")
st.markdown("This app generates jokes using a Hugging Face model.")

topic = st.text_input("Enter a topic for the joke:")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a joke generating assistant. Generate only ONE joke on the given topic and do NOT continue any conversation include any introductions, explanations, or additional jokes."),
    ("user", "topic: {topic}")
])



llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=HF_TOKEN,
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

if topic:
    with st.spinner("Generating joke..."):
        response = chain.invoke({"topic": topic})
        st.success("Joke generated successfully!")
        st.write(response)
