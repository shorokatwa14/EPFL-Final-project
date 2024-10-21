document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;

    fetch('/login', {
      method: 'POST',
      body: new URLSearchParams({ email, password }),
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