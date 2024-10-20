document.addEventListener('DOMContentLoaded', () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        document.getElementById('profile-info').innerHTML = `
            <p><span class="label">Name:</span> ${user.name}</p>
            <p><span class="label">Email:</span> ${user.email}</p>
            <p><span class="label">Address:</span> ${user.address}</p>
            <p><span class="label">Phone:</span> ${user.phone}</p>
        `;
    } else {
        document.getElementById('profile-info').innerHTML = '<p class="error">User data not found.</p>';
    }
    
    fetch('/get_orders')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(data.orders);
                
                const ordersList = document.getElementById('orders-list');
                data.orders.forEach(order => {
                    const orderItem = document.createElement('div');
                    orderItem.className = 'order-item';
                    orderItem.innerHTML = `
                        <p><span class="label">Order ID:</span> ${order.order_id}</p>
                        <p><span class="label">Date:</span> ${order.order_date}</p>
                        <p><span class="label">Items:</span> ${order.cart.map(item => item.name).join(', ')}</p>
                        <p><span class="label">Total:</span> $${order.total}</p>
                    `;
                    ordersList.appendChild(orderItem);
                });
            } else {
                document.getElementById('orders-list').innerHTML = '<p class="error">Error fetching orders.</p>';
            }
        })
        .catch(error => {
            document.getElementById('orders-list').innerHTML = '<p class="error">Error fetching orders.</p>';
        });
});