import NavItem from "./NavItem";
import React from "react";
import { Moon, Sun, MessageSquare, FileText, Home } from 'lucide-react';

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
export default Navbar;