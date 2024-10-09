function SelectDocsType({docsType , setDocsType}){
   
  const handleDocsChange = (e) =>{
    setDocsType(e.target.value);
  }; 
   
  return(
    <>
      <div className="mb-4">
        <label htmlFor="modelSelect" className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          Choose Docs type:
        </label>
        <select
          id="modelSelect"
          value={docsType}
          onChange={handleDocsChange}
          className="p-2 border border-gray-300 rounded dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white"
        >
          <option value="dev">Dev</option>
          <option value="user">User</option>
        </select>
      </div>
    </>
  );
};
export default SelectDocsType;