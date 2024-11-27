document.addEventListener('DOMContentLoaded', function () {
    const categoryHeaders = document.querySelectorAll('.category-header');

    categoryHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const wasActive = header.classList.contains('active');
            
            // Cerrar todas las categorías
            categoryHeaders.forEach(otherHeader => {
                otherHeader.classList.remove('active');
                otherHeader.nextElementSibling.classList.remove('active');
            });

            // Si el header clickeado no estaba activo, abrirlo
            if (!wasActive) {
                header.classList.add('active');
                header.nextElementSibling.classList.add('active');
            }
        });
    });

    // Inicializar los íconos de Feather
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});
