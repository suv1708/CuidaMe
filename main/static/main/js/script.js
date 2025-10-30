document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias del DOM y variables de estado ---
    const loginBtn = document.getElementById('btn-login');
    const registerBtn = document.getElementById('btn-register');
    const registerMenu = document.getElementById('register-menu');
    const registerMedicoLink = document.getElementById('register-medico');
    const registerPacienteLink = document.getElementById('register-paciente');
    const btnIniciarAhora = document.getElementById('btn-iniciar-ahora');

    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    
    const closeLoginModal = document.getElementById('close-login-modal');
    const closeRegisterModal = document.getElementById('close-register-modal');
    const linkRegistroModal = document.getElementById('link-registro-modal');
    
    function mostrarModalRegistro() {
        if (loginModal) loginModal.style.display = 'none';
        if (!registerModal) return;

        registerModal.style.display = 'flex';
        registroTitulo.textContent = `Registro como usuario`;
        
        registerMenu.classList.remove('show');
    }

    // Eventos de botones de la Landing Page
    loginBtn?.addEventListener('click', () => {
        if (loginModal) loginModal.style.display = 'flex';
        if (registerMenu) registerMenu.classList.remove('show');
    });
    
    registerBtn?.addEventListener('click', () => {
        mostrarModalRegistro('paciente')
    });
    
    // Botón "Empezar Ahora"
    btnIniciarAhora?.addEventListener('click', () => {
        if (loginModal) loginModal.style.display = 'flex';
    });

    // Cierre de modales
    closeLoginModal?.addEventListener('click', () => { if (loginModal) loginModal.style.display = 'none'; });
    closeRegisterModal?.addEventListener('click', () => { if (registerModal) registerModal.style.display = 'none'; });
    
    // Link "Regístrate aquí"
    linkRegistroModal?.addEventListener('click', (e) => {
        e.preventDefault();
        mostrarModalRegistro('paciente'); 
    });
    
    // Cerrar menú de registro al hacer clic fuera
    document.addEventListener('click', (e) => {
        if (registerMenu && registerBtn && !registerBtn.contains(e.target) && !registerMenu.contains(e.target)) {
            registerMenu.classList.remove('show');
        }
    });

});