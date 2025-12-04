// Este es el contenido de GrupoSantaMaria/GrupoSantaMaria/static/js/main.js

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

function handleCredentialResponse(response) {
    console.log("Google ID Token: " + response.credential);
}
// En tu propio archivo JS, o en un {% block extra_js %} en plantilla.html
$(document).ready(function() {
    $(".blog-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: false,
        dots: false,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });
});
// CÓDIGO A REEMPLAZAR DENTRO DE main.js
$('.header-carousel').owlCarousel({
    // --- Configuración de velocidad y transición ---
    autoplay: true,
    autoplayTimeout: 15000, // <--- **15,000 milisegundos (15 segundos)**
    autoplayHoverPause: true, // Pausa si el ratón está encima
    smartSpeed: 1000,         // Velocidad de la animación
    
    // --- Efecto de Transición (Desvanecimiento) ---
    // El mejor efecto tipo "diapositiva" que Owl Carousel ofrece.
    animateOut: 'fadeOut', 
    animateIn: 'fadeIn',  
    
    // --- Opciones de diseño ---
    items: 1,
    loop: true,
    dots: false,
    nav: false,
    // (Asegúrate de dejar cualquier otra opción que ya estuviera aquí originalmente)
});

