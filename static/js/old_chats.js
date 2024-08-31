/**
 * Updates the active state of the navigation items.
 * @param {string} clickedNavId -   Id of the clicked navigation item
 */
function updateNavActiveState(clickedNavId) {
  const navItems = document.querySelectorAll('.navbar-nav .nav-link');
  navItems.forEach(item => item.classList.remove('active'));
  document.getElementById(clickedNavId).classList.add('active');
}

// add an event listener to the navigation elements
document.getElementById("nav-home").addEventListener("click", () => updateNavActiveState('nav-home'));
document.getElementById("nav-docs").addEventListener("click", () => updateNavActiveState('nav-docs'));

const oldChatsNavItem = document.getElementById("nav-old-chats");
oldChatsNavItem.addEventListener("click", () => updateNavActiveState('nav-old-chats'));

const oldChatsOffcanvas = document.getElementById('oldChatsOffcanvas');
const oldChatModelSelect = document.getElementById('oldChatModelSelect');

/**
 * Loads the previous conversations for the selected model.
 * @param {string} modelType - Model type for which to load the old chats
 */
async function loadOldChats(modelType) {
  const loader = document.getElementById('loaderOldChats');
  const oldChatsContent = document.getElementById('oldChatsContent');   
  // Show loader
  loader.classList.remove("d-none");
  oldChatsContent.innerHTML = '';
  try {
      const response = await fetch(`/api/get_old_chats?model=${modelType}`);
      const data = await response.json();
      console.log('Old chats:', data);
      if (data.conversations && data.conversations.length > 0) {
        data.conversations.forEach(conversation => {
          const conversationElement = document.createElement('div');
          conversationElement.id = `conversation-${conversation.id}`;
          conversationElement.className = 'card mb-3';
          conversationElement.innerHTML = `
            <div class="card-body">
              <button type="button" class="btn-close float-end" aria-label="Close" onclick="deleteConversation('${conversation.id}', '${modelType}')"></button>
              <p class="card-text">${conversation.content}</p>
              <p class="blockquote-footer">${conversation.timestamp}</p>
          </div>
          `;
          oldChatsContent.appendChild(conversationElement);
        });
      } else {
        oldChatsContent.innerHTML = '<p>Nessuna conversazione precedente trovata.</p>';
      }} catch (error) {
        console.error('Errore nel recupero delle vecchie conversazioni:', error);
        oldChatsContent.innerHTML = '<p class="text-danger">Errore nel caricamento delle vecchie conversazioni.</p>';
      } finally {
        // Hide loader
        loader.classList.add("d-none");
      }
  
} 
/**
* Adds a listener for the 'show.bs.offcanvas' event on the oldChatsOffcanvas element.
* When the offcanvas is shown, updates the active state of the navigation and loads the old conversations.
*/
oldChatsOffcanvas.addEventListener('show.bs.offcanvas', function () {
  updateNavActiveState('nav-old-chats');
  loadOldChats(oldChatModelSelect.value);
});
  
/**
* Adds a listener for the 'change' event on the oldChatModelSelect element.
* When the selected model changes, loads the old conversations based on the newly selected model.
*/
oldChatModelSelect.addEventListener('change', function() {
  loadOldChats(this.value);
});
  
  
/**
* DELETES a specific conversation 
* @param {string} model - Model type of the conversation to be deleted
* @param {number} uid - ID of the conversation to be deleted
*/
async function deleteConversation(uid,model) {
  if (!model || !uid) {
    alert("Invalid model or UID");
    return;
  }
  console.log('Deleting conversation', uid, model);
  try {
    const response = await fetch(`/api/delete_conversation?model=${model}&uids_to_delete=${uid}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({  uids_to_delete: [uid], model_type: model }),
    });
    const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete conversation');
      }
      //Remove the conversation element from the DOM
      const conversationElement = document.getElementById(`conversation-${uid}`);
      if (conversationElement) {
        conversationElement.remove();
        const oldChatsContent = document.getElementById('oldChatsContent');
        oldChatsContent.innerHTML = '<p>Nessuna conversazione precedente trovata.</p>';
      }
      console.log('Conversation deleted successfully');
      alert('Conversation deleted successfully');
    } catch (error) {
      console.error('Error deleting conversation:', error);
      alert(`Failed to delete conversation: ${error.message}`);
    }
};
  