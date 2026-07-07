const chat = document.getElementById("chat");
const emptyState = document.getElementById("empty-state");
const queryInput = document.getElementById("query-input");
const askBtn = document.getElementById("ask-btn");
const recordBtn = document.getElementById("record-btn");
const statusBar = document.getElementById("status-bar");

function setStatus(text) {
  if (!text) {
    statusBar.classList.add("hidden");
    statusBar.textContent = "";
    return;
  }

  statusBar.textContent = text;
  statusBar.classList.remove("hidden");
}

function scrollToBottom() {
  chat.scrollTop = chat.scrollHeight;
}

function hideEmptyState() {
  emptyState.classList.add("hidden");
}

function addUserMessage(text, tag) {
  hideEmptyState();

  const msg = document.createElement("div");
  msg.className = "msg user";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (tag) {
    const tagEl = document.createElement("div");
    tagEl.className = "msg-tag";
    tagEl.textContent = tag;
    bubble.appendChild(tagEl);
  }

  const textEl = document.createElement("div");
  textEl.textContent = text;
  bubble.appendChild(textEl);

  msg.appendChild(bubble);
  chat.appendChild(msg);
  scrollToBottom();
}

function addAssistantBubble(isError) {
  hideEmptyState();

  const msg = document.createElement("div");
  msg.className = "msg assistant";

  const bubble = document.createElement("div");
  bubble.className = "bubble" + (isError ? " error" : "");
  bubble.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';

  msg.appendChild(bubble);
  chat.appendChild(msg);
  scrollToBottom();

  return bubble;
}

function resolveBubble(bubble, text, isError) {
  bubble.classList.toggle("error", Boolean(isError));
  bubble.textContent = text;
  scrollToBottom();
}

async function askText() {
  const query = queryInput.value.trim();

  if (!query) {
    return;
  }

  queryInput.value = "";
  askBtn.disabled = true;

  addUserMessage(query);
  const bubble = addAssistantBubble(false);

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    resolveBubble(bubble, data.answer, false);
  } catch (err) {
    resolveBubble(bubble, err.message, true);
  } finally {
    askBtn.disabled = false;
    queryInput.focus();
  }
}

askBtn.addEventListener("click", askText);

queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    askText();
  }
});

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

  mediaRecorder.onstop = async () => {
    stream.getTracks().forEach((track) => track.stop());

    const blob = new Blob(audioChunks, { type: "audio/webm" });
    await sendVoiceQuery(blob);
  };

  mediaRecorder.start();
  isRecording = true;

  recordBtn.classList.add("recording");
  setStatus("Listening... click the mic again to stop.");
}

function stopRecording() {
  if (mediaRecorder && isRecording) {
    mediaRecorder.stop();
  }

  isRecording = false;
  recordBtn.classList.remove("recording");
}

async function sendVoiceQuery(blob) {
  setStatus("Transcribing...");
  recordBtn.disabled = true;

  const formData = new FormData();
  formData.append("audio", blob, "recording.webm");

  try {
    const res = await fetch("/api/voice", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      resolveBubble(addAssistantBubble(true), data.detail || "Request failed.", true);
      return;
    }

    addUserMessage(data.transcribed, "Voice");
    resolveBubble(addAssistantBubble(false), data.answer, false);
  } catch (err) {
    resolveBubble(addAssistantBubble(true), err.message, true);
  } finally {
    recordBtn.disabled = false;
    setStatus(null);
  }
}

recordBtn.addEventListener("click", async () => {
  if (isRecording) {
    stopRecording();
    return;
  }

  try {
    await startRecording();
  } catch (err) {
    resolveBubble(addAssistantBubble(true), "Microphone access denied or unavailable.", true);
  }
});
