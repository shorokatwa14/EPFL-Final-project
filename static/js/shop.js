document.addEventListener('DOMContentLoaded', () => {
    let wishlist = [];

    function fetchWishlist() {
        return fetch('/get_wishlist')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    wishlist = data.wishlist;
                } else {
                    alert(`Error fetching wishlist: ${data.error}`);
                }
            })
            .catch(() => {
                alert('Error fetching wishlist. Please try again later.');
            });
    }

    function toggleWishlist(productId, heartIcon) {
        fetch('/add_to_wishlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    heartIcon.classList.toggle('active');
                } else {
                    alert(`Error adding to wishlist: ${data.error}`);

                }
            })
            .catch(() => {
                alert('Error adding to wishlist. Please try again later.');
            });
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
            .catch(() => {
                alert('Error adding to cart. Please try again later.');
            });    }

    function fetchProducts(category = null) {
        let url = "/get_products";
        if (category) {
            url += `?category=${category}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const productList = document.getElementById('products');
                productList.innerHTML = ''; // Clear existing products
                data.forEach(product => {
                    const listItem = document.createElement('li');
                    const isWishlisted = wishlist.includes(product.id);
                    listItem.innerHTML = `
                        <span class="wishlist-heart ${isWishlisted ? 'active' : ''}" data-id="${product.id}">
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
                        toggleWishlist(product.id, heartIcon);
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
            })
            .catch(() => {
                alert('Error fetching the products. Please try again later.');
            });
            }

    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');

    fetchWishlist().then(() => fetchProducts(category));
});