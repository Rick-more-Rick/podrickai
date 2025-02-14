document.getElementById('convertButton').addEventListener('click', function () {
    const form = document.getElementById('pdfForm');
    const formData = new FormData(form);

    fetch('/convert_pdf', {  
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Ocultar el botón y mostrar la animación
            document.getElementById('convertButton').style.display = 'none';
            
            // Cargar la animación Lottie
            let animContainer = document.getElementById('animacion');
            let animation = lottie.loadAnimation({
                container: animContainer,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: '/animacion/tu_animacion.json' // Ruta del archivo JSON
            });

            // Opcional: Redirigir después de que termine la animación
            setTimeout(() => {
                window.location.href = '/esperando';
            }, 50000); // 5 segundos de animación
        } else {
            alert('Error al convertir PDF.');
        }
    })
    
});
