document.addEventListener('DOMContentLoaded', function() {
      const uploadButton = document.getElementById('uploadButton');
      const uploadModal = document.getElementById('uploadModal');
      const modalContent = document.getElementById('modalContent');

      // Open modal and fetch content
      uploadButton.addEventListener('click', function() {
        fetch('/upload_resume')
          .then(response => response.text())
          .then(data => {
            modalContent.innerHTML = data;
            uploadModal.classList.add('flex');
            uploadModal.classList.remove('hidden');

            // Attach event listeners for the modal content after it's loaded
            const fileInput = modalContent.querySelector('#fileInput');
            const fileName = modalContent.querySelector('#fileName');
            const dragDropText = modalContent.querySelector('#dragDropText');
            const uploadIcon = modalContent.querySelector('#uploadIcon');
            const form = modalContent.querySelector('#uploadForm');
            
            
            if (fileInput && fileName && dragDropText && uploadIcon) {
                fileInput.addEventListener('change', function() {
                    if (fileInput.files.length > 0) {
                        const file = fileInput.files[0];
                        fileName.textContent = `Selected file: ${file.name}`;
                        fileName.classList.remove('hidden');
                        dragDropText.classList.add('hidden');
                        uploadIcon.classList.add('hidden');
                    }
                });
            }

            form.addEventListener('submit',function(event){
                event.preventDefault();
                if (fileInput.files.length > 0) {
                    const file = fileInput.files[0];
                    const formData = new FormData();
                    formData.append('file', file);
                    fetch('/upload_resume/', { // Use the correct endpoint
                          method: 'POST',
                          body: formData,
                        })
                        .then(response => {
                          if (!response.ok) {
                            return response.json().then(err => { throw new Error(err.detail || 'File upload failed'); });
                          }
                          return response.json();
                        })
                        .then(data => {
                          console.log('Upload successful:', data);
                          // Handle the successful upload (e.g., show a success message)
                          alert('File uploaded successfully!');
                          uploadModal.classList.add('hidden');
                          feedback(data.filename)
                          
                        
                        })
                        .catch(error => {
                          console.error('Error uploading file:', error);
                          // Handle the error (e.g., show an error message to the user)
                          alert('Error uploading file: ' + error.message);
                          uploadButton.textContent = 'Upload'; // Restore button text
                          uploadButton.disabled = false; // Re-enable the button
                        });
                }
            })
            // Close modal when clicking outside
            uploadModal.addEventListener('click', function(event) {
              if (event.target === uploadModal) {
                uploadModal.classList.add('hidden');
              }
            });

            // Close modal with a button (if added)
            const closeButton = modalContent.querySelector('#closeModalButton');
            if (closeButton) {
              closeButton.addEventListener('click', function() {
                uploadModal.classList.add('hidden');
              });
            }
          })
          .catch(error => {
            console.error('Error fetching upload form:', error);
            modalContent.innerHTML = '<p>Error loading upload form.</p>';
            uploadModal.classList.remove('hidden');
          });
      });
    });


    function feedback(id) {
      const uploadModal = document.getElementById('uploadModal');
      const modalContent = document.getElementById('modalContent');
      fetch(`/feedback?path=${id}`)
          .then(response => response.text())
          .then(data => {
            modalContent.innerHTML = data;
            uploadModal.classList.add('flex');
            uploadModal.classList.remove('hidden');
            // document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('preferencesForm');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const selectedPreferences = [];
    const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');

    checkboxes.forEach(function(checkbox) {
      selectedPreferences.push(checkbox.name); // Assuming the 'name' attribute holds the preference value
    });

    // Now you have an array 'selectedPreferences' containing the names
    // of all the checked checkboxes.

    // You can now send this array to your API using a fetch request or
    // any other method you prefer.

    console.log("Selected Preferences:", selectedPreferences);
    console.log(JSON.stringify({path:id, preferences: selectedPreferences }));
    

    // Example of how you might send this to an API using fetch:
    fetch('/apply_feedback', {
      method: 'POST',
       headers: {
    'Content-Type': 'application/json'
  },
      body: JSON.stringify({path:id, preferences: selectedPreferences }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      // Handle the API response here (e.g., show a success message)
    })
    .catch((error) => {
      console.error('Error:', error);
      // Handle any errors that occurred during the API call
    });
  });
});
          }