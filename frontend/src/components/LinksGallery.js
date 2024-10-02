function LinksGallery () {
    console.log('hey');
    return(

       <section id="siteReference" className="mt-4 text-center">

        <h4> YOU MAY ALSO NEED</h4>

        <div className=" mt-4 flex flex-row space-x-3 justify-center">
          <div className="p-4 bg-gray-200 rounded dark:bg-gray-700 cursor-pointer hover:bg-gray-400 hover:text-white">Langchain</div>
          <div className="p-4 bg-gray-200 rounded dark:bg-gray-700 cursor-pointer hover:bg-gray-400 hover:text-white">VertexAi</div>
          <div className="p-4 bg-gray-200 rounded dark:bg-gray-700 cursor-pointer hover:bg-gray-400 hover:text-white">Alpenite</div>
       </div>
       
       </section>
    );
}

export default LinksGallery;