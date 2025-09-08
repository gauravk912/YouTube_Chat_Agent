import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Track memory per session (video_id)
chat_sessions = {}

# ---------- Helper: Extract video ID ----------
def extract_video_id(url_or_id: str) -> str:
    if len(url_or_id) == 11 and not url_or_id.startswith("http"):
        return url_or_id
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    if not match:
        raise ValueError("Invalid YouTube video ID or URL.")
    return match.group(1)

# ---------- Fetch transcript ----------
def get_transcript_text(video_id: str) -> str:
    try:
        transcript_chunks = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return " ".join(chunk["text"] for chunk in transcript_chunks)
    except (TranscriptsDisabled, NoTranscriptFound):
        raise ValueError("No transcript available for this video.")
    except VideoUnavailable:
        raise ValueError("The video is unavailable.")
    except Exception as e:
        raise RuntimeError(f"Transcript fetching failed: {e}")

# ---------- Build vector store ----------
def build_vector_store(transcript_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([transcript_text])
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    return FAISS.from_documents(docs, embeddings)

# ---------- Create conversational chain ----------
def create_chatbot_chain(vector_store):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5}),
        memory=memory,
        return_source_documents=False
    )

    return qa_chain, memory

# ---------- Main entry point for FastAPI ----------
def ask_video_question(video_id: str, query: str) -> str:
    video_id_clean = extract_video_id(video_id)

    # Create or retrieve session for that video
    if video_id_clean not in chat_sessions:
        transcript = get_transcript_text(video_id_clean)
        vector_store = build_vector_store(transcript)
        chain, memory = create_chatbot_chain(vector_store)
        chat_sessions[video_id_clean] = {
            "chain": chain,
            "memory": memory
        }

    # Use existing memory chain
    chain = chat_sessions[video_id_clean]["chain"]

    result = chain.invoke({"question": query})
    return result["answer"]
