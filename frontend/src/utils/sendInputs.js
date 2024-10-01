export function handleSend(input, messages, setMessages, setInput, setLoading) {
  if (input.trim() !== '' && input) {
    const newMessages = [...messages, { sender: 'User', text: input }];
    setMessages(newMessages);  // Update the chat with the user's message
    setInput('');  
    setLoading(true);  // Show the loader

    fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: input,
        model: 'chatgpt'  // or 'gemini' 
      }),
    })
    .then(response => response.json())
    .then(data => {
      setLoading(false);  // Hide the loader

      if (data.error) {
        setMessages([...newMessages, { sender: 'AI', text: 'Error: ' + data.error }]);
      } else {
        const aiMessage = { sender: 'AI', text: data.content };
        setMessages([...newMessages, aiMessage]);  // Append AI's response to the chat
      }
    })
    .catch(error => {
      console.error('Error:', error);
      setLoading(false);  // Hide the loader on error
      setMessages([...newMessages, { sender: 'AI', text: 'Error: Could not reach the server.' }]);
    });
  }
}

export const sendEnter = async (e, input, messages, setMessages, setInput, setLoading) => {
  if (e.key === 'Enter' && input.trim() !== '' && input) {
    e.preventDefault();
    handleSend(input, messages, setMessages, setInput, setLoading); 
  }
};