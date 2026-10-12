
import os
from operator import itemgetter

from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from prompts import personal_prompt


# -------------------------------------
# Load environment variables
# -------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# -------------------------------------
# Data ingestion
# -------------------------------------

loader = TextLoader("self.txt", encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50,
)

splits = text_splitter.split_documents(documents)


# -------------------------------------
# Embeddings and vector store
# -------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)

vector_store = FAISS.from_documents(
    documents=splits,
    embedding=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# -------------------------------------
# Gemini LLM
# -------------------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    max_output_tokens=1500,
)


# -------------------------------------
# Format retrieved documents
# -------------------------------------

def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )


# -------------------------------------
# Personal chatbot chain
# -------------------------------------

parser = StrOutputParser()

personal_chain = (
    {
        "context": (
            itemgetter("question")
            | retriever
            | RunnableLambda(format_docs)
        ),
        "question": itemgetter("question"),
    }

    | personal_prompt
    | model
    | parser
)


# -------------------------------------
# Test the personal chain
# -------------------------------------

# while True:
#     user_query = input("Enter your question: ")

#     if user_query.lower() in ["exit", "quit"]:
#          break
    
#     response = personal_chain.invoke({
#         "question": user_query
#     })

#     print("\nResponse:\n", response)