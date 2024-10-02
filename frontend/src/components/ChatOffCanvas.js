import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';

const ChatOffCanvas = ({ isOpen, onClose }) => {
  const [conversations, setConversations] = useState([]); // Store fetched conversations
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state
  const [model, setModel] = useState('chatgpt'); // Default model (chatgpt)
  
  // Function to fetch old chats (Similar to loadOldChats in my vanilla JS)
  const loadOldChats = async (modelType) => {
    setLoading(true); // Show loader
    setError(null); // Reset previous errors
    setConversations([]); // Clear previous conversations

    try {

      const response = await fetch(`http://127.0.0.1:5000/api/get_old_chats?model=${modelType}&offset=0&limit=3`); // Fetch API
      const data = await response.json();

      if (response.ok) {
        setConversations(data.conversations || []); // Set the conversations
      } else {
        setError(data.error || 'Failed to load conversations'); // Handle API error
      }
    } catch (err) {
      setError('Error fetching conversations: ' + err.message); // Catch any other error
    } finally {
      setLoading(false); // Hide loader
    }
  };

  // Function to delete a specific conversation?
  const deleteConversation = async (uid, modelType) => {
    try {
      const response = await fetch(`/api/delete_conversation?model=${modelType}&uids_to_delete=${uid}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uids_to_delete: [uid], model_type: modelType }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete conversation');
      }

      // Remove deleted conversation from the state
      setConversations((prevConversations) => prevConversations.filter(convo => convo.id !== uid));

      alert('Conversation deleted successfully');
    } catch (error) {
      console.error('Error deleting conversation:', error);
      alert(`Failed to delete conversation: ${error.message}`);
    }
  };

  // Fetch chats when the component (off-canvas) is shown (similar to 'show.bs.offcanvas' in vanilla JS)
  useEffect(() => {
    if (isOpen) {
      loadOldChats(model); // Fetch old chats for the current model
    }
  }, [isOpen, model]); // Re-fetch if model changes

  return (
    <div
      className={`fixed inset-y-0 right-0 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
        isOpen ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
      <div className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Chat</h2>
        <button
          onClick={onClose}
          className="p-1 rounded-full text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700"
        >
          <X size={24} />
        </button>
      </div>

      {/* Model Select Dropdown */}
      <div className="p-4">
        <label htmlFor="oldChatModelSelect" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Choose AI model:
        </label>
        <select
          id="oldChatModelSelect"
          value={model}
          onChange={(e) => setModel(e.target.value)} // Update model when selected
          className="p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white"
        >
          <option value="chatgpt">ChatGPT</option>
          <option value="gemini">Gemini</option>
        </select>
      </div>

      {/* Chat Content */}
      <div className="p-4">
        {loading && <p>Loading chats...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        {!loading && !error && (
          conversations.length > 0 ? (
            <ul>
              {conversations.map((conversation) => (
                <li key={conversation.id} className="mb-2">
                  <div className="card mb-3">
                    <div className="card-body">
                      <button
                        type="button"
                        className="btn-close float-end"
                        aria-label="Close"
                        onClick={() => deleteConversation(conversation.id, model)} // Attach delete function
                      ></button>
                      <p className="card-text">{conversation.content}</p>
                      <p className="blockquote-footer">{new Date(conversation.timestamp).toLocaleString()}</p>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No previous conversations found.</p>
          )
        )}
      </div>
    </div>
  );
};

export default ChatOffCanvas;
