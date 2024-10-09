import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { deleteConversation } from '../utils/deleteConversation';

const ChatOffCanvas = ({ isOpen, onClose }) => {
  const [conversations, setConversations] = useState([]); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); 
  const [model, setModel] = useState('chatgpt'); // Default 
  

  const loadOldChats = async (modelType) => {
    setLoading(true); 
    setError(null); 
    setConversations([]); 

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/get_old_chats?model=${modelType}&offset=0&limit=3`); // Fetch API
      const data = await response.json();

      if (response.ok) {
        setConversations(data.conversations || []); 
      } else {
        setError(data.error || 'Failed to load conversations'); 
      }
    } catch (err) {
      setError('Error fetching conversations: ' + err.message); 
    } finally {
      setLoading(false);
    }
  };



  useEffect(() => {
    if (isOpen) {
      loadOldChats(model); 
    }
  }, [isOpen, model]); 

  return (
    <div
      className={`fixed inset-y-0 overflow-y-auto  right-0 sm:w-full md:w-80 lg:w-80 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
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
      <div className="p-6">
        {loading && <p className='text-white'>Loading chats...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        {!loading && !error && (
          conversations.length > 0 ? (
            <ul>
              {conversations.map((conversation) => (
                <li key={conversation.id} className="mb-5 dark:text-white">
                  <div className="card mb-3">
                    <div className="card-body shadow-xl">
                      
                    <div className="flex justify-end items-center p-4 border-b border-gray-200 dark:border-gray-700">
                      <button onClick={() => deleteConversation(conversation.id, model, setConversations)} className="p-1 rounded-full text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700">
                        <X size={12} />
                        </button>
                    </div>
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
