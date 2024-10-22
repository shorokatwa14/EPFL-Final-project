let total = 0;
const checkoutForm = document.getElementById('checkout-form');
const placeOrderBtn = document.querySelector('.place-order');
const requiredInputs = checkoutForm.querySelectorAll('input[required]');

placeOrderBtn.disabled = true;
placeOrderBtn.style.opacity = '0.5';
placeOrderBtn.style.cursor = 'not-allowed';

function validateForm() {
    let isValid = true;
    let emptyFields = [];
    
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            emptyFields.push(input.getAttribute('placeholder'));
        }
    });
    
    if (isValid) {
        placeOrderBtn.disabled = false;
        placeOrderBtn.style.opacity = '1';
        placeOrderBtn.style.cursor = 'pointer';
    } else {
        placeOrderBtn.disabled = true;
        placeOrderBtn.style.opacity = '0.5';
        placeOrderBtn.style.cursor = 'not-allowed';
    }

    return { isValid, emptyFields };
}

requiredInputs.forEach(input => {
    input.addEventListener('input', validateForm);
    input.addEventListener('focus', () => {
        input.style.borderColor = '';
    });
});

async function displayCart() {
    const cartItemsElement = document.getElementById('cart-items');
    cartItemsElement.innerHTML = '';
    total = 0;

    try {
        const response = await fetch('/get_cart_items', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        const products = await response.json();

        products.forEach(product => {
            const quantity = product.quantity;
            const itemTotal = product.price * quantity;
            total += itemTotal;

            const productDiv = document.createElement('div');
            productDiv.className = 'product-item';
            productDiv.innerHTML = `
                <img src="${product.thumbnail}" alt="${product.name}" class="product-image">
                <div class="product-details">
                    <div>${product.name}</div>
                    <div>x ${quantity}</div>
                </div>
                <div class="product-price">$${itemTotal.toFixed(2)}</div>
            `;
            cartItemsElement.appendChild(productDiv);
        });

        document.getElementById('subtotal').textContent = `$${total.toFixed(2)}`;
        document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    } catch (error) {
        document.getElementById('cart-items').innerHTML = '<div>Error fetching cart items.</div>';
    }
}

async function fetchCartFromBackend() {
    try {
        const response = await fetch('/get_cart_items', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        return await response.json();
    } catch (error) {
        document.getElementById('cart-items').innerHTML = '<div>Error fetching cart items.</div>';
        return {};
    }
}

async function placeOrder() {
    const validation = validateForm();
    
    if (!validation.isValid) {
        const emptyFieldsList = validation.emptyFields.join(', ');
        alert(`Please fill in all required fields to continue your order.\n\nMissing information for: ${emptyFieldsList}`);
        
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.style.borderColor = 'red';
                input.addEventListener('input', function removeHighlight() {
                    if (input.value.trim()) {
                        input.style.borderColor = '';
                        input.removeEventListener('input', removeHighlight);
                    }
                });
            }
        });
        return;
    }

    const formData = new FormData(document.getElementById('checkout-form'));
    const orderData = {
        customerInfo: Object.fromEntries(formData),
        cart: await fetchCartFromBackend(),
        total: total,
    };

    try {
        const response = await fetch('/save_order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });
        const data = await response.json();

        if (data.success) {
            showSuccessDialog();
        } else {
            alert('Error placing order: ' + data.message);
        }
    } catch (error) {
        alert('Error placing order.');
    }
}

function showSuccessDialog() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('successDialog').style.display = 'block';
}

function hideSuccessDialog() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('successDialog').style.display = 'none';
}

displayCart();