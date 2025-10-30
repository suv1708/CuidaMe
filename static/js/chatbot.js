document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias del DOM ---
    const chatbotBtn = document.getElementById("chatbot-btn");
    const chatbotWindow = document.getElementById("chatbot-window");
    const messagesDiv = document.getElementById("chatbot-messages");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // --- Variables de Estado y Datos ---
    const usuarioActualEmail = localStorage.getItem('usuarioActual');
    const tipoUsuario = localStorage.getItem('tipoUsuario');

    // Función para obtener los datos del almacenamiento local de forma segura
    function cargarDatos() {
        return {
            pacientes: JSON.parse(localStorage.getItem('pacientes')) || [],
            citas: JSON.parse(localStorage.getItem('citas')) || [],
            medicamentos: JSON.parse(localStorage.getItem('medicamentos')) || [],
            alergias: JSON.parse(localStorage.getItem('alergias')) || [],
            vacunas: JSON.parse(localStorage.getItem('vacunas')) || [],
        };
    }

    const data = cargarDatos();
    const usuario = data.pacientes.find(p => p.email === usuarioActualEmail);
    const pacienteId = usuario ? usuario.id : null;

    // --- Lógica del Chatbot ---

    // 1. Mostrar/Ocultar
    chatbotBtn?.addEventListener("click", () => {
        if (chatbotWindow) {
            if (chatbotWindow.style.display === "flex") {
                chatbotWindow.style.display = "none";
            } else {
                chatbotWindow.style.display = "flex";
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                if (messagesDiv.children.length === 0) {
                    agregarMensaje(
                        `🤖 ¡Hola! Soy tu Asistente de Cuídame. ${usuario ? 'Veo que eres ' + usuario.nombre + '.' : 'Inicia sesión para ver tus datos.'} ¿En qué te puedo ayudar hoy?`, 
                        "bot"
                    );
                    agregarMensaje("🤖 Puedes preguntarme sobre tu *próxima cita*, tus *medicamentos activos* o si tienes alguna *alergia*.", "bot");
                }
            }
        }
    });

    // 2. Renderizado de Mensajes
    function agregarMensaje(texto, tipo) {
        const msg = document.createElement("div");
        msg.className = `msg ${tipo}`;
        msg.textContent = texto;
        messagesDiv.appendChild(msg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // 3. Función de Respuesta Inteligente
    function responderInteligente(pregunta) {
        const texto = pregunta.toLowerCase();

        // ------------------ Respuestas Contextuales (Si el usuario está logueado) ------------------
        if (pacienteId) {
            // A. PRÓXIMA CITA
            if (texto.includes('próxima cita') || texto.includes('cuando tengo cita') || texto.includes('cita pendiente')) {
                const citasUsuario = data.citas.filter(c => c.pacienteId === pacienteId);
                const hoy = new Date();
                const proximaCita = citasUsuario
                    .filter(c => new Date(c.fecha) >= hoy)
                    .sort((a, b) => new Date(a.fecha) - new Date(b.fecha))[0];

                if (proximaCita) {
                    const fecha = new Date(proximaCita.fecha).toLocaleString('es-ES');
                    return `📅 Tu próxima cita es el **${fecha}** con el Dr./Dra. ${proximaCita.medico || 'no especificado'}.`;
                } else {
                    return `✅ ¡Felicidades! No tienes citas pendientes registradas en tu agenda.`;
                }
            }

            // B. MEDICAMENTOS ACTIVOS
            if (texto.includes('medicamentos') || texto.includes('tomo') || texto.includes('tratamiento')) {
                const medsUsuario = data.medicamentos.filter(m => m.pacienteId === pacienteId);

                if (medsUsuario.length > 0) {
                    const listaMeds = medsUsuario.map(m => `**${m.nombre}** (${m.dosis} - ${m.frecuencia})`).join(', ');
                    return `💊 Actualmente tienes **${medsUsuario.length}** medicamentos activos: ${listaMeds}. No olvides seguir tus recordatorios.`;
                } else {
                    return `✅ No tienes medicamentos activos registrados. ¡Excelente!`;
                }
            }

            // C. ALERGIAS REGISTRADAS
            if (texto.includes('alergia') || texto.includes('alergias') || texto.includes('soy alergico')) {
                const alergiasUsuario = data.alergias.filter(a => a.pacienteId === pacienteId);

                if (alergiasUsuario.length > 0) {
                    const listaAlergias = alergiasUsuario.map(a => `${a.sustancia} (Reacción: ${a.reaccion})`).join('; ');
                    return `⚠️ ¡Cuidado! Tienes **${alergiasUsuario.length}** alergias registradas: ${listaAlergias}. Asegúrate de informarlo a tu médico.`;
                } else {
                    return `✅ No tienes alergias registradas en tu historial.`;
                }
            }
        } 
        
        // ------------------ Respuestas Generales (Fallback) ------------------
        
        // Saludos
        const saludos = ['hola', 'que tal', 'saludos', 'buen día'];
        if (saludos.some(s => texto.includes(s))) {
            return `¡Hola! 👋 Soy tu Asistente de Cuídame. ${usuario ? 'Soy inteligente y puedo revisar tus datos.' : ''} ¿En qué te puedo ayudar?`;
        }

        // Si no está logueado o la pregunta no es contextual
        if (!pacienteId && !usuarioActualEmail) {
            return "🔒 Debes **iniciar sesión como Paciente** para que pueda revisar tu información personal (citas, medicamentos, alergias).";
        }
        
        // Si no entendió
        return `❓ Lo siento, no entendí bien la pregunta. Por favor, sé más específico sobre: **Próxima cita**, **Medicamentos activos** o **Alergias**.`;
    }

    // 4. Envío de Mensajes
    sendBtn?.addEventListener("click", () => {
        const texto = userInput.value.trim();
        if (!texto) return;

        agregarMensaje("🙋 " + texto, "user");
        
        // Simular un retraso para que parezca que está "pensando"
        setTimeout(() => {
            const respuesta = responderInteligente(texto);
            agregarMensaje("🤖 " + respuesta, "bot");
        }, 800);

        userInput.value = "";
    });

    userInput?.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendBtn?.click();
        }
    });
});