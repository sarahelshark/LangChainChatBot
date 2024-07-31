document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const placeholder = document.getElementById("placeholder");
    const userInput = document.getElementById("userInput");
    const sendButton = document.querySelector("button");
    const resetButton = document.createElement("button");
    resetButton.textContent = "Reset Conversation";
    resetButton.style.marginLeft = "10px";
    sendButton.parentNode.insertBefore(resetButton, sendButton.nextSibling);

    /**
     * Appends a new message to the chatbox.
     * 
     * @param {string} content - The content of the message.
     * @param {string} sender - The sender of the message.
     */
    function appendMessage(content, sender) {
        const messageElement = document.createElement("div");
        messageElement.className = `message ${sender}`;
        messageElement.innerText = content;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    /**
     * Sends a message to the chat API and appends the user's message to the chat window.
     * @async
     * @function sendMessage
     */
    async function sendMessage() {
        const input = userInput.value.trim();
        if (!input) return;

        appendMessage(input, "user");
        userInput.value = "";
        placeholder.innerHTML = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.content) {
                appendMessage(data.content, "assistant");
            } else {
                console.error("Unexpected response format:", data);
            }
        } catch (error) {
            console.error("Error sending message:", error);
            appendMessage("Sorry, there was an error processing your request.", "assistant");
        }
    }

    /**
     * Resets the conversation by making a POST request to the '/api/reset' endpoint.
     * Clears the chatbox and displays a message indicating that the conversation has been reset.
     * If an error occurs during the reset process, an error message is displayed.
     */
    async function resetConversation() {
        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            chatbox.innerHTML = ''; 
            appendMessage("Conversation reset. You can start a new chat now.", "system");
        } catch (error) {
            console.error("Error resetting conversation:", error);
            appendMessage("Sorry, there was an error resetting the conversation.", "system");
        }
    }

    // Attach sendMessage function to the button
    sendButton.addEventListener("click", sendMessage);

    // Attach resetConversation function to the reset button
    resetButton.addEventListener("click", resetConversation);

    // Allow pressing "Enter" to send the message
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});