document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias del DOM para modales y menús ---
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const btnIniciarAhora = document.getElementById('btn-iniciar-ahora');

    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    
    const closeLoginModal = document.getElementById('close-login-modal');
    const closeRegisterModal = document.getElementById('close-register-modal');
    const linkRegistroModal = document.getElementById('link-registro-modal');
    
    const registroTitulo = document.getElementById('registro-titulo');
    const registroTipoInput = document.getElementById('registro-tipo');
    const campoEspecialidad = document.getElementById('campo-especialidad');

    // --- LÓGICA DE NAVEGACIÓN Y MODALES ---
    function mostrarModalRegistro(rol) {
        if (loginModal) loginModal.style.display = 'none';
        if (!registerModal) return;

        registerModal.style.display = 'flex';
        if (registroTipoInput) registroTipoInput.value = rol;
        if (registroTitulo) registroTitulo.textContent = `Registro como ${rol === 'medico' ? 'Médico' : 'Paciente'}`;
        
        if (campoEspecialidad) {
            campoEspecialidad.style.display = rol === 'medico' ? 'block' : 'none';
        }
    }

    // Eventos de botones de la Landing Page
    loginBtn?.addEventListener('click', () => {
        if (loginModal) loginModal.style.display = 'flex';
    });
    
    registerBtn?.addEventListener('click', () => {
        if (registerModal) registerModal.style.display = 'flex';
        // Por defecto, mostrar registro como paciente
        if (registroTipoInput) registroTipoInput.value = 'paciente';
        if (registroTitulo) registroTitulo.textContent = 'Registro como Paciente';
        if (campoEspecialidad) campoEspecialidad.style.display = 'none';
    });
    
    // Botón "Empezar Ahora"
    btnIniciarAhora?.addEventListener('click', () => {
        if (loginModal) loginModal.style.display = 'flex';
    });

    // Cierre de modales
    closeLoginModal?.addEventListener('click', () => { 
        if (loginModal) loginModal.style.display = 'none'; 
    });
    
    closeRegisterModal?.addEventListener('click', () => { 
        if (registerModal) registerModal.style.display = 'none'; 
    });
    
    // Link "Regístrate aquí" en el modal de login
    linkRegistroModal?.addEventListener('click', (e) => {
        e.preventDefault();
        if (loginModal) loginModal.style.display = 'none';
        mostrarModalRegistro('paciente'); 
    });
    
    // Cerrar modales al hacer clic fuera de ellos
    window.addEventListener('click', (e) => {
        if (loginModal && e.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (registerModal && e.target === registerModal) {
            registerModal.style.display = 'none';
        }
    });

    // --- CHATBOT TOGGLE ---
    const chatbotBtn = document.getElementById('chatbot-btn');
    const chatbotWindow = document.getElementById('chatbot-window');
    
    chatbotBtn?.addEventListener('click', () => {
        if (chatbotWindow) {
            chatbotWindow.classList.toggle('active');
        }
    });
});