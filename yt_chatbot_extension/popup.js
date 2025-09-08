const chatLog = document.getElementById("chat-log");
const questionInput = document.getElementById("question");

document.getElementById("ask-btn").addEventListener("click", async () => {
  const question = questionInput.value.trim();
  if (!question) return;

  // Clear input field
  questionInput.value = "";

  // Show user message
  appendMessage("user", question);
  appendMessage("bot", "Thinking... ");

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = new URL(tab.url);
  const videoId = url.searchParams.get("v");

  if (!videoId) {
    updateLastBotMessage("This is not a valid YouTube video URL.");
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, query: question })
    });

    const data = await res.json();
    if (res.ok) {
      updateLastBotMessage("" + data.answer);
    } else {
      updateLastBotMessage(" Error: " + (data.detail || "Unknown error"));
    }
  } catch (err) {
    updateLastBotMessage("Could not reach backend. Is FastAPI running?");
  }
});

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = "message " + sender;
  msg.textContent = text;
  chatLog.appendChild(msg);
  chatLog.scrollTop = chatLog.scrollHeight; // auto-scroll
}

// Replace last bot message (used for "Thinking..." → actual response)
function updateLastBotMessage(newText) {
  const messages = document.querySelectorAll(".message.bot");
  const lastBot = messages[messages.length - 1];
  if (lastBot) lastBot.textContent = newText;
}
