document.getElementById('convertButton').addEventListener('click', function () {
    const form = document.getElementById('pdfForm');
    const formData = new FormData(form);

    // Redirigir a la página de carga
    window.location.href = 'Esperando.html';

    // Enviar archivo al servidor Flask
    fetch('http://127.0.0.1:5000/convert_pdf', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            // Redirigir a la página de resultado al completar la conversión
            window.location.href = 'resultado.html';
        } else {
            throw new Error('Error al convertir PDF.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al procesar el archivo.');
    });
});
