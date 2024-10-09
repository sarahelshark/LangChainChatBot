import React, { useState } from 'react';
import MarkdownContent from './MarkdownContent';
import LinksGallery from './LinksGallery';
import SelectDocsType from './SelectDocsType';

const DocsContainer = () => {
  const [docsType, setDocsType] = useState('dev'); // default docs type

  return (
    <div className="mt-8 mx-5 md:mx-11">
      <h1 className="text-2xl font-bold mb-4 text-center">Chatbot Docs</h1>
      <SelectDocsType docsType={docsType} setDocsType={setDocsType} />
      <div className="h-64 p-4 bg-gray-200 dark:bg-gray-700 overflow-y-auto rounded">
        <MarkdownContent docsType={docsType} />
      </div>
      <LinksGallery />
    </div>
  );
};

export default DocsContainer;
