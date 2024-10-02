import { useState, useEffect } from 'react';
import { sendEnter } from '../utils/sendInputs';
import SendButton from './SendButton';
import ResetButton from './ResetButton';
import UploadButton from './UploadButton';
import useResetConversation from '../hooks/useResetConversation';
import SelectModel from './SelectModel';

const Chat = () => {
  const {
    messages,
    setMessages,
    input,
    setInput,
    resetConversation,
  } = useResetConversation();

  const [loading, setLoading] = useState(false);  
  const [model] = useState('chatgpt');   

  return (
    <section className="mt-8 mx-5 md:mx-11">
      <h1 className="text-2xl font-bold mb-4 text-center">Welcome to the Chatbot</h1>
       <SelectModel/>
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
          <p className="text-gray-500 text-center">Start a conversation! When you're done, type 'exit'...</p>
        )}
        {loading && <div className="loader"></div>}  {/* Display loader when loading is true */}
      </div>

      {/* Input and buttons */}
      <div className="mt-4 flex">
        <label htmlFor="formInput" className="sr-only">
          User input
        </label>
        <input
          name="formInput"
          id="formInput"
          type="text"
          className="flex-grow p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          value={input}
          onKeyDown={(e) => sendEnter(e, input, messages, setMessages, setInput, setLoading , model)}  
          onChange={(e) => setInput(e.target.value)}
          placeholder="Write a message..."
        />
        <SendButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} setLoading={setLoading} model={model}  />
        <ResetButton resetConversation={resetConversation} />
      </div>

      <UploadButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} />
    </section>
  );
};

export default Chat;
