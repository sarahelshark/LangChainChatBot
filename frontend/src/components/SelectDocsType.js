function SelectDocsType(){
    return(
        <>
        <div className="mb-4">
         <label htmlFor="modelSelect" className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
           Choose Docs type:
         </label>
         <select
           id="modelSelect"
           value=""
           onChange=""
           className="p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white"
         >
           <option value="">Dev</option>
           <option value="">User</option>
         </select>
       </div>
        </>
    );
};
export default SelectDocsType;