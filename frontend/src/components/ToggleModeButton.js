import React from "react";
import { Moon, Sun} from 'lucide-react';

const ToggleModeButton = ({darkMode, toggleDarkMode,}) => {
    return (
      <button
        onClick={toggleDarkMode}
        className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
        value={darkMode}
      >
        {darkMode ? <Sun size={24} /> : <Moon size={24} />}
      </button>

    );
};

export default ToggleModeButton;