import React from "react";

const NavItem = ({ icon: Icon, label, onClick }) => (
  <button
    className="flex items-center space-x-2 px-4 py-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
    onClick={onClick}
  >
    <Icon size={20} />
    <span>{label}</span>
  </button>
);
export default NavItem;