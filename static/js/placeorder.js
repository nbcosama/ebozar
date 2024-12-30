// Function to increase quantity
function increaseQuantity(button) {
    const quantitySpan = button.parentElement.querySelector("#quantity");
    let currentQuantity = parseInt(quantitySpan.textContent);
    currentQuantity += 1;
    quantitySpan.textContent = currentQuantity;

    updateOrderSummary();
}

// Function to decrease quantity
function decreaseQuantity(button) {
    const quantitySpan = button.parentElement.querySelector("#quantity");
    let currentQuantity = parseInt(quantitySpan.textContent);
    if (currentQuantity > 1) {
        currentQuantity -= 1;
        quantitySpan.textContent = currentQuantity;

        updateOrderSummary();
    }
}

// Function to calculate and update the order summary
function updateOrderSummary() {
    const products = document.querySelectorAll(".product-card");
    let subtotal = 0;
    const shippingCost = 50; // Example fixed shipping cost
    const orderDetails = []; 
    
    products.forEach((product) => {
        // Scope the selectors to the current product card
        const productId = product.querySelector("input[name='product_id']").value;
        const price = parseFloat(product.querySelector(".product-info p:nth-child(2)").textContent.replace("Price:", ""));
        const quantity = parseInt(product.querySelector("#quantity").textContent);

        // Accumulate subtotal
        subtotal += price * quantity;

        // Add product details to the orderDetails array
        orderDetails.push({
            product_id: productId,
            quantity: quantity,
        });
    });

    const total = subtotal + shippingCost;

    // Update the order summary in the DOM
    document.querySelector("#subtotal").textContent = `Rs.${subtotal.toFixed(2)}`;
    document.querySelector("#shipping").textContent = `Rs.${shippingCost.toFixed(2)}`;
    document.querySelector("#total").textContent = `Rs.${total.toFixed(2)}`;

    // Return the order details for further use
    return orderDetails;
}

// Function to send order data to the server
function sendOrderData(orderDetails) {
    const data = {
        order_details: orderDetails,
    };

    fetch('/buyerOrder/?action=place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // Include CSRF token for Django
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        window.location.reload();
        return response.json();
    })
    
    .catch((error) => {
        console.error('Error sending order data:', error);
        alert('Failed to place order. Please try again.');
    });
}

// Function to get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Attach event listeners to buttons
window.onload = function () {
    const increaseButtons = document.querySelectorAll(".quantity-control button:nth-child(3)");
    const decreaseButtons = document.querySelectorAll(".quantity-control button:nth-child(1)");
    const placeOrderButton = document.querySelector("#placeOrderButton");

    increaseButtons.forEach((button) => {
        button.addEventListener("click", () => increaseQuantity(button));
    });

    decreaseButtons.forEach((button) => {
        button.addEventListener("click", () => decreaseQuantity(button));
    });

    placeOrderButton.addEventListener("click", () => {
        // Generate order details and send order data when the button is clicked
        const orderDetails = updateOrderSummary();
        sendOrderData(orderDetails);
    });

    // Initialize the order summary on page load
    updateOrderSummary();
};