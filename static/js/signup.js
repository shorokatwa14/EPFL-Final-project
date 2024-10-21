document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signup-form');
    const submitButton = document.querySelector('input[type="submit"]');

    const fullname = document.getElementById('fullname');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const address = document.getElementById('address');
    const phone = document.getElementById('phone');
    const security_question = document.getElementById('security_question');

    const fullnameError = document.getElementById('fullname-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const addressError = document.getElementById('address-error');
    const phoneError = document.getElementById('phone-error');
    const securityQuestionError = document.getElementById('security_question-error');

    submitButton.disabled = true;

    function checkEmailValidity() {
        const emailPattern = /^[a-zA-Z][^@]+@[^@]+\.[a-zA-Z]{2,}$/;
        const emailValid = emailPattern.test(email.value);

        if (!email.value) {
            emailError.style.display = 'none'; 
            return true; 
        }

        if (!emailValid) {
            email.classList.add('error');
            emailError.textContent = 'Please enter a valid email address.';
            emailError.style.display = 'block';
            return false;
        } else {
            email.classList.remove('error');
            emailError.style.display = 'none';
            return true; 
        }
    }

    function checkFormValidity() {
        const isValidFullname = fullname.value.trim().length >= 3;
        const isValidPassword = password.value.length >= 6;
        const isValidAddress = address.value.trim() !== '';
        const isValidPhone = /^[0-9]{10,15}$/.test(phone.value);
        const isValidSecurityQuestion = security_question.value.trim() !== '';

        fullnameError.style.display = fullname.value ? (isValidFullname ? 'none' : 'block') : 'none';
        passwordError.style.display = password.value ? (isValidPassword ? 'none' : 'block') : 'none';
        addressError.style.display = address.value ? (isValidAddress ? 'none' : 'block') : 'none';
        phoneError.style.display = phone.value ? (isValidPhone ? 'none' : 'block') : 'none';
        securityQuestionError.style.display = security_question.value ? (isValidSecurityQuestion ? 'none' : 'block') : 'none';

        const isEmailValid = checkEmailValidity();
        
        submitButton.disabled = !(isValidFullname && isEmailValid && isValidPassword && isValidAddress && isValidPhone && isValidSecurityQuestion);
    }

    fullname.addEventListener('input', checkFormValidity);
    email.addEventListener('input', checkFormValidity);
    password.addEventListener('input', checkFormValidity);
    address.addEventListener('input', checkFormValidity);
    phone.addEventListener('input', checkFormValidity);
    security_question.addEventListener('input', checkFormValidity);

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!submitButton.disabled) {
            const formData = new URLSearchParams({
                fullname: fullname.value,
                email: email.value,
                password: password.value,
                address: address.value,
                phone: phone.value,
                security_question: security_question.value
            });

            fetch('/signup', {
                method: 'POST',
                body: formData,
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
                    if (data.error) {
                        if (data.error.includes('Email already exists')) {
                            email.classList.add('error');
                            emailError.textContent = data.error;
                            emailError.style.display = 'block';
                        }
                        submitButton.disabled = true;  
                    }
                }
            })
            .catch(err => {
                alert("There was an error processing your request. Please try again later.");
            });       
         }
    });

    email.addEventListener('input', function () {
        if (email.classList.contains('error')) {
            checkFormValidity();
        }
    });
});
