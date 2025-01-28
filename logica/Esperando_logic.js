// Cargar animación de Lottie
const animation = lottie.loadAnimation({
    container: document.getElementById('loading'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/animations/loading.json' // Cambia esto a la ruta de tu animación
});