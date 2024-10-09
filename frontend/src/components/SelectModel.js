import { useState, useEffect } from 'react';

function SelectModel({ model, setModel}){
  
  const [showOverlay, setShowOverlay] = useState(false);  

  useEffect(() => {
    if (showOverlay) {
      const timer = setTimeout(() => {
        setShowOverlay(false);
      }, 500); 
      return () => clearTimeout(timer);
    }
  }, [showOverlay]);
  
  const handleModelChange = (e) => {
    setModel(e.target.value);
    setShowOverlay(true);  // Show overlay when model changes
  };
  
  return(
   <>
     {showOverlay && (
       <div id="overlay" className={!showOverlay ? "hidden" : ""}>
          <div id="overlay-text">
            Switching to {model === 'chatgpt' ? 'ChatGPT' : 'Gemini'}...
          </div>
        </div>
      )}

      <div className="mb-4">
        <label htmlFor="modelSelect" className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
         Choose AI model:
        </label>
        <select
          id="modelSelect"
          value={model}
          onChange={handleModelChange}
          className="p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white"
         >
          <option value="chatgpt">ChatGPT</option>
          <option value="gemini">Gemini</option>
        </select>
      </div>
   </>
  );
};

export default SelectModel;