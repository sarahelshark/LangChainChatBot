import { saveThemePreference } from './saveThemePreference';

export const toggleChat = (chatOpen, setChatOpen) => () => setChatOpen(!chatOpen);

export const toggleDarkMode = (darkMode, setDarkMode) => () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    saveThemePreference(newDarkMode);
};