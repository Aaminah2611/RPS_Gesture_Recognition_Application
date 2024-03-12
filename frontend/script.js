// script.js
fetch('/matchmaking', {
    method: 'POST',
    // Additional options like headers and body can be added here
}).then(response => {
    // Handle response from server
}).catch(error => {
    console.error('Error:', error);
});
