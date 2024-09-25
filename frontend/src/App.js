import './index.css';
import Navbar from './components/Navbar';
import Chat from './components/Chat';
import ChatOffCanvas from './components/ChatOffCanvas';
import Docs from './components/Docs';
import Footer from './components/Footer';
import { toggleChat, toggleDarkMode } from './utils/toggleFunctions';
import useAppState from './hooks/useAppState';
const App = () => {
  const {
    darkMode,
    setDarkMode,
    chatOpen,
    setChatOpen,
    activePage,
    setActivePage,
  } = useAppState();

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