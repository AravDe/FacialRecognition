document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const videoElement = document.getElementById('webcam');

    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            alert('Login form submitted!');
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', (event) => {
            event.preventDefault();
            alert('Signup form submitted!');
        });
    }

    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
        navigator.mediaDevices.getUserMedia({video : true})
        .then(function(stream){
            videoElement.srcObject = stream;
        })
        .catch(function(error){
            console.log("Error accessing webcam: ", error); 
        });
    }
    else
    {
        alert("Your browser doesn't support webcam access")
    }
});