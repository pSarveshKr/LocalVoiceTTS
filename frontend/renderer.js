const API = window.location.protocol.startsWith("http")
  ? window.location.origin
  : "http://127.0.0.1:8000";

const state = {
  voices: [],
  finalAudioBlob: null,
  activeAudioUrl: null,
};

const uploadForm = document.getElementById("uploadForm");
const voiceNameInput = document.getElementById("voiceName");
const voiceFileInput = document.getElementById("voiceFile");
const voiceTags = document.getElementById("voiceTags");
const linesContainer = document.getElementById("linesContainer");
const addLineButton = document.getElementById("addLineButton");
const combineButton = document.getElementById("combineButton");
const downloadButton = document.getElementById("downloadButton");
const statusBar = document.getElementById("statusBar");
const audioPreview = document.getElementById("audioPreview");

function setStatus(message, tone = "") {
  statusBar.textContent = message;
  statusBar.className = `status ${tone}`.trim();
}

function makeButton(text, className, title) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = className;
  button.textContent = text;
  if (title) button.title = title;
  return button;
}

async function errorMessage(response) {
  const type = response.headers.get("content-type") || "";
  if (type.includes("application/json")) {
    const data = await response.json();
    return data.detail || data.error || "Request failed.";
  }

  return (await response.text()) || "Request failed.";
}

async function fetchAudio(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  return response.blob();
}

function playBlob(blob) {
  if (state.activeAudioUrl) {
    URL.revokeObjectURL(state.activeAudioUrl);
  }

  state.activeAudioUrl = URL.createObjectURL(blob);
  audioPreview.src = state.activeAudioUrl;
  audioPreview.classList.add("is-visible");
  audioPreview.play();
}

async function loadVoices() {
  try {
    const response = await fetch(`${API}/voices`);
    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    const data = await response.json();
    state.voices = data.voices || [];
    renderVoiceTags();
    refreshAllSelects();
    setStatus("Ready", "good");
  } catch (error) {
    setStatus("Backend is not reachable. Run python start.py from this folder.", "error");
  }
}

function renderVoiceTags() {
  voiceTags.replaceChildren();

  if (state.voices.length === 0) {
    const empty = document.createElement("span");
    empty.className = "empty-state";
    empty.textContent = "No voices uploaded";
    voiceTags.appendChild(empty);
    return;
  }

  state.voices.forEach((voice) => {
    const tag = document.createElement("div");
    tag.className = "voice-tag";

    const label = document.createElement("span");
    label.textContent = voice;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "tag-delete";
    remove.textContent = "x";
    remove.title = `Delete ${voice}`;
    remove.addEventListener("click", () => deleteVoice(voice));

    tag.append(label, remove);
    voiceTags.appendChild(tag);
  });
}

function refreshAllSelects() {
  document.querySelectorAll(".voice-select").forEach((select) => {
    const current = select.value;
    select.replaceChildren();

    if (state.voices.length === 0) {
      const option = new Option("No voices", "");
      select.appendChild(option);
      return;
    }

    state.voices.forEach((voice) => {
      select.appendChild(new Option(voice, voice));
    });

    if (state.voices.includes(current)) {
      select.value = current;
    }
  });
}

async function uploadVoice(event) {
  event.preventDefault();

  const name = voiceNameInput.value.trim();
  const file = voiceFileInput.files[0];

  if (!name) {
    setStatus("Add a voice name first.", "error");
    voiceNameInput.focus();
    return;
  }

  if (!file) {
    setStatus("Choose a WAV or MP3 voice sample.", "error");
    voiceFileInput.focus();
    return;
  }

  const formData = new FormData();
  formData.append("name", name);
  formData.append("file", file);

  const submitButton = uploadForm.querySelector("button[type='submit']");
  submitButton.disabled = true;
  setStatus(`Uploading ${name}...`, "work");

  try {
    const response = await fetch(`${API}/upload-voice`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    const data = await response.json();
    voiceNameInput.value = "";
    voiceFileInput.value = "";
    await loadVoices();
    setStatus(`Voice ${data.voice || name} uploaded.`, "good");
  } catch (error) {
    setStatus(error.message || "Upload failed.", "error");
  } finally {
    submitButton.disabled = false;
  }
}

async function deleteVoice(name) {
  if (!window.confirm(`Delete voice "${name}"?`)) return;

  setStatus(`Deleting ${name}...`, "work");

  try {
    const response = await fetch(`${API}/voices/${encodeURIComponent(name)}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(await errorMessage(response));
    }

    await loadVoices();
    setStatus(`Voice ${name} deleted.`, "good");
  } catch (error) {
    setStatus(error.message || "Delete failed.", "error");
  }
}

function addLine(text = "", voice = "") {
  const row = document.createElement("div");
  row.className = "line-row";

  const select = document.createElement("select");
  select.className = "voice-select";
  select.title = "Voice";

  const input = document.createElement("input");
  input.type = "text";
  input.value = text;
  input.placeholder = "Type dialog text";
  input.autocomplete = "off";
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addLine();
    }
  });

  const playButton = makeButton("Play", "btn secondary", "Preview this line");
  playButton.addEventListener("click", () => playLine(row));

  const removeButton = makeButton("x", "btn danger remove-line", "Remove line");
  removeButton.addEventListener("click", () => row.remove());

  row.append(select, input, playButton, removeButton);
  linesContainer.appendChild(row);
  refreshAllSelects();

  if (voice && state.voices.includes(voice)) {
    select.value = voice;
  }

  input.focus();
}

async function playLine(row) {
  const voice = row.querySelector(".voice-select").value;
  const text = row.querySelector("input").value.trim();
  const button = row.querySelector(".btn.secondary");

  if (!text) {
    setStatus("Type text before previewing a line.", "error");
    return;
  }

  if (!voice) {
    setStatus("Upload a voice before previewing.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("text", text);
  formData.append("voice", voice);

  button.disabled = true;
  button.textContent = "Working";
  setStatus(`Synthesizing with ${voice}...`, "work");

  try {
    const blob = await fetchAudio(`${API}/synthesize`, {
      method: "POST",
      body: formData,
    });

    playBlob(blob);
    setStatus("Playing preview.", "good");
  } catch (error) {
    setStatus(error.message || "Synthesis failed.", "error");
  } finally {
    button.disabled = false;
    button.textContent = "Play";
  }
}

function collectLines() {
  return Array.from(document.querySelectorAll(".line-row"))
    .map((row) => ({
      text: row.querySelector("input").value.trim(),
      voice: row.querySelector(".voice-select").value,
    }))
    .filter((line) => line.text && line.voice);
}

async function combineAll() {
  const lines = collectLines();

  if (lines.length === 0) {
    setStatus("Add at least one line with a voice.", "error");
    return;
  }

  combineButton.disabled = true;
  setStatus(`Combining ${lines.length} line${lines.length === 1 ? "" : "s"}...`, "work");

  try {
    state.finalAudioBlob = await fetchAudio(`${API}/combine`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lines }),
    });

    playBlob(state.finalAudioBlob);
    setStatus("Combined dialog is ready.", "good");
  } catch (error) {
    setStatus(error.message || "Combine failed.", "error");
  } finally {
    combineButton.disabled = false;
  }
}

function downloadFinal() {
  if (!state.finalAudioBlob) {
    setStatus("Combine the dialog before downloading.", "error");
    return;
  }

  const link = document.createElement("a");
  link.href = URL.createObjectURL(state.finalAudioBlob);
  link.download = "dialog.wav";
  link.click();
  URL.revokeObjectURL(link.href);
  setStatus("dialog.wav is ready to save.", "good");
}

uploadForm.addEventListener("submit", uploadVoice);
addLineButton.addEventListener("click", () => addLine());
combineButton.addEventListener("click", combineAll);
downloadButton.addEventListener("click", downloadFinal);

loadVoices().finally(() => {
  if (linesContainer.children.length === 0) {
    addLine();
  }
});
