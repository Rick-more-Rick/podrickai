document.getElementById('pdfForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Evita el envío del formulario de forma tradicional

    const formData = new FormData();
    const fileInput = document.getElementById('pdfFile');
    
    formData.append('pdfFile', fileInput.files[0]);

    // Enviar el archivo al servidor Flask
    fetch('http://127.0.0.1:5000/convert_pdf', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())  // Esperamos que nos devuelvan el archivo MP3
    .then(blob => {
        // Crear un enlace para descargar el archivo MP3
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'archivo_convertido.mp3';  // Nombre del archivo descargado
        link.click();
    })
    .catch(error => {
        console.error('Error al convertir PDF:', error);
    });
});