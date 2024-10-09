import React from 'react';
const footerInfo = {
  copyright: "2024 Alpenite test. All rights reserved.",
};

const Footer = () => (
  <footer className="bg-gray-200 dark:bg-gray-800 text-center p-1 mt-auto">
    <p className="text-gray-600 dark:text-gray-400">&copy;{footerInfo.copyright}</p>
  </footer>
);

export default Footer;