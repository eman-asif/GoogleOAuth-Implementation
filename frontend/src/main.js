import './style.css';

// Load Google Identity Services SDK dynamically
(function() {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
})();

window.onload = () => {
    google.accounts.id.initialize({
        client_id: '346899942676-c2f4d6h8cjd7nnc36sauhm7peo2qt5dn.apps.googleusercontent.com', // <-- Replace with your Client ID
        callback: handleCredentialResponse,
    });

    google.accounts.id.renderButton(
        document.getElementById("google-signin-button"),
        { theme: "outline", size: "large" }
    );
};

function handleCredentialResponse(response) {
    const id_token = response.credential;
    console.log("ID Token:", id_token);

    // Send ID Token to Backend
    fetch('http://localhost:8000/api/google-login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: id_token })  // <<== Send as JSON body
    })
    .then(res => res.json())
    .then(data => {
        console.log("Backend Response:", data);
        alert(`Welcome ${data.user.name}`);
    })
    .catch(err => {
        console.error("Error sending token to backend:", err);
    });
}
