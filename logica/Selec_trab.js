// scripts.js

let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const totalSlides = slides.length;
const prevButton = document.getElementById('prev-slide');
const nextButton = document.getElementById('next-slide');
const buttons = document.querySelectorAll('.custom-button');
const forms = document.querySelectorAll('.custom-form-container');

// Función para mostrar el slide actual
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });

    // Ocultar cualquier formulario abierto al cambiar de slide
    forms.forEach(form => form.classList.add('hidden'));
}

// Evento: Navegación hacia atrás
prevButton.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
});

// Evento: Navegación hacia adelante
nextButton.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
});

// Evento: Mostrar/ocultar formulario al hacer clic en un botón
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const formId = button.dataset.form;
        const form = document.getElementById(formId);

        // Si el formulario ya está visible, ocultarlo
        if (!form.classList.contains('hidden')) {
            form.classList.add('hidden');
        } else {
            // Ocultar cualquier formulario visible antes de mostrar el actual
            forms.forEach(f => f.classList.add('hidden'));
            form.classList.remove('hidden');
        }
    });
});

// Mostrar el primer slide al cargar
showSlide(currentSlide);
