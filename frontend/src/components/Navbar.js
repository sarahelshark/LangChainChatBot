import React from "react";
import NavItem from "./NavItem";
import ToggleModeButton from "./ToggleModeButton";

import { MessageSquare, FileText, Home } from 'lucide-react';

const Navbar = ({ darkMode, toggleDarkMode, toggleChat, setActivePage }) => (
    <nav className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
      <div className="flex space-x-4">
       <NavItem icon={Home} label="Home" onClick={() => setActivePage('home')} />
       <NavItem icon={MessageSquare} label="Chat" onClick={toggleChat} />
       <NavItem icon={FileText} label="Docs" onClick={() => setActivePage('docs')} />
      </div>
      <ToggleModeButton darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
    </nav>
  );
export default Navbar;