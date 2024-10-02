import { sendEnter } from '../utils/sendInputs';
import SendButton from './SendButton';
import ResetButton from './ResetButton';
import UploadButton from './UploadButton';

const FormInput = ({ input, setInput, messages, setMessages, setLoading, model, resetConversation }) => {
  return (
    <div className="mt-4 flex">
      <label htmlFor="formInput" className="sr-only">
        User input
      </label>
      <input
        name="formInput"
        id="formInput"
        type="text"
        className="flex-grow p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
        value={input}
        onKeyDown={(e) => sendEnter(e, input, messages, setMessages, setInput, setLoading, model)}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Write a message..."
      />
      <SendButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} setLoading={setLoading} model={model} />
      <ResetButton resetConversation={resetConversation} />
      <UploadButton input={input} messages={messages} setMessages={setMessages} setInput={setInput} />
    </div>
  );
};

export default FormInput;
