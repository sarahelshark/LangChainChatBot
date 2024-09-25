import React, { useState } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input) {
      setMessages([...messages, { text: input, sender: 'User' }]);
      setInput('');
    }
  };

  return (
    <div className="mt-8">
      <h1 className="text-2xl font-bold mb-4">Welcome to the Chatbot</h1>
      <div className="h-64 p-4 bg-gray-100 dark:bg-gray-700 overflow-y-auto rounded">
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`p-2 rounded mb-2 ${msg.sender === 'User' ? 'bg-blue-200 dark:bg-blue-600' : 'bg-gray-200 dark:bg-gray-600'}`}
            >
              {msg.text}
            </div>
          ))
        ) : (
          <p className="text-gray-500">Inizia una conversazione!</p>
        )}
      </div>
      <div className="mt-4 flex">
        <label htmlFor="formInput" className="sr-only">
          user input
        </label>
        <input
          name='formInput'
          id='formInput'
          type="text"
          className="flex-grow p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Scrivi un messaggio..."
        />
        <button
          onClick={handleSend}
          className="ml-2 p-2 bg-blue-500 text-white rounded"
        >
          Invia
        </button>
      </div>
    </div>
  );
};

export default Chat;