document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('soporte-form');

    form.addEventListener('submit', function(e) {
        //e.preventDefault(); (me impedía enviar el formulario)
    
        
    
        alert('Mensaje enviado!');
    });
});