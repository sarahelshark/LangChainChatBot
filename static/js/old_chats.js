

document.addEventListener('DOMContentLoaded', function() {
    
  function updateNavActiveState(clickedNavId) {
      const navItems = document.querySelectorAll('.navbar-nav .nav-link');
      navItems.forEach(item => item.classList.remove('active'));
      document.getElementById(clickedNavId).classList.add('active');
    }
    document.getElementById("nav-home").addEventListener("click", () => updateNavActiveState('nav-home'));
    document.getElementById("nav-docs").addEventListener("click", () => updateNavActiveState('nav-docs'));
  
    const oldChatsNavItem = document.getElementById("nav-old-chats");
    oldChatsNavItem.addEventListener("click", () => updateNavActiveState('nav-old-chats'));
  
    const oldChatsOffcanvas = document.getElementById('oldChatsOffcanvas');
    const oldChatModelSelect = document.getElementById('oldChatModelSelect');
  
    async function loadOldChats(modelType) {
      const loader = document.getElementById('loaderOldChats');
      const oldChatsContent = document.getElementById('oldChatsContent');
      
      // Show loader
      loader.classList.remove("d-none");
      oldChatsContent.innerHTML = '';

      

      try {
        const response = await fetch(`/api/get_old_chats?model=${modelType}`);
        const data = await response.json();
  
        if (data.conversations && data.conversations.length > 0) {
          data.conversations.forEach(conversation => {
            const conversationElement = document.createElement('div');
            conversationElement.id = `conversation-${conversation.id}`;
            conversationElement.className = 'card mb-3';
            conversationElement.innerHTML = `
              <div class="card-body">
                <button type="button" class="btn-close float-end" aria-label="Close" onclick="confirmDeleteConversation(${conversation.id}, '${modelType}')"></button>
                <p class="card-text">${conversation.content}</p>
              </div>
            `;
            oldChatsContent.appendChild(conversationElement);
          });
        } else {
          oldChatsContent.innerHTML = '<p>Nessuna conversazione precedente trovata.</p>';
        }
      } catch (error) {
        console.error('Errore nel recupero delle vecchie conversazioni:', error);
        oldChatsContent.innerHTML = '<p class="text-danger">Errore nel caricamento delle vecchie conversazioni.</p>';
      } finally {
        // Hide loader
        loader.classList.add("d-none");
      }
    }
  
    oldChatsOffcanvas.addEventListener('show.bs.offcanvas', function () {
      updateNavActiveState('nav-old-chats');
      loadOldChats(oldChatModelSelect.value);
    });
  
    oldChatModelSelect.addEventListener('change', function() {
      loadOldChats(this.value);
    });
  
    async function deleteConversation(id, model) {
      console.log('Deleting conversation', id, model);
      try {
        const response = await fetch('/api/delete_conversation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id, model }),
        });

        const data = await response.json();
  
        if (!response.ok) {
          throw new Error(data.error || 'Failed to delete conversation');
        }
  
        // Remove the conversation element from the DOM
        const conversationElement = document.getElementById(`conversation-${id}`);
        if (conversationElement) {
          conversationElement.remove();
        }
  
        console.log('Conversation deleted successfully');
        // Show a success message to the user
        alert('Conversation deleted successfully');
      } catch (error) {
        console.error('Error deleting conversation:', error);
        alert(`Failed to delete conversation: ${error.message}`);
      }
    }
  
    // Confirmation dialog function
    window.confirmDeleteConversation = function(id, model) {
      if (confirm('Are you sure you want to delete this conversation?')) {
        deleteConversation(id, model);
      }
    };
  
    // Make deleteConversation function globally available
    window.deleteConversation = deleteConversation;
  });