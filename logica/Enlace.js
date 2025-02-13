document.getElementById('convertButton').addEventListener('click', function () {
    const form = document.getElementById('pdfForm');
    const formData = new FormData(form);

    // Enviar archivo al servidor Flask
    fetch('/convert_pdf', {  // Usa la ruta relativa basada en Flask
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            // Redirigir a la página de "Esperando" ya gestionada en Flask
            window.location.href = '/esperando.html';
        } else {
            throw new Error('Error al convertir PDF.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al procesar el archivo.');
    });
});
