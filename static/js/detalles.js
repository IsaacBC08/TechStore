// Inicializar los iconos Feather
feather.replace();
function redirectToDetails(button) {
    var redirection = button.getAttribute('data-id');
    window.location.href = redirection
}