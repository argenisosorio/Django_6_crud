// 1. Seleccionamos todos los elementos con clase .toast.
var toastElList = [].slice.call(document.querySelectorAll('.toast'));

// 2. Definimos el objeto de opciones.
var toastOptions = {
    animation: true,   // Aplica la transición de desvanecimiento CSS.
    autohide: true,    // Oculta el toast automáticamente.
    delay: 5000        // Tiempo de espera en milisegundos (5 segundos).
};

// 3. Inicializamos cada Toast con las opciones y lo mostramos.
var toastList = toastElList.map(function (toastEl) {
    // Inicializar instancia con el objeto de opciones.
    var toast = new bootstrap.Toast(toastEl, toastOptions);

    // Mostrar el toast inmediatamente.
    toast.show();

    return toast;
});
