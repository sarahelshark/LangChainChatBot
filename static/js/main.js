//chatbox elements
const chatbox = document.getElementById("chatbox");
const placeholder = document.getElementById("placeholder");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const bodyElement = document.body;

//theme elements
const switchElement = document.getElementById("darkModeSwitch");
const darkIcon = document.querySelector(".fa-moon");
const lightIcon = document.querySelector(".fa-sun");
const docsLink = document.getElementById("nav-docs");
const homeLink = document.getElementById("nav-home");
const footerDark = document.getElementById("footer-dark");
initializeDarkMode();

//create model select element
const modelSelect = document.createElement("select");
modelSelect.id = "modelSelect";
modelSelect.classList.add("border-primary");


/**
* Initializes the reset button and adds it to the DOM, Then an event listener is applied and triggers the resetConversation() funct.
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
* Initializes the model selection dropdown and adds it to the DOM, Then an event is triggered whether the selected option is Chatgpt or Gemini, an overlay with the chosen model is added in order to give give a feedback .
*/
function initializeModelSelect() {
    const chatgptOption = document.createElement("option");
    chatgptOption.value = "chatgpt";
    chatgptOption.textContent = "ChatGPT";

    const geminiOption = document.createElement("option");
    geminiOption.value = "gemini";
    geminiOption.textContent = "Gemini";

    modelSelect.append(chatgptOption, geminiOption);
    sendButton.parentNode.insertBefore(modelSelect, sendButton);

    feedbackOverlay();
}
/**
* An overlay gives a visual feedback to the user when the model is selected.
*/
function feedbackOverlay() {
    modelSelect.addEventListener("change", () => {
        console.log("Selected model:", modelSelect.value);

        const overlayHTML = `
            <div id="overlay">
                <div id="overlay-text" class="display-1">
                    ${modelSelect.value}
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', overlayHTML);
        const overlay = document.getElementById("overlay");

        // Aggiungi la classe 'hidden' per nascondere l'overlay dopo 2 secondi
        setTimeout(() => {
            overlay.classList.add("hidden");
            // Rimuovi l'overlay dal DOM dopo che l'animazione di nascondimento è completata
            setTimeout(() => {
                overlay.remove();
            }, 200); 
        }, 500);

        // Pulisci il contenuto della chatbox
        chatbox.innerHTML = '';
    });
}
/**
* sets dark mode theme style elements
* @param {boolean} isDark - The theme to set.
*/
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
// Event listener for theme toggle
switchElement.addEventListener("change", () => setTheme(!switchElement.checked));

/**
* Toggles dark mode theme based on the user's preference (persisted in localStorage).
* */
function initializeDarkMode() {
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
// Event listener for navigation
document.getElementById("nav-docs").addEventListener("click", homeNotActive);

/**
* Appends a new message to the chatbox.
* @param {string} content - The content of the message.
* @param {string} sender - The sender of the message.
*/
function appendMessage(content, sender) {
    const messageElement = document.createElement("div");
    messageElement.className = `message ${sender}`; 
    if (sender === "system") {
        messageElement.className = `message-system`;
        setTimeout(() => {
            messageElement.style.display = "none";  
        }, 3000);           
    }
    messageElement.innerText = content;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

/**
* Creates and appends a loader element to the document body.
* @function
* @name createLoader
* @description This function creates a new div element with the class 'loader' and appends it to the document body.
*  
*/
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
    const input = getUserInput();
    if (!input) return;

    const loader = showLoader();
    appendMessage(input, "user");
    clearUserInput();
    hidePlaceholder();

    try {
        const response = await sendChatRequest(input);
        const data = await handleResponse(response);
        processResponseData(data);
    } catch (error) {
        handleError(error);
    } finally {
        hideLoader(loader);
    }
}
//helper functions for sendMesssage()
function getUserInput() {
    return userInput.value.trim();
}
function clearUserInput() {
    userInput.value = "";
}
function hidePlaceholder() {
    placeholder.style.display = "none";
}
function showLoader() {
    const loader = createLoader();
    loader.classList.remove("d-none");
    return loader;
}
function hideLoader(loader) {
    loader.classList.add("d-none");
    setTimeout(() => loader.remove(), 300); // Remove after transition
}
async function sendChatRequest(input) {
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

    return response;
}
async function handleResponse(response) {
    return await response.json();
}
function processResponseData(data) {
    if (data && data.content) {
        appendMessage(data.content, "assistant");
    } else if (data && data.error) {
        appendMessage("An error occurred: " + data.error, "assistant");
    } else {
        appendMessage("Received an unexpected response format.", "assistant");
    }
}
function handleError(error) {
    console.log("Error processing request:", error);
    appendMessage("Sorry, there was an error processing your request.", "assistant");
}


/**
* Resets the conversation by making a POST request to the '/api/reset' endpoint.
* @async
* @function resetConversation
* @description Clears the chatbox and displays a message indicating that the conversation has been reset.
* If an error occurs during the reset process, an error message is displayed.
*/
async function resetConversation() {
    try {
        const modelType = getModelType();
        const response = await sendResetRequest(modelType);
        const data = await handleResetResponse(response);
        clearChatbox();
        logStatus(data.status);
        notifyUser("La conversazione è stata resettata correttamente, puoi iniziarne una nuova.🎉");
    } catch (error) {
        handleError(error);
    }
}
//helper functions for resetConversation()
async function handleResetResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}
function getModelType() {
    return modelSelect.value;
}
async function sendResetRequest(modelType) {
    return await fetch('/api/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: modelType }),
    });
}
async function handleResetResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}
function clearChatbox() {
    chatbox.innerHTML = '';
}
function logStatus(status) {
    console.log(status);
}
function notifyUser(message) {
    appendMessage(message, "system");
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

// docs page

/**
* Fetches and renders the content of README.md file in the '/static/images/' directory.
* @async
* @function fetchReadmeContent
* @description This function performs an HTTP GET request to fetch the content of
* the README.md file from the '/static/images/' directory. It then parses the
* markdown content and renders it as HTML in the element with id 'readme-content'.
* @throws {Error} Throws an error if the HTTP request fails.
* @requires marked - A library for parsing markdown into HTML. It is included via cdn in the index.html file.
*/
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



