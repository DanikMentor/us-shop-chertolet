
(function () {
    const getCart = () => {
        try {
            return JSON.parse(localStorage.getItem('cart') || '[]');
        } catch (e) {
            return [];
        }
    };

    const setCart = (cart) => {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        updateCartTotal();
    };

    const updateCartCount = () => {
        const el = document.getElementById('cart-count');
        const totalEl = document.getElementById('cart-count-total');
        const count = getCart().length;
        if (el) el.textContent = count;
        if (totalEl) totalEl.textContent = count;
    };

    const updateCartTotal = () => {
        const el = document.getElementById('cart-total');
        if (el) {
            const total = getCart().reduce((sum, item) => sum + (Number(item.price) || 0), 0);
            el.textContent = total.toLocaleString();
        }
    };

    const addToCart = (item) => {
        const cart = getCart();
        cart.push(item);
        setCart(cart);
    };

    const removeFromCart = (idx) => {
        const cart = getCart();
        cart.splice(idx, 1);
        setCart(cart);
        renderCartPage();
    };

    const clearCart = () => {
        setCart([]);
        renderCartPage();
    };

    const createCartCard = (item, idx) => {
        const card = document.createElement('article');
        card.className = 'car-card';
        card.innerHTML = `
            <div class="car-image">
                <img src="${item.img || ''}" alt="${item.title}" />
            </div>
            <div class="car-details">
                <div>
                    <div class="car-header">
                        <h2 class="car-title">${item.title}</h2>
                        <span class="car-price">${Number(item.price).toLocaleString()} €</span>
                    </div>
                </div>
                <div class="car-actions">
                    <button class="btn-clear">Remove</button>
                </div>
            </div>
        `;
        card.querySelector('.btn-clear').addEventListener('click', () => removeFromCart(idx));
        return card;
    };

    const renderCartPage = () => {
        const container = document.getElementById('cart-items');
        if (!container) return;
        
        container.innerHTML = '';
        const cart = getCart();
        
        if (cart.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-shopping-cart"></i>
                    <p>Your cart is empty</p>
                    <a href="/">Continue Shopping</a>
                </div>
            `;
        } else {
            const list = document.createElement('div');
            list.className = 'cart-list';
            cart.forEach((item, idx) => list.appendChild(createCartCard(item, idx)));
            container.appendChild(list);
        }
        
        updateCartTotal();
    };

    document.addEventListener('DOMContentLoaded', () => {
        updateCartCount();
        // ai
        const normalizePrice = (raw) => {
            if (raw == null) return 0;
            const s = String(raw).replace(/[,\s€\$£]/g, '').replace(/[^0-9.\-]/g, '');
            const v = parseFloat(s);
            return Number.isFinite(v) ? v : 0;
        };

        document.querySelectorAll('.btn-add').forEach((btn) => {
            btn.addEventListener('click', () => {
                const card = btn.closest('.car-card');
                if (!card) return;
                const rawPrice = card.dataset.price || card.querySelector('.car-price')?.textContent || '0';
                const item = {
                    title: (card.dataset.title || card.querySelector('.car-title')?.textContent || 'Item').trim(),
                    price: normalizePrice(rawPrice),
                    img: card.querySelector('img')?.src || ''
                };
                addToCart(item);
                btn.textContent = 'Added';
                setTimeout(() => btn.textContent = 'Add to cart', 1000);
            });
        });
        renderCartPage();
        document.getElementById('clear-cart')?.addEventListener('click', clearCart);
    });

    window.__cart = { getCart, addToCart, updateCartCount };
})();
