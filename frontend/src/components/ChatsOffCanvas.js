import React, { useState, useEffect } from 'react';
import ChatHeader from './ChatsHeader';
import ChatContent from './ChatsContent';
import SelectModel from './SelectModel';

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
      className={`fixed inset-y-0 overflow-y-auto right-0 sm:w-full md:w-80 lg:w-80 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
        isOpen ? 'translate-x-0' : 'translate-x-full'
      }`}
    >
      <ChatHeader onClose={onClose} />
      <div className="p-4">
        <SelectModel model={model} setModel={setModel} />
      </div>
      <div className="p-6">
        <ChatContent 
          loading={loading}
          error={error}
          conversations={conversations}
          model={model}
          setConversations={setConversations}
        />
      </div>
    </div>
  );
};

export default ChatOffCanvas;
