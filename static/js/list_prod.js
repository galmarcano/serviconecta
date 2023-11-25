// Seleccionar todos los elementos con la clase .btn-agregar
const buttons = document.querySelectorAll('.btn-agregar');

// Agregar un escucha de eventos a cada botón
buttons.forEach(function(button) {
    button.addEventListener('click', function () {
        const productName = button.getAttribute('data-producto');
        alert('Producto ' + productName + ' agregado al carrito');
    });
});