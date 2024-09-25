import React, { useState } from 'react';
import {handleSend , sendEnter} from '../utils/sendInputs';
import { ArrowUp } from 'lucide-react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const resetConversation = () => {
    setMessages([]);
    setInput('');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    // Handle the file upload logic here
    console.log('File uploaded:', file);
  };

  return (
    <section className="mt-8 mx-5 md:mx-11">
      <h1 className="text-2xl font-bold mb-4 text-center">Welcome to the Chatbot</h1>
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
          <p className="text-gray-500 text-center">Inizia una conversazione!</p>
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
          onKeyDown={(e) => sendEnter(e, input, messages, setMessages, setInput)}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Scrivi un messaggio..."
        />
        <button
          onClick={() => handleSend(input, messages, setMessages, setInput)}
          className="ml-2 p-2 bg-blue-500 text-white rounded"
        >
          Invia
        </button>
        <button
          onClick={resetConversation}
          className="ml-2 p-2 border border-red-500 text-red-500 rounded"
        >
          Reset
        </button>
      </div>
      <div className="upload flex items-center mt-2">
        <label className="upload-area">
          <input
            type="file"
            className="hidden"
            id="fileUpload"
            onChange={handleFileUpload}
          />
          <span className="upload-button btn ">
            <ArrowUp className="text-xl" />
          </span>
        </label>
      </div>
    </section>
  );
};

export default Chat;