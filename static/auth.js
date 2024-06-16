document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const credentials = btoa(username + ':' + password);

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Authorization': 'Basic ' + credentials
        }
    });

    if (response.ok) {
        localStorage.setItem('username', username);
        localStorage.setItem('password', password);
        window.location.href = '/';
    }
});