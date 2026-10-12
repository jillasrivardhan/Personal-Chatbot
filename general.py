

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from prompts import general_prompt
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=gemini_api_key,
      temperature=0.2,
      max_output_tokens=1000,
)

prompt = general_prompt

parser = StrOutputParser()

general_chain = prompt | model | parser     

# user_query = input("Enter your question: ")

# response = chain.invoke({"question": user_query})

# print("Response:", response)