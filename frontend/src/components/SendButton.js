import React from "react";
import {handleSend } from '../utils/sendInputs';

const SendButton = ({input, messages, setMessages, setInput, setLoading, model}) => {
  return (
    <button
      onClick={() => handleSend(input, messages, setMessages, setInput, setLoading, model)}
      className="ml-2 p-2 bg-blue-500 text-white rounded hover:bg-sky-700 "
    >
      Invia
    </button>
  );
};


export default SendButton;