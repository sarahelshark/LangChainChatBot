import React, { useEffect, useState } from 'react';
import { marked } from 'marked';

function Docs() {
    const [content, setContent] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/README.md')  // Updated path to fetch README.md from the root of the project
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
                console.error('Error fetching and rendering README.md:', error);
                setError('Error loading README.md content.');
            });
    }, []);

    return (

        <div className="mt-8">
        <h1 className="text-2xl font-bold mb-4">Chatbot Docs</h1>
        <div className="h-64 p-4 bg-gray-100 dark:bg-gray-700 overflow-y-auto rounded">
        <div id="readme-content">
            {error ? <p className="text-danger">{error}</p> : <div dangerouslySetInnerHTML={{ __html: content }} />}
        </div>
        </div>
        
      </div>
    );
}

export default Docs;