const inputImagen = document.getElementById('imagen');
const vistaPrevia = document.getElementById('vista-previa');
      
        inputImagen.addEventListener('change', () => {
          const archivo = inputImagen.files[0];
          if (archivo) {
            const lector = new FileReader();
      
            lector.addEventListener('load', () => {
              const imagen = document.createElement('img');
              imagen.src = lector.result;
              // Establecer el tamaño de la imagen en 600px x 600px
              imagen.style.width = '250px';
              imagen.style.height = '250px';
      
              vistaPrevia.innerHTML = '';
              vistaPrevia.appendChild(imagen);
      
              const botonEliminar = document.createElement('button');
              botonEliminar.textContent = 'Eliminar';
              botonEliminar.addEventListener('click', () => {
                vistaPrevia.innerHTML = '';
                inputImagen.value = '';
              });
      
              vistaPrevia.appendChild(botonEliminar);
            });
      
            lector.readAsDataURL(archivo);
          }
        });