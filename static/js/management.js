document.addEventListener("DOMContentLoaded", function () {
    const categoriaSelect = document.getElementById("categoria");
    const tipoSelect = document.getElementById("tipo");
    const tipoOptions = tipoSelect.querySelectorAll(".tipo-option");

    // Función que actualiza las subcategorías según la categoría seleccionada
    function actualizarSubcategorias() {
        const categoriaSeleccionada = categoriaSelect.value;
        tipoOptions.forEach(option => {
            const categoriaId = option.getAttribute("data-categoria");
            // Si la opción corresponde a la categoría seleccionada, mostrarla, de lo contrario ocultarla
            if (categoriaId === categoriaSeleccionada) {
                option.classList.remove("hidden");
            } else {
                option.classList.add("hidden");
            }
        });
    }

    // Agregar el evento onchange para actualizar las subcategorías cuando cambie la categoría
    categoriaSelect.addEventListener("change", actualizarSubcategorias);
});

// Obtener el modal y el icono de cierre
const modal = document.getElementById("myModal");

// Seleccionar todos los botones de abrir modal
const openModalBtns = document.querySelectorAll(".openModalBtn");

// Abrir el modal al hacer clic en cualquiera de los botones "Abrir Modal"
openModalBtns.forEach(button => {
    button.onclick = function () {
        modal.classList.remove("hidden");
    }
});

window.onclick = function (event) {
    if (event.target === modal) {
        modal.classList.add("hidden");
    }
}
// Cerrar el modal si el usuario hace clic fuera del contenido
window.onclick = function (event) {
    if (event.target === modal) {
        modal.classList.add("hidden");
    }
}
