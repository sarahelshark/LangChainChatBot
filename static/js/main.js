
    const chatbox = document.getElementById("chatbox");
    const placeholder = document.getElementById("placeholder");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");

    // Initialize GLOBAL UI elements
    
    initializeDarkMode();

    /**
     * Initializes the reset button and adds it to the DOM.
     */
    function initializeResetButton() {
        const resetButton = document.createElement("button");
        resetButton.classList.add("btn", "border", "border-danger", "btn-outline-danger", "rounded");
        resetButton.textContent = "Reset Conversation";
        resetButton.style.marginLeft = "10px";
        sendButton.insertAdjacentElement('afterend', resetButton);
        resetButton.addEventListener("click", resetConversation);
    }

    /**
     * Initializes the model selection dropdown and adds it to the DOM.
     */
    function initializeModelSelect() {
        const modelSelect = document.createElement("select");
        modelSelect.id = "modelSelect";
        modelSelect.classList.add("border-primary");

        const chatgptOption = document.createElement("option");
        chatgptOption.value = "chatgpt";
        chatgptOption.textContent = "ChatGPT";

        const geminiOption = document.createElement("option");
        geminiOption.value = "gemini";
        geminiOption.textContent = "Gemini";

        modelSelect.append(chatgptOption, geminiOption);
        sendButton.parentNode.insertBefore(modelSelect, sendButton);
    }

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

    function createLoader() {
        const loader = document.createElement('div');
        loader.className = 'loader d-none';
        document.body.appendChild(loader);
        return loader;
    }

    /**
     * Sends a message to the chat API and appends the user's message to the chat window.
     * @async
     * @function sendMessage
     */
    async function sendMessage() {
        const loader = createLoader();
        
        const input = userInput.value.trim();
        if (!input) return;
        
        appendMessage(input, "user");
        userInput.value = "";
        placeholder.innerHTML = '';

         // Show loader
        loader.classList.remove("d-none");

        try {
            console.log("Sending request to /api/chat");
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input, model: modelSelect.value }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data && data.content) {
                appendMessage(data.content, "assistant");
            } else if (data && data.error) {
                appendMessage("An error occurred: " + data.error, "assistant");
            } else {
                appendMessage("Received an unexpected response format.", "assistant");
            }
        } catch (error) {
            appendMessage("Sorry, there was an error processing your request.", "assistant");
        }  finally {
            // Hide loader 
            loader.classList.add("d-none");
            setTimeout(() => loader.remove(), 300); // Remove after transition
        }
    }

    /**
     * Resets the conversation by making a POST request to the '/api/reset' endpoint.
     * Clears the chatbox and displays a message indicating that the conversation has been reset.
     * If an error occurs during the reset process, an error message is displayed.
     */
    async function resetConversation() {
        try {
            const modelType = modelSelect.value; // Ottieni il modello selezionato
            const response = await fetch('/api/reset', {
                method: 'POST',   
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ model: modelType }), // Invia il tipo di modello
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            chatbox.innerHTML = ''; 
            console.log(data.status);
            appendMessage("La conversazione è stata resettata correttamente, puoi iniziarne una nuova.🎉", "system");
        } catch (error) {
            console.error("Error resetting conversation:", error);
            appendMessage("Sorry, there was an error resetting the conversation.", "system");
        }
    }
    
    /**
     * Initializes event listeners for the send button and user input.
     */
    function initializeEventListeners() {
        sendButton.addEventListener("click", sendMessage);
        userInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    }

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
     const footerDark = document.getElementById("footer-dark");

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
    
    /**
    * Handles the navigation state by updating the active class on navigation items.
    */
    function homeNotActive() {
        document.getElementById("nav-home").classList.remove("active");
        document.getElementById("nav-docs").classList.add("active");
    }
    document.getElementById("nav-docs").addEventListener("click", homeNotActive);


    function fetchReadmeContent() {
            fetch('/static/images/README.md')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(markdown => {
                    const readmeContent = document.getElementById('readme-content');
                    readmeContent.innerHTML = marked.parse(markdown);
                })
                .catch(error => {
                    console.error('Error fetching and rendering README.md:', error);
                    const readmeContent = document.getElementById('readme-content');
                    readmeContent.innerHTML = '<p class="text-danger">Error loading README.md content.</p>';
                });
        }



