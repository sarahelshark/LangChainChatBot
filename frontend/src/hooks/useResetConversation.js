import { useState } from 'react';

const useResetConversation = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const resetConversation = () => {
    setMessages([]);
    setInput('');
  };

  return {
    messages,
    setMessages,
    input,
    setInput,
    resetConversation,
  };
};

export default useResetConversation;