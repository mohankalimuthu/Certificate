const API_URL = "http://127.0.0.1:5000";

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const admin_id = document.getElementById('admin_id').value;
    const password = document.getElementById('password').value;

    const message = document.getElementById('message');

    try {

        const response = await fetch(`${API_URL}/admin-login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                admin_id,
                password
            })
        });

        const data = await response.json();

        if (data.success) {

            message.style.color = 'green';
            message.innerHTML = data.message;

            localStorage.setItem('adminLoggedIn', true);

            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);

        } else {

            message.style.color = 'red';
            message.innerHTML = data.message;
        }

    } catch (error) {

        message.style.color = 'red';
        message.innerHTML = 'Server Error';
    }
});