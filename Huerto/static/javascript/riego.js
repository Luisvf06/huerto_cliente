document.addEventListener('DOMContentLoaded', (event) => {
    const plantas = document.querySelectorAll('.planta');
    let algunaNecesitaRiego = false; 

    plantas.forEach((planta) => {
        const necesitaRiego = planta.getAttribute('data-regar') === 'True';
        if (necesitaRiego) {
            algunaNecesitaRiego = true; 
            planta.style.color = 'red'; 
        }
    });
    
    if (algunaNecesitaRiego) {
        alert('Algunas plantas necesitan ser regadas.'); 
    }
});
