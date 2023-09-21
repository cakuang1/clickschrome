// background.js

console.log("Background is running")

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === 'mouseClick') {
    const clickEventData = request.data;
    const producerEndpoint = 'http://127.0.0.1:8000/send_click'; 
    const postData = {
      clickData: clickEventData,
    };

    // Send a POST request
    fetch(producerEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Handle the response from the producer if needed
      console.log('Response from producer:', data);
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error sending POST request:', error);
    });
  }
});
