import './index.css';
import React, { useState, useEffect } from 'react';
import { Moon, Sun, MessageSquare, FileText, Home, X } from 'lucide-react';

const NavItem = ({ icon: Icon, label, onClick }) => (
  <button
    className="flex items-center space-x-2 px-4 py-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
    onClick={onClick}
  >
    <Icon size={20} />
    <span>{label}</span>
  </button>
);

const Navbar = ({ darkMode, toggleDarkMode, toggleChat }) => (
  <nav className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
    <div className="flex space-x-4">
      <NavItem icon={Home} label="Home" />
      <NavItem icon={MessageSquare} label="Chat" onClick={toggleChat} />
      <NavItem icon={FileText} label="Docs" />
    </div>
    <button
      onClick={toggleDarkMode}
      className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
    >
      {darkMode ? <Sun size={24} /> : <Moon size={24} />}
    </button>
  </nav>
);

const ChatOffCanvas = ({ isOpen, onClose }) => (
  <div
    className={`fixed inset-y-0 right-0 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
      isOpen ? 'translate-x-0' : 'translate-x-full'
    }`}
  >
    <div className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Chat</h2>
      <button onClick={onClose} className="p-1 rounded-full text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700">
        <X size={24} />
      </button>
    </div>
    <div className="p-4 text-gray-900 dark:text-white">
      <p>Chat content goes here</p>
    </div>
  </div>
);

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input) {
      setMessages([...messages, { text: input, sender: 'User' }]);
      setInput('');
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4">Chat</h2>
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
          <p className="text-gray-500">Inizia una conversazione!</p>
        )}
      </div>
      <div className="mt-4 flex">
        <input
          type="text"
          className="flex-grow p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Scrivi un messaggio..."
        />
        <button
          onClick={handleSend}
          className="ml-2 p-2 bg-blue-500 text-white rounded"
        >
          Invia
        </button>
      </div>
    </div>
  );
};

const Footer = () => (
  <footer className="bg-gray-200 dark:bg-gray-800 text-center p-4 mt-auto">
    <p className="text-gray-600 dark:text-gray-400">&copy; 2024 Chatbot App. All rights reserved.</p>
  </footer>
);

const App = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);

  const saveThemePreference = (isDarkMode) => {
    localStorage.setItem('darkMode', isDarkMode ? 'true' : 'false');
  };

  const toggleChat = () => setChatOpen(!chatOpen);

  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode) {
      setDarkMode(savedDarkMode === 'true');
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    saveThemePreference(newDarkMode);
  };

  return (
    <div className={`min-h-screen flex flex-col ${darkMode ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white flex-grow">
        <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} toggleChat={toggleChat} />
        <main className="p-4 flex-grow">
          <h1 className="text-2xl font-bold mb-4">Welcome to the Chatbot</h1>
          <p>
            This is a simple chatbot application built with React and Tailwind CSS. Click on the chat
            button in the navigation bar to open the chat interface.
          </p>
          <Chat />
        </main>
      </div>
      <Footer />
      <ChatOffCanvas isOpen={chatOpen} onClose={toggleChat} />
    </div>
  );
};

export default App;