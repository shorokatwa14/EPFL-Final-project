
async function fetchCartItems() {
    try {
        const response = await fetch('/get_cart_items', {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error fetching cart items:', errorData.error);
            document.getElementById('cart-items').innerHTML = '<tr><td colspan="6">No items in the cart .</td></tr>';
            disableCheckoutButton();
            return;
        }

        const cartItems = await response.json();
        displayCartItems(cartItems);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('cart-items').innerHTML = '<tr><td colspan="6"> Error fetching data.</td></tr>';
        disableCheckoutButton();

    }
}

async function removeItem(itemId) {
    try {
        const response = await fetch('/remove_from_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ product_id: itemId })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error removing item:', errorData.error);
            disableCheckoutButton();
            return;
        }


        fetchCartItems();
    } catch (error) {
        console.error('Error:', error);
        disableCheckoutButton();

    }
}

async function addQuantity(itemId) {
    try {
        const response = await fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ product_id: itemId, quantity: 1 })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error adding quantity:', errorData.error);
            return;
        }

        fetchCartItems();
    } catch (error) {
        console.error('Error:', error);
    }
}

async function removeQuantity(itemId) {
    try {
        const response = await fetch('/remove_quantity_from_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ product_id: itemId, quantity: 1 })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error removing quantity:', errorData.error);
            return;
        }

        fetchCartItems();
    } catch (error) {
        console.error('Error:', error);
    }
}


function displayCartItems(cartItems) {  
    const cartItemsContainer = document.getElementById('cart-items');
    
    cartItemsContainer.innerHTML = ''; 
    if (!cartItems.length) {
        cartItemsContainer.innerHTML = '<tr><td colspan="6">Cart is empty.</td></tr>';
        disableCheckoutButton();
        return;   
    }
    enableCheckoutButton();

    let subtotal = 0;

    // Iterate through each item and create table rows
    cartItems?.forEach(item => {        
        const quantity = item.quantity || 1; // Assuming quantity is part of the product data
        const itemSubtotal = item.price * quantity;

        // Create a new table row
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><img src="${item.thumbnail}" alt="${item.name}" width="50"></td>
            <td>${item.name}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>
                <button onclick="removeQuantity('${item.id}')">-</button>
                ${quantity}
                <button onclick="addQuantity('${item.id}')">+</button>
            </td>
            <td>$${itemSubtotal.toFixed(2)}</td>
            <td><button onclick="removeItem('${item.id}')">Remove</button></td>
        `;
        cartItemsContainer.appendChild(row);

        subtotal += itemSubtotal; // Add to subtotal
    });

    // Update totals
    updateCartTotals(subtotal);
}

// Function to update cart totals
function updateCartTotals(subtotal) {
    const shipping = 0; // Assuming free shipping
    const total = subtotal + shipping;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}
function disableCheckoutButton() {
    const checkoutButton = document.getElementById('checkout-button');
    checkoutButton.classList.add('disabled');
    checkoutButton.addEventListener('click', preventCheckout);
}

function enableCheckoutButton() {
    const checkoutButton = document.getElementById('checkout-button');
    checkoutButton.classList.remove('disabled');
    checkoutButton.removeEventListener('click', preventCheckout);
}

function preventCheckout(event) {
    event.preventDefault();
    alert('You must add items to your cart before proceeding to checkout.');
}

window.onload = fetchCartItems;
