import React, { useEffect, useState } from 'react';
import { marked } from 'marked';

const MarkdownContent = ({ docsType }) => {
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    let url = docsType === 'dev' ? '/README.md' : '/READMEUSER.md';
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(markdown => {
        setContent(marked.parse(markdown));
      })
      .catch(error => {
        console.error(`Error fetching and rendering ${url}:`, error);
        setError(`Error loading ${url} content.`);
      });
  }, [docsType]);

  return error ? <p className="text-danger">{error}</p> : <div dangerouslySetInnerHTML={{ __html: content }} />;
};

export default MarkdownContent;
