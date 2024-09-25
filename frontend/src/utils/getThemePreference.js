import { useEffect } from 'react';
import { saveThemePreference } from './saveThemePreference';

export function useThemePreference(setDarkMode){
    useEffect(() => {
      const savedDarkMode = localStorage.getItem('darkMode');
      if (savedDarkMode) {
        setDarkMode(savedDarkMode === 'true');
      }
    }, [setDarkMode]);
};

export const toggleChat = (chatOpen, setChatOpen) => () => setChatOpen(!chatOpen);
  

export const toggleDarkMode = (darkMode, setDarkMode) => () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    saveThemePreference(newDarkMode);
};