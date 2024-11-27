document.addEventListener('DOMContentLoaded', function () {
    AOS.init({
        duration: 800,
        once: true,
        offset: 100,
    });

    feather.replace();

    const mobileMenuButton = document.querySelector('[data-collapse-toggle="mobile-menu"]');
    const mobileMenu = document.getElementById('mobile-menu');

    mobileMenuButton.addEventListener('click', function () {
        mobileMenu.classList.toggle('active');
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
