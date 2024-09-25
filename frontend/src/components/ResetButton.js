import React from "react";

const resetButton = ({ resetConversation }) => {
  
  return (
    <button
      onClick={resetConversation}
      className="ml-2 p-2 border border-red-500 text-red-500 hover:bg-red-200 rounded "
    >
      Reset
    </button>
  );
};
export default resetButton;