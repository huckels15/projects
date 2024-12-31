export const uploadData = async (file) => {
    try {
      // Fetch the external IP of the target VM from the backend
      const ipResponse = await fetch(`${window.location.protocol}//${window.location.hostname}/port3001/api/vm-external-ip?zone=us-east1-c&instanceName=ansible-data`);
      if (!ipResponse.ok) throw new Error("Failed to fetch VM external IP");
  
      const { ip: externalIP } = await ipResponse.json();
      const url = `http://${externalIP}:8000/predict/`;
  
      // Prepare and send the file upload request
      const formData = new FormData();
      formData.append("file", file);
  
      const response = await fetch(url, {
        method: "POST",
        body: formData, // Do not set Content-Type manually
      });
  
      if (!response.ok) {
        const errorText = await response.text(); // Capture error details from the server
        throw new Error(`Failed to upload dataset. Status: ${response.status} - ${errorText}`);
      }
  
      const jsonResponse = await response.json();
      return { success: true, json: jsonResponse };
    } catch (error) {
      console.error("Error uploading dataset:", error);
      return { success: false, error: error.message };
    }
  };
  