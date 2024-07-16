export const getGeojsonData = async (formData) => {
    try {
      const response = await axios.post('http://localhost:8000/uploadfile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('File uploaded successfully:', response.data);
    } catch (error) {
      console.error('There was an error uploading the file!', error);
    }
  };