
import React, { useState, useEffect } from 'react';
import './index.css';
import Navbar from './components/Navbar';
import Chat from './components/Chat';
import ChatOffCanvas from './components/ChatOffCanvas';
import Docs from './components/Docs';
import Footer from './components/Footer';
import { useThemePreference , toggleChat ,toggleDarkMode } from './utils/getThemePreference';

const App = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [activePage, setActivePage] = useState('home');
  useThemePreference(setDarkMode);

  return (
    <div className={`min-h-screen flex flex-col ${darkMode ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white flex-grow">
        <Navbar
          darkMode={darkMode}
          toggleDarkMode={toggleDarkMode(darkMode, setDarkMode)}
          toggleChat={toggleChat(chatOpen, setChatOpen)}
          setActivePage={setActivePage}
        />
        <main className="p-4 flex-grow">
          {activePage === 'home' ? <Chat /> : <Docs />}
        </main>
      </div>
      <ChatOffCanvas isOpen={chatOpen} onClose={toggleChat(chatOpen, setChatOpen)} />
      <Footer />
    </div>
  );
};

export default App;