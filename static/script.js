let currentConversation = null;

function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (message === "") return;

    addMessage(message, "user");
    if (!currentConversation) {
    createNewHistoryItem(message);
}
    inputField.value = "";

    showTyping();

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error");
        }
        return response.json();
    })
    .then(data => {
        removeTyping();
        addMessage(data.reply, "bot");
    })
    .catch(error => {
        removeTyping();
        addMessage("Server connection failed.", "bot");
        console.error("Error:", error);
    });
}

function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");

    messageDiv.className =
        sender === "user"
        ? "bg-indigo-600 self-end p-3 rounded-xl max-w-xs"
        : "bg-gray-700 p-3 rounded-xl max-w-xs";

    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("hidden");
}

function openLogin() {
    document.getElementById("loginModal").classList.remove("hidden");
}

function closeLogin() {
    document.getElementById("loginModal").classList.add("hidden");
}

document.getElementById("user-input")
.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function showTyping() {
    const chatBox = document.getElementById("chat-box");
    const typingDiv = document.createElement("div");
    typingDiv.id = "typing";
    typingDiv.className = "bg-gray-700 p-3 rounded-xl max-w-xs animate-pulse";
    typingDiv.innerText = "Typing...";
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

function newChat() {
    document.getElementById("chat-box").innerHTML = "";
    currentConversation = null;
}

function addToHistory(message) {
    const history = document.getElementById("history");
    const item = document.createElement("div");

    item.className = "p-2 hover:bg-gray-700 rounded cursor-pointer text-sm";
    item.innerText = message.substring(0, 25) + "...";

    history.appendChild(item);
}

function createNewHistoryItem(firstMessage) {
    const history = document.getElementById("history");
    const item = document.createElement("div");

    currentConversation = Date.now();

    item.className = "p-2 hover:bg-gray-700 rounded cursor-pointer text-sm";
    item.innerText = firstMessage.substring(0, 25);

    history.prepend(item);
}