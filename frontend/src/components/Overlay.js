import React from 'react';

const Overlay = ({ showOverlay, model }) => {
  return (
    showOverlay && (
      <div id="overlay" className={!showOverlay ? "hidden" : ""}>
        <div id="overlay-text">
          Switching to {model === 'chatgpt' ? 'ChatGPT' : 'Gemini'}...
        </div>
      </div>
    )
  );
};

export default Overlay;
