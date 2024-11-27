    // Inicializar los iconos Feather
    feather.replace();

    // Filtro móvil toggle
    const mobileFilterToggle = document.getElementById('mobile-filter-toggle');
    const filtersContainer = document.querySelector('.filters-container');

    mobileFilterToggle.addEventListener('click', () => {
        filtersContainer.classList.toggle('expanded');
        const icon = mobileFilterToggle.querySelector('i');
        icon.style.transform = filtersContainer.classList.contains('expanded') ? 'rotate(180deg)' : '';
    });

    // Toggle para categorías
    document.querySelectorAll('.category-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const items = toggle.nextElementSibling;
            const icon = toggle.querySelector('i');
            items.classList.toggle('expanded');
            icon.style.transform = items.classList.contains('expanded') ? 'rotate(180deg)' : '';
        });
    });
    function countChars(paragraph) {
        string = paragraph.textContent
    }
    function filterProducts() {
        const minPrice = parseFloat(document.getElementById('minPrice').value) || 0;
        const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;

        const products = document.querySelectorAll('.product-card');

        products.forEach(product => {
            const price = parseFloat(product.getAttribute('data-price'));
            if (price >= minPrice && price <= maxPrice) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    }
    
    // Funcionalidad para redirigir
    function redirectToDetails(button) {
        var productId = button.getAttribute('data-id');
        window.location.href = '/detalles/' + productId;
    }
    // Funcionalidad de búsqueda
    function setupSearch(searchInput) {
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();
            document.querySelectorAll('.product-card').forEach(card => {
                const name = card.querySelector('h3').textContent.toLowerCase();
                const description = card.querySelector('.product-description').textContent.toLowerCase();
                card.style.display = (name.includes(searchTerm) || description.includes(searchTerm)) ? 'block' : 'none';
            });
        });
    }

    // Funcionalidad de orden
    function setupSort(selectElement) {
        selectElement.addEventListener('change', () => {
            const selectedValue = selectElement.value;
            const products = Array.from(document.querySelectorAll('.product-card'));
            const container = document.querySelector('.grid');

            products.sort((a, b) => {
                const nameA = a.querySelector('h3').textContent.toLowerCase();
                const nameB = b.querySelector('h3').textContent.toLowerCase();
                const priceA = parseFloat(a.querySelector('.text-xl').textContent.replace('₡', '').replace(',', ''));
                const priceB = parseFloat(b.querySelector('.text-xl').textContent.replace('₡', '').replace(',', ''));

                switch (selectedValue) {
                    case 'precio-bajo': return priceA - priceB;
                    case 'precio-alto': return priceB - priceA;
                    case 'nombre-az': return nameA.localeCompare(nameB);
                    case 'nombre-za': return nameB.localeCompare(nameA);
                    default: return 0;
                }
            });

            products.forEach(product => container.appendChild(product));
        });
    }

    // Filtro por categorías (escritorio)
    function setupCategoryFilterDesktop(container) {
        const checkboxes = container.querySelectorAll('.category-checkbox');

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                const selectedCategories = Array.from(checkboxes)
                    .filter(checkbox => checkbox.checked)
                    .map(checkbox => checkbox.value);

                document.querySelectorAll('.product-card').forEach(card => {
                    const category = card.querySelector('.product-category').textContent.trim();
                    if (selectedCategories.length === 0 || selectedCategories.includes(category)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // Filtro por categorías (móvil)
    function setupCategoryFilterMobile(container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                const selectedCategories = Array.from(checkboxes)
                    .filter(checkbox => checkbox.checked)
                    .map(checkbox => checkbox.nextElementSibling.textContent.trim());

                document.querySelectorAll('.product-card').forEach(card => {
                    const category = card.querySelector('.product-category').textContent.trim();
                    if (selectedCategories.length === 0 || selectedCategories.includes(category)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // Inicializar búsqueda y orden para móvil y escritorio
    setupSearch(document.getElementById('mobile-search'));
    setupSearch(document.getElementById('desktop-search'));
    setupSort(document.getElementById('mobile-order-select'));
    setupSort(document.getElementById('desktop-order-select'));

    // Inicializar filtros por categorías
    setupCategoryFilterDesktop(document.getElementById('category-filters'));
    setupCategoryFilterMobile(document.querySelector('.category-items'));