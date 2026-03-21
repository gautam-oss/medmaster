document.addEventListener('DOMContentLoaded', function () {
    const chatForm      = document.getElementById('chatForm');
    const messageInput  = document.getElementById('messageInput');
    const chatMessages  = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    function scrollToBottom() { chatMessages.scrollTop = chatMessages.scrollHeight; }

    function addMessage(content, isUser = true) {
        const div = document.createElement('div');
        div.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        const safe = content
            .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
            .replace(/\n/g,'<br>');
        const time = new Date().toLocaleString();
        div.innerHTML = `
            <div class="message-wrapper">
                <div class="message-sender">
                    ${isUser ? '<i class="fas fa-user-circle"></i> You' : '<i class="fas fa-robot"></i> AI Assistant'}
                </div>
                <div class="message-content"><div class="message-text">${safe}</div></div>
                <div class="message-time"><i class="far fa-clock me-1"></i>${time}</div>
            </div>`;
        chatMessages.appendChild(div);
        scrollToBottom();
    }

    function showTyping() { typingIndicator.style.display = 'block'; scrollToBottom(); }
    function hideTyping() { typingIndicator.style.display = 'none'; }

    function getCookie(name) {
        let val = null;
        if (document.cookie) {
            document.cookie.split(';').forEach(c => {
                c = c.trim();
                if (c.startsWith(name + '=')) val = decodeURIComponent(c.slice(name.length + 1));
            });
        }
        return val;
    }

    function getCSRF() {
        return getCookie('csrftoken') ||
               (document.querySelector('[name=csrfmiddlewaretoken]') || {}).value || '';
    }

    async function sendMessage(message) {
        try {
            const csrf = getCSRF();
            const response = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                if (response.status === 403) throw new Error('Session expired. Please refresh the page.');
                throw new Error(`Server error (${response.status}). Please try again.`);
            }

            const data = await response.json();
            if (data.success) {
                addMessage(data.ai_response, false);
            } else {
                addMessage('Error: ' + (data.error || 'Something went wrong.'), false);
            }
        } catch (err) {
            addMessage('Sorry, I encountered an error: ' + err.message, false);
        } finally {
            hideTyping();
        }
    }

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const msg = messageInput.value.trim();
        if (!msg) return;
        addMessage(msg, true);
        messageInput.value = '';
        showTyping();
        sendMessage(msg);
    });

    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    messageInput.focus();
    scrollToBottom();
});
