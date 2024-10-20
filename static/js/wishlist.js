document.addEventListener('DOMContentLoaded', () => {
    function fetchWishlistProducts() {
        fetch('/get_wishlist')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const wishlist = data.wishlist;
                    fetch('/get_wishlist_products', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ wishlist: wishlist })
                    })
                        .then(response => response.json())
                        .then(products => {
                            renderWishlist(products);
                        })
                        .catch(error => console.error('Error fetching wishlist products:', error));
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error fetching wishlist:', error));
    }

    function renderWishlist(products) {
        const productList = document.getElementById('products');
        productList.innerHTML = ''; // Clear the list before rendering

        products.forEach(product => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <span class="wishlist-heart active" data-id="${product.id}">
                    &#10084;
                </span>
                <img src="${product.thumbnail}" alt="${product.name}" width="50">
                <div class="product-details ${product.inStock ? '' : 'out-of-stock'}">
                    <strong>${product.name}</strong>
                    <p>${product.description}</p>
                    <p class="type">${product.type}</p>
                    <span class="price">$${product.price} </span>
                </div>
                <div class="product-actions">
                <div class="quantity-control">
                    <button class="decrease">-</button>
                    <input type="number" min="1" value="1" class="quantity">
                    <button class="increase">+</button>
                </div>
                <button class="add-to-cart-btn ${product.inStock ? '' : 'out-of-stock'}" data-id="${product.id}">
                    Add to Cart
                </button>
                </div>
            `;
            productList.appendChild(listItem);

            const heartIcon = listItem.querySelector('.wishlist-heart');
            heartIcon.addEventListener('click', () => {
                heartIcon.classList.toggle('active');
                removeFromWishlist(product.id);
            });

            const addToCartBtn = listItem.querySelector('.add-to-cart-btn');
            const quantityInput = listItem.querySelector('.quantity');
            const decreaseBtn = listItem.querySelector('.decrease');
            const increaseBtn = listItem.querySelector('.increase');

            decreaseBtn.addEventListener('click', () => {
                quantityInput.value = Math.max(1, parseInt(quantityInput.value) - 1);
            });

            increaseBtn.addEventListener('click', () => {
                quantityInput.value = parseInt(quantityInput.value) + 1;
            });

            addToCartBtn.addEventListener('click', () => {
                if (product.inStock) {
                    const quantity = parseInt(quantityInput.value);
                    addToCart(product, quantity);
                }
            });
        });
    }

    function removeFromWishlist(productId) {
        fetch('/remove_from_wishlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchWishlistProducts(); // Refresh the wishlist
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => console.error('Error removing from wishlist:', error));
    }

    function addToCart(product, quantity) {
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: product.id, quantity: quantity })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Added ${quantity} ${product.name}(s) to cart!`);
                } else {
                    alert(`Error adding to cart: ${data.error}`);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    fetchWishlistProducts();
});