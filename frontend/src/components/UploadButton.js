import React, { useState } from "react";
import { ArrowUp } from "lucide-react";
import { sendUpload } from "../utils/sendUpload"
import Modal from "./Modal";

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
    sendUpload(event)
    if (file) {

      setFileName(file.name);
      setModalVisible(true);

      setTimeout(() => {
        setModalVisible(false);
      }, 2000);
    } 

  };

  return (
    <>
      <Modal isModalVisible={isModalVisible} fileName={fileName} modalInfo={modalInfo} />
      <div className="upload flex items-center mt-2">
        <label className="upload-area">
          <input
            type="file"
            encType='multipart/form-data'
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
