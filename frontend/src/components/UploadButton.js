import React from "react";

import { ArrowUp } from 'lucide-react';

const UploadButton = (e) => {
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        // Handle the file upload logic here
        console.log('File uploaded:', file);
      };
return (
    <div className="upload flex items-center mt-2">
    <label className="upload-area">
      <input
        type="file"
        className="hidden"
        id="fileUpload"
        onChange={handleFileUpload}
      />
      <span className="upload-button btn ">
        <ArrowUp className="text-xl" />
      </span>
    </label>
  </div>
  );
};



export default UploadButton;