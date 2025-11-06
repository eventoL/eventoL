// Datos del juego
const projectsData = {
    linux: {
        name: 'Linux',
        animal: 'Pingüino',
        icon: '🐧',
        curiosity: 'Tux, el pingüino de Linux, fue nombrado así porque Linus Torvalds fue mordido por un pingüino en un zoológico de Australia. ¡El kernel Linux tiene más de 27 millones de líneas de código!'
    },
    firefox: {
        name: 'Firefox',
        animal: 'Panda Rojo',
        icon: '🦊',
        curiosity: 'Firefox originalmente se llamaba "Phoenix" y luego "Firebird". El logo no es un zorro, ¡es un panda rojo! Estos adorables animales están en peligro de extinción.'
    },
    gnu: {
        name: 'GNU',
        animal: 'Ñu',
        icon: '🦬',
        curiosity: 'GNU es un acrónimo recursivo que significa "GNU\'s Not Unix". Fue iniciado por Richard Stallman en 1983 y es la base del movimiento del software libre.'
    },
    python: {
        name: 'Python',
        animal: 'Serpiente',
        icon: '🐍',
        curiosity: 'Python fue creado por Guido van Rossum en 1991. ¡Su nombre viene del grupo de comedia británico "Monty Python", no de la serpiente! Es uno de los lenguajes más populares del mundo.'
    },
    debian: {
        name: 'Debian',
        animal: 'Espiral',
        icon: '🌀',
        curiosity: 'El nombre Debian viene de su creador Ian Murdock y su esposa Debra. La espiral roja representa el crecimiento colaborativo y orgánico de la comunidad cooperativa.'
    },
    php: {
        name: 'PHP',
        animal: 'Elefante',
        icon: '🐘',
        curiosity: 'El elefante de PHP se llama "elePHPant" y fue diseñado en 1998. PHP originalmente significaba "Personal Home Page" pero ahora es "PHP: Hypertext Preprocessor".'
    },
    openssh: {
        name: 'OpenSSH',
        animal: 'Pez Globo',
        icon: '🐡',
        curiosity: 'El pez globo representa la seguridad: cuando se siente amenazado, se infla con espinas. OpenSSH cifra el 90% de las conexiones remotas en Internet, ¡protegiendo millones de servidores!'
    }
};

// Variables del juego
let score = 0;
let matchedPairs = 0;
let draggedElement = null;

// Elementos del DOM
const scoreValue = document.getElementById('scoreValue');
const curiosityModal = document.getElementById('curiosityModal');
const modalIcon = document.getElementById('modalIcon');
const modalTitle = document.getElementById('modalTitle');
const modalCuriosity = document.getElementById('modalCuriosity');
const btnContinue = document.getElementById('btnContinue');
const victoryModal = document.getElementById('victoryModal');
const btnRestart = document.getElementById('btnRestart');

// Inicializar el juego
function initGame() {
    const logoItems = document.querySelectorAll('.logo-item');
    const animalZones = document.querySelectorAll('.animal-zone');

    // Event listeners para logos (drag)
    logoItems.forEach(logo => {
        // Desktop events
        logo.addEventListener('dragstart', handleDragStart);
        logo.addEventListener('dragend', handleDragEnd);

        // Mobile events
        logo.addEventListener('touchstart', handleTouchStart, { passive: false });
        logo.addEventListener('touchmove', handleTouchMove, { passive: false });
        logo.addEventListener('touchend', handleTouchEnd, { passive: false });
    });

    // Event listeners para zonas de animales (drop)
    animalZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('dragleave', handleDragLeave);
        zone.addEventListener('drop', handleDrop);
    });

    // Botones
    btnContinue.addEventListener('click', closeModal);
    btnRestart.addEventListener('click', restartGame);
}

// === DRAG & DROP (Desktop) ===

function handleDragStart(e) {
    if (this.classList.contains('matched')) return;
    
    draggedElement = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.dataset.project);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    
    if (!this.classList.contains('matched')) {
        this.classList.add('drag-over');
    }
    return false;
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    e.preventDefault();

    this.classList.remove('drag-over');

    if (!draggedElement || this.classList.contains('matched')) return;

    const projectId = draggedElement.dataset.project;
    const animalId = this.dataset.animal;

    checkMatch(projectId, animalId, draggedElement, this);

    return false;
}

// === TOUCH (Mobile) ===

let touchStartX, touchStartY;
let touchClone = null;

function handleTouchStart(e) {
    if (this.classList.contains('matched')) return;
    
    e.preventDefault();
    draggedElement = this;
    
    const touch = e.touches[0];
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;

    // Crear clon visual
    touchClone = this.cloneNode(true);
    touchClone.style.position = 'fixed';
    touchClone.style.pointerEvents = 'none';
    touchClone.style.opacity = '0.8';
    touchClone.style.zIndex = '9999';
    touchClone.style.width = this.offsetWidth + 'px';
    touchClone.style.left = (touch.clientX - this.offsetWidth / 2) + 'px';
    touchClone.style.top = (touch.clientY - this.offsetHeight / 2) + 'px';
    document.body.appendChild(touchClone);

    this.classList.add('dragging');
}

function handleTouchMove(e) {
    if (!draggedElement) return;
    e.preventDefault();

    const touch = e.touches[0];
    
    if (touchClone) {
        touchClone.style.left = (touch.clientX - touchClone.offsetWidth / 2) + 'px';
        touchClone.style.top = (touch.clientY - touchClone.offsetHeight / 2) + 'px';
    }

    // Highlight zone under touch
    const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
    const animalZones = document.querySelectorAll('.animal-zone');
    
    animalZones.forEach(zone => {
        zone.classList.remove('drag-over');
    });

    if (elementBelow) {
        const zone = elementBelow.closest('.animal-zone');
        if (zone && !zone.classList.contains('matched')) {
            zone.classList.add('drag-over');
        }
    }
}

function handleTouchEnd(e) {
    if (!draggedElement) return;
    e.preventDefault();

    const touch = e.changedTouches[0];
    const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
    const animalZone = elementBelow ? elementBelow.closest('.animal-zone') : null;

    if (touchClone) {
        touchClone.remove();
        touchClone = null;
    }

    draggedElement.classList.remove('dragging');

    if (animalZone && !animalZone.classList.contains('matched')) {
        const projectId = draggedElement.dataset.project;
        const animalId = animalZone.dataset.animal;
        checkMatch(projectId, animalId, draggedElement, animalZone);
    }

    // Clean up drag-over classes
    document.querySelectorAll('.animal-zone').forEach(zone => {
        zone.classList.remove('drag-over');
    });

    draggedElement = null;
}

// === LÓGICA DEL JUEGO ===

function checkMatch(projectId, animalId, logoElement, animalElement) {
    if (projectId === animalId) {
        // ¡MATCH CORRECTO!
        matchedPairs++;
        score++;
        
        logoElement.classList.add('matched');
        animalElement.classList.add('matched');
        
        updateScore();
        showCuriosity(projectId);
        
        // Verificar victoria
        if (matchedPairs === Object.keys(projectsData).length) {
            setTimeout(showVictory, 1500);
        }
    } else {
        // Match incorrecto - feedback visual
        animalElement.style.animation = 'none';
        setTimeout(() => {
            animalElement.style.animation = '';
        }, 10);
        
        // Shake animation
        logoElement.style.animation = 'shake 0.5s';
        setTimeout(() => {
            logoElement.style.animation = '';
        }, 500);
    }
}

function updateScore() {
    const totalPairs = Object.keys(projectsData).length;
    scoreValue.textContent = `${matchedPairs}/${totalPairs}`;
}

function showCuriosity(projectId) {
    const project = projectsData[projectId];
    
    modalIcon.textContent = project.icon;
    
    // Agregar clase especial si es Debian para mostrar espiral roja
    if (projectId === 'debian') {
        modalIcon.style.color = '#D70A53';
        modalIcon.style.filter = 'drop-shadow(2px 2px 6px rgba(215, 10, 83, 0.3))';
    } else {
        modalIcon.style.color = '';
        modalIcon.style.filter = '';
    }
    
    modalTitle.textContent = `¡Correcto! ${project.name} → ${project.animal}`;
    modalCuriosity.textContent = project.curiosity;
    
    curiosityModal.classList.add('show');
}

function closeModal() {
    curiosityModal.classList.remove('show');
}

function showVictory() {
    victoryModal.classList.add('show');
}

function restartGame() {
    // Reset variables
    score = 0;
    matchedPairs = 0;
    
    // Reset UI
    updateScore();
    
    const logoItems = document.querySelectorAll('.logo-item');
    const animalZones = document.querySelectorAll('.animal-zone');
    
    logoItems.forEach(logo => {
        logo.classList.remove('matched', 'dragging');
    });
    
    animalZones.forEach(zone => {
        zone.classList.remove('matched', 'drag-over');
    });
    
    // Cerrar modales
    victoryModal.classList.remove('show');
    curiosityModal.classList.remove('show');
    
    // Shuffle logos para nueva partida
    shuffleLogos();
}

function shuffleLogos() {
    const container = document.getElementById('logosContainer');
    const items = Array.from(container.children);
    
    // Fisher-Yates shuffle
    for (let i = items.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        container.appendChild(items[j]);
    }
}

// Agregar animación shake al CSS dinámicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    initGame();
    shuffleLogos();
});