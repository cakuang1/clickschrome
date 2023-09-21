console.log('content script')

document.addEventListener('click', function(event) {
    const x = event.clientX;
    const y = event.clientY;
    const targetElement = event.target.tagName;
    
    const clickEventData = {
        x: x,
        y: y,
        targetElement: targetElement,
        timestamp: new Date().toLocaleString() // Add the current date and time
    };


    chrome.runtime.sendMessage({
        type: 'mouseClick',
        data: clickEventData
    });
});
