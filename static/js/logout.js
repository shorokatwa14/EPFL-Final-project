const logoutButton = document.querySelector('.logout-button');

logoutButton.addEventListener('click', () => {
    localStorage.removeItem('user');
})