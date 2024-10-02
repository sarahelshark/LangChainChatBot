export function saveThemePreference(isDarkMode) {
    return (
        localStorage.setItem('darkMode', isDarkMode ? 'true' : 'false')
    );
  }