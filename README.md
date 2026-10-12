# 🤖 Personal AI Chatbot — Powered by LangChain & Gemini

A personal AI chatbot that answers questions about you using your own personal knowledge file and handles general questions using Google's Gemini models.

Built with **Python, LangChain, Google Gemini, FAISS, and Streamlit**, this project demonstrates query classification, retrieval-augmented generation (RAG), and conditional chain routing without using AI agents or tool-calling frameworks.

## ✨ Features

* 👤 **Personal Q&A:** Answers questions about your education, technical skills, projects, and professional interests using `self.txt`.
* 🌐 **General Q&A:** Uses Google Gemini to answer programming, technology, and general knowledge questions.
* 🔀 **Intelligent Routing:** Uses LangChain's `RunnableBranch` to select the appropriate response chain.
* 🔎 **Semantic Search:** Uses Google embeddings and FAISS to retrieve relevant personal information.
* 💬 **Interactive Chat UI:** Provides a Streamlit chat interface with message history and a sidebar.
* 🧩 **Modular Architecture:** Keeps personal processing, general responses, routing, and UI in separate files.
* 🛡️ **Context-Aware Responses:** Uses a personal prompt that instructs the model not to invent missing personal details.

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │       User Query     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    Streamlit UI       │
                  │       app.py          │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    Query Router       │
                  │   Gemini + LangChain  │
                  └──────────┬───────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
          ┌────────────────┐  ┌────────────────┐
          │ PERSONAL Query │  │ GENERAL Query  │
          └────────┬───────┘  └────────┬───────┘
                   │                   │
                   ▼                   ▼
          ┌────────────────┐  ┌────────────────┐
          │   self.txt     │  │  Gemini LLM    │
          │ Text Splitting │  │ General Chain  │
          │ Embeddings     │  └────────┬───────┘
          │ FAISS Search   │           │
          └────────┬───────┘           │
                   │                   │
                   ▼                   │
          ┌────────────────┐           │
          │ Personal Chain │           │
          └────────┬───────┘           │
                   │                   │
                   └─────────┬─────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Final Response      │
                  └──────────────────────┘
```

## ⚙️ How It Works

### 1. Personal Knowledge Ingestion

The chatbot loads information from `self.txt`, splits it into smaller chunks using `RecursiveCharacterTextSplitter`, generates embeddings, and stores the resulting vectors in FAISS.

### 2. Query Classification

A Gemini-powered router classifies each user query into one of two categories:

| Category   | Purpose                                                | Example                     |
| ---------- | ------------------------------------------------------ | --------------------------- |
| `PERSONAL` | Questions requiring information about the user         | What projects have I built? |
| `GENERAL`  | Questions that can be answered using general knowledge | What is LangChain?          |

### 3. Conditional Routing

LangChain's `RunnableBranch` selects the appropriate chain based on the router's classification.

* **Personal chain:** Retrieves relevant text from FAISS and supplies it to the personal prompt.
* **General chain:** Sends the query to the general-purpose Gemini chain.

### 4. Response Generation

The selected chain generates the answer and returns it to the Streamlit interface.

**Note:** This is a chain-based chatbot, not an autonomous AI agent. It uses predefined routing logic rather than agent tool selection or autonomous tool execution.

## 🛠️ Tech Stack

| Technology                      | Purpose                                               |
| ------------------------------- | ----------------------------------------------------- |
| Python                          | Core programming language                             |
| LangChain                       | Prompt templates, runnable composition, and branching |
| Google Gemini API               | Query classification and language generation          |
| Google Generative AI Embeddings | Converts personal text into vector representations    |
| FAISS                           | Similarity search over personal knowledge             |
| Streamlit                       | Interactive chat interface                            |
| python-dotenv                   | Environment variable management                       |

## 📁 Project Structure

```text
Personal-Chatbot/
│
├── app.py                 # Streamlit user interface
├── main.py                # Router and RunnableBranch
├── personal.py            # Personal knowledge retrieval chain
├── general.py             # General-purpose Gemini chain
├── prompts.py             # Prompt templates
├── self.txt               # Personal knowledge base
├── .env                   # API key configuration
├── .gitignore             # Files excluded from Git
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or a compatible version supported by your installed packages
* A Google Gemini API key with access to the selected models
* An internet connection for Gemini API calls and embedding generation
* Basic familiarity with Python and LangChain

### 1. Clone the Repository

```bash
git clone https://github.com/jillasrivardhan/Personal-Chatbot.git
cd Personal-Chatbot
```

Replace the repository URL with your actual GitHub repository URL if the project has a different name.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv chatbot
chatbot\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv chatbot
source chatbot/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you have not created `requirements.txt` yet, you can install the main packages with:

```bash
pip install streamlit python-dotenv langchain langchain-core langchain-community langchain-text-splitters langchain-google-genai faiss-cpu
```

Use package versions compatible with your project and consult the relevant integration documentation when updating LangChain packages.

### 4. Configure Your API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Obtain your API key through [Google AI Studio](https://aistudio.google.com/).

Never commit your actual API key to GitHub.

### 5. Prepare Your Personal Knowledge File

Create `self.txt` and add information you want the chatbot to know, such as:

* Personal and educational background
* Technical skills
* Projects and their descriptions
* Professional interests
* Career goals

Use accurate information and avoid including passwords, API keys, or other sensitive details.

### 6. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal by Streamlit.

## 💬 Example Questions

### Personal Questions

* What is my educational background?
* What are my technical skills?
* Which AI projects have I built?
* What technologies do I use in my projects?

### General Questions

* What is LangChain?
* Explain retrieval-augmented generation.
* What is the difference between embeddings and an LLM?
* How does a vector database work?

The personal chain can only answer questions supported by the content retrieved from `self.txt`. Add more verified information to improve coverage.

## 🔐 Privacy and Security

* Keep `.env` out of version control.
* Do not publish personal information unless you intend to make it public.
* Use `.gitignore` to exclude secrets, virtual environments, caches, and local data.
* Be aware that queries sent to Gemini and text sent for embedding generation are processed by Google's API services.
* The application uses a local FAISS index in the current implementation, but the underlying personal data is not automatically private from external API processing.
* Avoid putting confidential personal or professional information into the knowledge base.

## ⚠️ Limitations

* Responses depend on the accuracy and completeness of `self.txt`.
* The router may occasionally classify a query incorrectly.
* Similarity search may retrieve incomplete or irrelevant context.
* General responses depend on the selected Gemini model.
* API access, model availability, rate limits, and usage quotas can affect operation.
* Chat history in Streamlit session state is not permanent storage.
* The current implementation does not provide autonomous agent behavior or tool calling.

## 🔮 Future Improvements

* Add persistent conversation history using SQLite.
* Improve routing with structured output and category validation.
* Add a dedicated `HYBRID` category for questions requiring both personal context and general knowledge.
* Support multiple personal knowledge files.
* Add tests for routing, retrieval, and missing personal information.
* Add caching for embeddings and the FAISS index to reduce repeated initialization.
* Improve retrieval using metadata filtering and configurable chunk sizes.
* Add optional streaming responses and more detailed error handling.
* Deploy the chatbot using Streamlit Community Cloud or another suitable hosting platform.

## 🎯 Learning Outcomes

By building this project, you can practice:

* LangChain Expression Language (LCEL)
* `RunnableBranch` and runnable composition
* Prompt engineering and query classification
* Text splitting, embeddings, and vector similarity search
* Retrieval-augmented generation
* Gemini API integration
* Streamlit application development
* Modular design for LLM applications

## 👨‍💻 Author

**Jilla Srivardhan**

* LinkedIn: [jilla-srivardhan](https://www.linkedin.com/in/jilla-srivardhan/)
* GitHub: [jillasrivardhan](https://github.com/jillasrivardhan)

## 📄 License

Consider adding an [MIT License](https://choosealicense.com/licenses/mit/) if you want others to reuse and modify the project. Only include it once you have decided on the project's licensing terms.

---

⭐ If you find this project useful, consider starring the repository and sharing your feedback.
