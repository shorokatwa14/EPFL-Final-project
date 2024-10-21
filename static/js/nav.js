document.addEventListener('DOMContentLoaded', function() {
    const navUserDropdown = document.querySelector('.nav-user-dropdown');
    const dropdownContent = navUserDropdown.querySelector('.dropdown-content');

    navUserDropdown.querySelector('.nav-user').addEventListener('click', function(e) {
      e.preventDefault();
      dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function(e) {
      if (!navUserDropdown.contains(e.target)) {
        dropdownContent.style.display = 'none';
      }
    });
  });