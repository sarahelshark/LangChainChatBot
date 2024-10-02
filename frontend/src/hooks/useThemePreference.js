import { useEffect } from 'react';

export function useThemePreference(setDarkMode){
    useEffect(() => {
      const savedDarkMode = localStorage.getItem('darkMode');
      if (savedDarkMode) {
        setDarkMode(savedDarkMode === 'true');
      }
    }, [setDarkMode]);
};
