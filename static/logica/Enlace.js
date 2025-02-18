document.getElementById('convertButton').addEventListener('click', function (event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario
    
    const form = document.getElementById('pdfForm');
    const formData = new FormData(form);

    fetch('http://127.0.0.1:5000/convert_pdf', {  // Asegúrate de usar el mismo puerto
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Redirigir a la nueva página
        } else {
            return response.json().then(data => {
                alert('Error al convertir PDF.');
            });
        }
    })
    .catch(error => {
        console.error('Error en la conversión:', error);
        alert('Hubo un problema en el servidor.');
    });
});
