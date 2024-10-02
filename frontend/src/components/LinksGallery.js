const linksData = [
   { name: 'Langchain', url: 'https://docs.langchain.com/' },
   { name: 'VertexAi', url: 'https://cloud.google.com/vertex-ai/docs' },
   { name: 'Alpenite', url: 'https://www.alpenite.com/' }
 ];
 
 function LinksGallery() {
   return (
     <section id="siteReference" className="mt-4 text-center">
       <h4>YOU MAY ALSO NEED</h4>
 
       <div className="mt-4 flex flex-row space-x-3 justify-center">
         {linksData.map((link, index) => (
           <a
             key={index}
             href={link.url}
             target="_blank"
             rel="noopener noreferrer"
             className="p-4 bg-gray-200 rounded dark:bg-gray-700 cursor-pointer hover:bg-gray-400 hover:text-white dark:hover:bg-gray-900"
           >
             {link.name}
           </a>
         ))}
       </div>
     </section>
   );
 }
 
 export default LinksGallery;
 