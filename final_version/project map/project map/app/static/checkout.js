const form = document.getElementById('checkoutForm');
const delivery = document.getElementById('delivery');
const payment = document.getElementById('payment');
const addressSection = document.getElementById('addressSection');
const cardSection = document.getElementById('cardSection');
const bankSection = document.getElementById('bankSection');

delivery?.addEventListener('change', () => {
    if (addressSection) {
        addressSection.style.display = delivery.value === 'delivery to home' ? 'block' : 'none';
    }
});


payment?.addEventListener('change', () => {
    if (cardSection) cardSection.style.display = payment.value === 'card' ? 'block' : 'none';
    if (bankSection) bankSection.style.display = payment.value === 'bank' ? 'block' : 'none';
});


if (delivery) {
    delivery.dispatchEvent(new Event('change'));
}
if (payment) {
    payment.dispatchEvent(new Event('change'));
}


form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('[CHECKOUT] Form submitted');

    const rawCart = JSON.parse(localStorage.getItem('cart') || '[]');

    if (!Array.isArray(rawCart) || rawCart.length === 0) {
        alert('Your cart is empty');
        return;
    }

    const cart = rawCart
        .map(item => (item && (item.title || item.name || '')).toString().trim())
        .filter(name => name.length > 0);

    if (cart.length === 0) {
        alert('Your cart is empty');
        return;
    }

    const data = {
        name: document.getElementById('name')?.value || '',
        phone: document.getElementById('phone')?.value || '',
        email: document.getElementById('email')?.value || '',
        delivery: delivery?.value || '',
        address: document.getElementById('address')?.value || '',
        payment: payment?.value || '',
        card_number: document.getElementById('card_number')?.value || '',
        card_expiry: document.getElementById('card_expiry')?.value || '',
        card_cvv: document.getElementById('card_cvv')?.value || '',
        iban: document.getElementById('iban')?.value || '',
        cart
    };

    try {
        const res = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            alert(result.error || 'Failed to create order');
            return;
        }

        const status = result.order?.status || result.message || 'Order created';
        alert(`Order created: ${status}`);
        localStorage.removeItem('cart');
        window.location.href = '/';
    } catch (err) {
        alert('Error: ' + err.message);
    }
});
