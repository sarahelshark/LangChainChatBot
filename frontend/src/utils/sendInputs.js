export function handleSend (input, messages, setMessages, setInput) {
    if (input) {  
      setMessages([...messages, { text: input, sender: 'User' }]);
      setInput('');
    };
  };

export function sendEnter(e, input, messages, setMessages, setInput){
    if (e.key === 'Enter') {
      handleSend(input, messages, setMessages, setInput);
    }
  }

 