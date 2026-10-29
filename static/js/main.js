// Main frontend JavaScript for PC mart

let allProducts = [];

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadCategories();
    loadProducts();
});

/**
 * Setup UI interaction event listeners
 */
function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const resetAllBtn = document.getElementById('resetAllBtn');

    // Debounced live search
    let debounceTimer;
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            loadProducts();
        }, 250);
    });

    // Category change
    categoryFilter.addEventListener('change', () => {
        loadProducts();
    });

    // Clear search input button
    clearSearchBtn.addEventListener('click', () => {
        if (searchInput.value.trim() !== '') {
            searchInput.value = '';
            loadProducts();
        }
    });

    // Reset filters button
    resetAllBtn.addEventListener('click', () => {
        searchInput.value = '';
        categoryFilter.value = 'all';
        loadProducts();
    });
}

/**
 * Fetch available categories from Backend API and populate dropdown
 */
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        if (data.success && Array.isArray(data.categories)) {
            const select = document.getElementById('categoryFilter');
            data.categories.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                select.appendChild(opt);
            });
        }
    } catch (err) {
        console.error('Error loading categories:', err);
    }
}

/**
 * Fetch products from Backend API with active filters
 */
async function loadProducts() {
    const search = document.getElementById('searchInput').value.trim();
    const category = document.getElementById('categoryFilter').value;

    const spinner = document.getElementById('loadingSpinner');
    const noProducts = document.getElementById('noProductsFound');
    const grid = document.getElementById('productGrid');
    const counter = document.getElementById('productCount');

    // Show spinner
    spinner.classList.remove('d-none');
    noProducts.classList.add('d-none');
    grid.innerHTML = '';

    try {
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (category && category !== 'all') params.append('category', category);

        const response = await fetch(`/api/products?${params.toString()}`);
        const data = await response.json();

        spinner.classList.add('d-none');

        if (data.success && data.products.length > 0) {
            allProducts = data.products;
            counter.textContent = `${data.products.length} item${data.products.length === 1 ? '' : 's'}`;
            renderProducts(data.products);
        } else {
            allProducts = [];
            counter.textContent = '0 items';
            noProducts.classList.remove('d-none');
        }
    } catch (err) {
        spinner.classList.add('d-none');
        counter.textContent = 'Error';
        grid.innerHTML = `
            <div class="col-12 text-center text-danger py-4">
                <i class="bi bi-wifi-off display-4"></i>
                <p class="mt-2">Failed to load catalogue from server. Please verify the Flask server is running.</p>
            </div>
        `;
        console.error('Error fetching products:', err);
    }
}

function normalizeImageUrl(url) {
    if (!url) return '/static/images/placeholder.svg';
    let u = String(url).trim();
    if (u.startsWith('./')) u = u.substring(1);
    if (!u.startsWith('/') && !u.startsWith('http')) u = '/' + u;
    return u;
}

/**
 * Render product cards into Bootstrap grid.
 * Each card is directly clickable and navigates to the dedicated product page.
 */
function renderProducts(products) {
    const grid = document.getElementById('productGrid');
    grid.innerHTML = '';

    products.forEach(product => {
        const col = document.createElement('div');
        col.className = 'col';

        // Format price in Indian Rupees (₹)
        const formattedPrice = Number(product.price).toLocaleString('en-IN', {
            maximumFractionDigits: 0
        });

        const imageSrc = normalizeImageUrl(product.image_url);

        col.innerHTML = `
            <div class="card h-100 product-card shadow-sm" onclick="window.location.href='/product/${product.id}'" role="button" title="View details for ${escapeHtml(product.name)}">
                <div class="product-card-img-wrapper">
                    <span class="badge bg-primary product-badge">${escapeHtml(product.category)}</span>
                    <img src="${escapeHtml(imageSrc)}" alt="${escapeHtml(product.name)}" loading="lazy" onerror="this.onerror=null; this.src='/static/images/placeholder.svg'">
                </div>
                <div class="card-body d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-baseline mb-1">
                        <small class="text-warning">
                            <i class="bi bi-star-fill"></i> ${product.rating ? product.rating.toFixed(1) : '4.5'}
                        </small>
                        <small class="text-success fw-semibold"><i class="bi bi-check2-circle"></i> In Stock</small>
                    </div>
                    <h5 class="card-title fw-bold text-dark fs-6 mb-2 text-truncate" title="${escapeHtml(product.name)}">
                        ${escapeHtml(product.name)}
                    </h5>
                    <p class="card-text description-truncate mb-3">
                        ${escapeHtml(product.description)}
                    </p>
                    <div class="mt-auto d-flex justify-content-between align-items-center pt-2 border-top">
                        <span class="fs-5 fw-bold text-primary">₹${formattedPrice}</span>
                        <span class="text-muted small"><i class="bi bi-arrow-right-circle text-primary fs-5"></i></span>
                    </div>
                </div>
            </div>
        `;

        grid.appendChild(col);
    });
}

/**
 * HTML escaping helper
 */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
