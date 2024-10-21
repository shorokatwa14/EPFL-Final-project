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

    // Disable submit button initially
    submitButton.disabled = true;

    function checkEmailValidity() {
        const emailPattern = /^[a-zA-Z][^@]+@[^@]+\.[a-zA-Z]{2,}$/;
        const emailValid = emailPattern.test(email.value);

        if (!email.value) {
            emailError.style.display = 'none'; // إخفاء الرسالة إذا كان الحقل فارغ
            return true; // اعتبر البريد صالح، سيظهر الخطأ بعد
        }

        if (!emailValid) {
            email.classList.add('error');
            emailError.textContent = 'Please enter a valid email address.';
            emailError.style.display = 'block';
            return false;
        } else {
            email.classList.remove('error');
            emailError.style.display = 'none';
            return true; // بريد صالح
        }
    }

    function checkFormValidity() {
        const isValidFullname = fullname.value.trim().length >= 3;
        const isValidPassword = password.value.length >= 6;
        const isValidAddress = address.value.trim() !== '';
        const isValidPhone = /^[0-9]{10,15}$/.test(phone.value);
        const isValidSecurityQuestion = security_question.value.trim() !== '';

        // Show/hide errors
        fullnameError.style.display = fullname.value ? (isValidFullname ? 'none' : 'block') : 'none';
        passwordError.style.display = password.value ? (isValidPassword ? 'none' : 'block') : 'none';
        addressError.style.display = address.value ? (isValidAddress ? 'none' : 'block') : 'none';
        phoneError.style.display = phone.value ? (isValidPhone ? 'none' : 'block') : 'none';
        securityQuestionError.style.display = security_question.value ? (isValidSecurityQuestion ? 'none' : 'block') : 'none';

        // Validate email separately
        const isEmailValid = checkEmailValidity();
        
        // Enable or disable submit button based on form validity
        submitButton.disabled = !(isValidFullname && isEmailValid && isValidPassword && isValidAddress && isValidPhone && isValidSecurityQuestion);
    }

    // Attach input event listeners to check for validity on each change
    fullname.addEventListener('input', checkFormValidity);
    email.addEventListener('input', checkFormValidity);
    password.addEventListener('input', checkFormValidity);
    address.addEventListener('input', checkFormValidity);
    phone.addEventListener('input', checkFormValidity);
    security_question.addEventListener('input', checkFormValidity);

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Check if the submit button is enabled
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
            .catch(err => console.error(err));
        }
    });

    email.addEventListener('input', function () {
        if (email.classList.contains('error')) {
            checkFormValidity();
        }
    });
});
