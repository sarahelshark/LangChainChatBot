import { useState } from 'react';
import { useThemePreference } from '../hooks/useThemePreference';

const useAppState = () => {
    const [darkMode, setDarkMode] = useState(false);
    const [chatOpen, setChatOpen] = useState(false);
    const [activePage, setActivePage] = useState('home');
    useThemePreference(setDarkMode);
  
    return {
      darkMode,
      setDarkMode,
      chatOpen,
      setChatOpen,
      activePage,
      setActivePage,
    };
  };
export default useAppState;