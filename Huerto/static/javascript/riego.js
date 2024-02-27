document.addEventListener('DOMContentLoaded', (event) => {
    const plantas = document.querySelectorAll('.planta');
    let algunaNecesitaRiego = false; // Bandera para controlar si alguna planta necesita riego

    plantas.forEach((planta) => {
        const necesitaRiego = planta.getAttribute('data-regar') === 'True';
        if (necesitaRiego) {
            algunaNecesitaRiego = true; // Actualizamos la bandera si alguna planta necesita riego
            planta.style.color = 'red'; // Cambiamos el color de la fuente a rojo
        }
    });

    if (algunaNecesitaRiego) {
        alert('Algunas plantas necesitan ser regadas.'); // Mostramos el alert solo una vez
    }
});
