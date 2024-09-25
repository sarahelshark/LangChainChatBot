import React, { useState } from 'react';
import {sendEnter} from '../utils/sendInputs';
import SendButton from './SendButton';
import ResetButton from './ResetButton';
import UploadButton from './UploadButton';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const resetConversation = () => {
    setMessages([]);
    setInput('');
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
        <SendButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} />
        <ResetButton resetConversation={resetConversation} />
      </div>
        <UploadButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} />
    </section>
  );
};

export default Chat;