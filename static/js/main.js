
    const chatbox = document.getElementById("chatbox");
    const placeholder = document.getElementById("placeholder");
    
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const resetButton = document.createElement("button");
    resetButton.classList.add("btn", "border" ,"border-danger", "btn-outline-danger", "rounded" );
    resetButton.textContent = "Reset Conversation";
    resetButton.style.marginLeft = "10px";
    sendButton.parentNode.insertBefore(resetButton, sendButton.nextSibling);

    // Add model selection dropdown
    const modelSelect = document.createElement("select");
    modelSelect.id = "modelSelect";
    modelSelect.classList.add("border-primary");
    
    const chatgptOption = document.createElement("option");
    chatgptOption.value = "chatgpt";
    chatgptOption.textContent = "ChatGPT";
    const geminiOption = document.createElement("option");
    geminiOption.value = "gemini";
    geminiOption.textContent = "Gemini";
    modelSelect.appendChild(chatgptOption);
    modelSelect.appendChild(geminiOption);
    sendButton.parentNode.insertBefore(modelSelect, sendButton);


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
            console.log("Sending request to /api/chat");
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input, model: modelSelect.value }),
            });
            
            console.log("Response received. Status:", response.status);
            console.log("Response headers:", response.headers);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const responseText = await response.text();
            console.log("Raw response text:", responseText);
            
            let data;
            try {
                data = JSON.parse(responseText);
                console.log("Parsed JSON data:", data);
            } catch (parseError) {
                console.error("Error parsing JSON:", parseError);
                appendMessage("Error: Received invalid JSON from server.", "system");
                return;
            }
            
            if (data && data.content) {
                appendMessage(data.content, "assistant");
            } else if (data && data.error) {
                console.error("API returned an error:", data.error);
                appendMessage("An error occurred: " + data.error, "assistant");
            } else {
                console.error("Unexpected response format:", data);
                appendMessage("Received an unexpected response format.", "assistant");
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
            appendMessage("La conversazione è stata resettata correttamente, puoi iniziarne una nuova.🎉", "system");
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


    /**
    * Toggles dark mode and updates the UI accordingly.
    * This function handles the dark mode toggle functionality, including:
    * - Switching between light and dark themes
    * - Updating the UI (body classes and icon visibility)
    * - Persisting the user's preference in localStorage
    * - Initializing the theme based on the user's previous preference or system preference
    * */
   function initializeDarkMode() {
     const bodyElement = document.body;
     const switchElement = document.getElementById("darkModeSwitch");
     const darkIcon = document.querySelector(".fa-moon");
     const lightIcon = document.querySelector(".fa-sun");
     const docsLink = document.getElementById("nav-docs");
     const homeLink = document.getElementById("nav-home");
     footerDark = document.getElementById("footer-dark");

      // Function to set the theme
     function setTheme(isDark) {
        bodyElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
        localStorage.setItem('bsTheme', isDark ? 'dark' : 'light');
        darkIcon.classList.toggle('d-none', !isDark);
        lightIcon.classList.toggle('d-none', isDark);
        bodyElement.classList.toggle('bg-dark', isDark);
        bodyElement.classList.toggle('text-white', isDark);
        docsLink.classList.toggle('custom-hover-dark', isDark);
        homeLink.classList.toggle('custom-hover-dark', isDark);
        footerDark.classList.toggle('text-white', isDark);
        switchElement.checked = !isDark;
     }

     // Initialize theme based on localStorage or system preference
     const storedTheme = localStorage.getItem('bsTheme');
     const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
     const initialTheme = storedTheme || (prefersDarkScheme ? 'dark' : 'light');
     setTheme(initialTheme === 'dark');
 
     // Event listener for theme toggle
     switchElement.addEventListener("change", () => setTheme(!switchElement.checked));

     // Listen for system theme changes
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('bsTheme')) {
            setTheme(e.matches);
        }
      });
    }
    
    initializeDarkMode();
    
    //se il bottone dellla nav è cliccato, allora aggiungi alla class custom box-shadow: 4px 4px 8px #0D6EFD; così dà indizacione del menu di navigazione 




