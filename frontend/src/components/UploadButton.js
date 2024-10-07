import React, { useState } from "react";
import { ArrowUp } from "lucide-react";

const modalInfo = {
  success: "Success!",
  details: " è stato caricato correttamente.",
  instructions: "Puoi continuare a usare il chatbot appena la finestra di dialogo si chiude.",
};

const UploadButton = () => {

  const [fileName, setFileName] = useState(null);
  const [isModalVisible, setModalVisible] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    if (file) {
      // Imposta il nome del file e mostra la modale
      setFileName(file.name);
      setModalVisible(true);

      setTimeout(() => {
        setModalVisible(false);
      }, 2000);
    }
  };

  return (
    <>
      {isModalVisible && (
        <div
          id="confirm-upload"
          className="relative z-10"
          aria-labelledby="modal-title"
          role="dialog"
          aria-modal="true"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
          <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
              <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <h3 className="text-base font-semibold leading-6 text-gray-900" id="modal-title">
                        {modalInfo.success}
                      </h3>
                      <div className="mt-2">
                        <p className="text-sm text-gray-500">
                          <strong>{fileName}</strong>
                          {modalInfo.details}
                        </p>
                        <p>{modalInfo.instructions}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      
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
    </>
  );
};

export default UploadButton;
