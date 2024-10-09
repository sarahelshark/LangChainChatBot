import React from 'react';
import { X } from 'lucide-react';
import { deleteConversation } from '../utils/deleteConversation';

const ChatContent = ({ loading, error, conversations, model, setConversations }) => {
  if (loading) return <p className='text-white'>Loading chats...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
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
  );
};

export default ChatContent;
