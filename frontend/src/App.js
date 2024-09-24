
import React, { useState, useEffect } from 'react';
import './index.css';
import Footer from './components/Footer';
import ChatOffCanvas from './components/ChatOffCanvas';
import Navbar from './components/Navbar';
import Chat from './components/Chat';


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
          <Chat/>
        </main>
      </div>
      <ChatOffCanvas isOpen={chatOpen} onClose={toggleChat} />
      <Footer />
      
    </div>
  );
};

export default App;