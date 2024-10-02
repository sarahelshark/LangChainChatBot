
const MessageList = ({ messages, loading }) => {
    return (
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
        {loading && <div className="loader"></div>} 
      </div>
    );
  };
  
  export default MessageList;
  