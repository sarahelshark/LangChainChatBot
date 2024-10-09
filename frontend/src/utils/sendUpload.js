export async function sendUpload(event) {
    const file = event.target.files[0];
    console.log(file);
    //if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    if (file) {
    fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData,
        
      })
      .then(response => response.json())
      .catch(error => {
        console.error('Error:', error);
    });
    }
  }
  
