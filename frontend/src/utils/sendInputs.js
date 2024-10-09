export function handleSend(input, messages, setMessages, setInput, setLoading, model) {
  if (input.trim() !== '' && input) {
    const newMessages = [...messages, { sender: 'User', text: input }];
    setMessages(newMessages);
    setInput(''); 
    setLoading(true);  //show loader

    fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: input,
        model: model, 
      }),
    })
    .then(response => response.json())
    .then(data => {
      setLoading(false);  
      if (data.error) {
        setMessages([...newMessages, { sender: 'AI', text: 'Error: ' + data.error }]);
      } else {
        const aiMessage = { sender: 'AI', text: data.content };
        setMessages([...newMessages, aiMessage]); 
      }
    })
    .catch(error => {
      console.error('Error:', error);
      setLoading(false); 
      setMessages([...newMessages, { sender: 'AI', text: 'Error: Could not reach the server.' }]);
    });
  }
}

export const sendEnter = async (e, input, messages, setMessages, setInput, setLoading, model) => {
  if (e.key === 'Enter' && input.trim() !== '' && input) {
    e.preventDefault();
    handleSend(input, messages, setMessages, setInput, setLoading, model); 
  }
};