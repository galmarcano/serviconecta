document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('soporte-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
    
        // Código para enviar el formulario (si es necesario)
    
        alert('Mensaje enviado!');
    });
});