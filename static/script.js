function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    const chatBox = document.getElementById("chat-box");

    if (message === "") return;

    // Show user message
    chatBox.innerHTML += `<div class="message user">${message}</div>`;

    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send to backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
