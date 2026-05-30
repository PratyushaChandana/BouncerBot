const chatBox = document.getElementById("chat-box");
const toggleBtn = document.getElementById("chat-toggle");

toggleBtn.onclick = () => {
    chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
};

function addMessage(text, sender) {
    const box = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "msg " + sender;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
    const text = document.getElementById("input").value;
    if (!text) return;

    addMessage(text, "user");
    document.getElementById("input").value = "";

    const res = await fetch("/message", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    });

    const data = await res.json();
    addMessage(data.reply, "bot");
}

// Fetch intro from backend
fetch("/message", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: "__init__"})
})
.then(res => res.json())
.then(data => addMessage(data.reply, "bot"));
