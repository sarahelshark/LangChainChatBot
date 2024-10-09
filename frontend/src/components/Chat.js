import { useState} from 'react';
import useResetConversation from '../hooks/useResetConversation';
import SelectModel from './SelectModel';
import MessageList from './MessageList'; 
import FormInput from './FormInput';     
const chatInfo = {
  title: "Welcome to the Chatbot",
};

const Chat = () => {
  const {
    messages,
    setMessages,
    input,
    setInput,
    resetConversation,
  } = useResetConversation();

  const [loading, setLoading] = useState(false);  
  const [model, setModel] = useState('chatgpt'); //default 

  return (
    <section className="mt-8 mx-5 md:mx-11">
      <h1 className="text-2xl font-bold mb-4 text-center">{chatInfo.title}</h1>
      <SelectModel model={model} setModel={setModel}/>
      <MessageList messages={messages} loading={loading} />
      <FormInput 
        input={input} 
        setInput={setInput} 
        messages={messages} 
        setMessages={setMessages} 
        setLoading={setLoading} 
        model={model} 
        resetConversation={resetConversation}
      />
    </section>
  );
};

export default Chat;
