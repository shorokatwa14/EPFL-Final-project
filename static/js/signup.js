document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const fullname = document.querySelector('input[name="fullname"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const address = document.querySelector('input[name="address"]').value;
    const phone = document.querySelector('input[name="phone"]').value;
    const security_question = document.querySelector('input[name="security_question"]').value;
    
    fetch('/signup', {
        method: 'POST',
        body: new URLSearchParams({ fullname, email, password, address, phone, security_question }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            localStorage.setItem('user', JSON.stringify(data));
            window.location.href = '/home';
        } else {
            alert(data.error);
        }
    })
    .catch(err => console.error(err));
});

function checkUserSession() {
    const user = localStorage.getItem('user');
    if (user) {
        const userData = JSON.parse(user);
        console.log("Logged in user:", userData);
    } else {
        console.log("No user logged in.");
    }
}

window.onload = checkUserSession;