let currentConversation = null;
let currentUser = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkUserStatus();
});

// Check if user is logged in
async function checkUserStatus() {
    try {
        const response = await fetch('/api/user/profile');
        if (response.ok) {
            currentUser = await response.json();
            updateUserUI();
        }
    } catch (error) {
        console.log('Not logged in');
    }
}

function updateUserUI() {
    const userButton = document.getElementById('userButton');
    const logoutBtn = document.getElementById('logoutBtn');
    const profileBtn = document.getElementById('profileBtn');
    const adminLink = document.getElementById('adminLink');
    const teacherLink = document.getElementById('teacherLink');
    
    if (currentUser) {
        userButton.textContent = `👤 ${currentUser.full_name}`;
        logoutBtn.classList.remove('hidden');
        profileBtn.classList.remove('hidden');
        
        if (currentUser.role === 'admin') {
            adminLink.classList.remove('hidden');
        } else if (currentUser.role === 'teacher') {
            teacherLink.classList.remove('hidden');
        }
        
        logoutBtn.addEventListener('click', logout);
    } else {
        userButton.textContent = '👤 Guest';
    }
}

function toggleUserMenu() {
    const menu = document.getElementById('userMenu');
    menu.classList.toggle('hidden');
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    const userButton = document.getElementById('userButton');
    const userMenu = document.getElementById('userMenu');
    if (!userButton.contains(e.target) && !userMenu.contains(e.target)) {
        userMenu.classList.add('hidden');
    }
});

async function logout() {
    try {
        const response = await fetch('/logout', { method: 'GET' });
        if (response.ok) {
            currentUser = null;
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

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
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            removeTyping();
            addMessage(data.reply, "bot", data.type, data.intent, data.source);
        }, 600);
    })
    .catch(() => {
        removeTyping();
        addMessage("Error connecting to server.", "bot", "error");
    });
}

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

function addMessage(text, sender, responseType = 'text', intent = null, source = null) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    
    messageDiv.className = sender === "user" 
        ? "flex justify-end" 
        : "flex justify-start";
    
    const contentDiv = document.createElement("div");
    contentDiv.className = sender === "user"
        ? "bg-indigo-600 p-3 rounded-xl max-w-2xl text-white"
        : "bg-gray-700 p-3 rounded-xl max-w-2xl text-gray-100";
    
    // Format message based on response type
    if (responseType === 'table' && sender === 'bot') {
        // Convert markdown tables to HTML
        const html = convertMarkdownToHTML(text);
        contentDiv.innerHTML = html;
    } else {
        contentDiv.textContent = text;
        contentDiv.style.whiteSpace = 'pre-wrap';
        contentDiv.style.wordWrap = 'break-word';
    }
    
    // Add metadata for rule-based responses
    if (sender === 'bot' && source === 'rule_based') {
        const metaDiv = document.createElement('div');
        metaDiv.className = 'text-xs text-gray-400 mt-2';
        metaDiv.textContent = `📊 Rule-based (${intent})`;
        contentDiv.appendChild(metaDiv);
    }
    
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function convertMarkdownToHTML(markdown) {
    let html = markdown;
    
    // Convert headers
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert markdown tables to HTML tables
    const lines = html.split('\n');
    let inTable = false;
    let tableHTML = '';
    let result = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.startsWith('|')) {
            if (!inTable) {
                inTable = true;
                tableHTML = '<div class="overflow-x-auto"><table class="text-sm w-full border-collapse"><thead>';
            }
            
            // Check if it's a separator line
            if (line.includes('---')) {
                tableHTML += '</thead><tbody>';
            } else {
                const cells = line.split('|').filter(c => c.trim());
                tableHTML += '<tr>';
                
                for (let cell of cells) {
                    tableHTML += `<td class="border border-gray-600 px-2 py-1">${cell.trim()}</td>`;
                }
                
                tableHTML += '</tr>';
            }
        } else {
            if (inTable) {
                tableHTML += '</tbody></table></div>';
                result.push(tableHTML);
                inTable = false;
                tableHTML = '';
            }
            if (line) {
                result.push(`<p>${line}</p>`);
            }
        }
    }
    
    if (inTable) {
        tableHTML += '</tbody></table></div>';
        result.push(tableHTML);
    }
    
    return result.join('');
}

function createNewHistoryItem(preview) {
    const historyDiv = document.getElementById("history");
    const newItem = document.createElement("div");
    newItem.className = "p-2 hover:bg-gray-700 rounded cursor-pointer";
    newItem.textContent = preview.substring(0, 30) + "...";
    historyDiv.appendChild(newItem);
}

function newChat() {
    currentConversation = null;
    document.getElementById("chat-box").innerHTML = `
        <div class="bg-gray-700 bg-opacity-30 p-4 rounded-lg">
            <p class="text-gray-300">Welcome to Student Assistant AI! 🎓</p>
            <p class="text-gray-400 text-sm mt-2">Ask me about:</p>
            <ul class="text-gray-400 text-sm mt-2 ml-4 list-disc">
                <li>📚 Exam Routine & Schedules</li>
                <li>📅 Class Routine & Timetables</li>
                <li>✏️ Class Tests (CT) & Topics</li>
                <li>📝 Assignment Deadlines</li>
                <li>💡 General Academic Help</li>
            </ul>
        </div>
    `;
    document.getElementById("user-input").value = "";
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("w-64");
    sidebar.classList.toggle("w-0");
}
