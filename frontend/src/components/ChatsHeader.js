import React from 'react';
import { X } from 'lucide-react';

const ChatHeader = ({ onClose }) => (
  <div className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
    <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Chat</h2>
    <button
      onClick={onClose}
      className="p-1 rounded-full text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700"
    >
      <X size={24} />
    </button>
  </div>
);

export default ChatHeader;
