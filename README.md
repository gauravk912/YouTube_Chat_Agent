# 🎥 YouTube Video Chatbot – Chrome Extension

Ever wished you could **chat with a YouTube video**?  
No more scrubbing through hours of tutorials or lectures — just ask and get instant answers.  

This Chrome extension turns any YouTube video into an **interactive knowledge agent** with context, memory, and **RAG-powered AI**.

---

## ✨ Features

- ✅ **Chat with videos** — ask questions directly on YouTube  
- ✅ **Context-aware answers** — the AI remembers your past queries  
- ✅ **Jump to timestamps** — get exact sections instantly  
- ✅ **Works on long videos (3+ hrs)** — no more losing context  
- ✅ **Powered by RAG** — transcript → FAISS → LangChain → GPT  

---

## 🚀 How It Works

1. **Transcript Fetching** → The extension grabs the video transcript  
2. **Chunking + Vector DB** → Transcript is split into chunks and stored in **FAISS** (semantic search)  
3. **Question → Retrieval** → Your query retrieves the most relevant chunks  
4. **Answer Generation** → **GPT-4o-mini** (via LangChain) generates the response with context  
5. **Interactive Agent** → Keeps memory across multiple queries in the same video  

---

## 🛠️ Tech Stack

- **Frontend** → Chrome Extension  
- **Backend** → FastAPI  
- **LLM Orchestration** → LangChain  
- **Vector Database** → FAISS  
- **LLM** → GPT-4o-mini (OpenAI API)  

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/chat-with-youtube.git
cd chat-with-youtube

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 🎥 YouTube Video Chatbot – Chrome Extension

---

## 3. Extension Setup

1. Open `chrome://extensions/`  
2. Enable **Developer Mode**  
3. Click **Load unpacked** and select the `extension` folder  

---

## 🎯 Usage

1. Open any YouTube video  
2. Click the extension icon  
3. Ask questions like:  
   - “What does the speaker say about LangChain?”  
   - “Does this cover RAG vs fine-tuning?”  
   - “Give me the timestamp where FAISS is explained”  

---

## 🔮 Future-Work

- [ ] Cross-video Q&A  
- [ ] Smarter clip navigation  
- [ ] Support for podcasts & recorded meetings  
- [ ] Cloud deployment for multi-user access  
