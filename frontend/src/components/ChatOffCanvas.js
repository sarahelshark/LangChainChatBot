import React from 'react';
import { X } from 'lucide-react';

const ChatOffCanva = ({ isOpen, onClose }) => (
  <div
    className={`fixed inset-y-0 right-0 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
      isOpen ? 'translate-x-0' : 'translate-x-full'
    }`}
  >
    <div className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Chat</h2>
      <button onClick={onClose} className="p-1 rounded-full text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700">
        <X size={24} />
      </button>
    </div>
    <div className="p-4 text-gray-900 dark:text-white">
      <p>Chat content goes here</p>
    </div>
  </div>
);

export default ChatOffCanva;