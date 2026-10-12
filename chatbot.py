
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableBranch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from prompts import classification_prompt
from general import general_chain
from personal import personal_chain

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

routing_prompt = classification_prompt

model = ChatGoogleGenerativeAI(
      model="gemini-3.5-flash",
      google_api_key=GEMINI_API_KEY,
      temperature=0.2,
      max_output_tokens=1000,
   )

parser = StrOutputParser()

router_chain = routing_prompt | model | parser

classified_chain = RunnablePassthrough.assign(
    category=router_chain
)

main_chain = classified_chain | RunnableBranch(
    (
        lambda x: x["category"].strip().upper() == "PERSONAL",
        personal_chain,
    ),
    general_chain,  # Default branch
)

if __name__ == "__main__":
    print("Welcome to the Personal AI Chatbot! Type 'exit' or 'quit' to end the conversation.")
    while True:
        question = input("\nYou: ")

        if question.strip().lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye, bro!")
            break

        response = main_chain.invoke({
            "question": question
        })

        print("\nChatbot:", response)