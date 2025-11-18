/**
 * Sistema de Incidencias - Main JavaScript
 * Funcionalidades principales y utilidades
 */

// ============================================
// GESTIÓN DE ALERTAS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Cerrar alertas automáticamente después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 300);
        }, 5000);
    });

    // ===== PREVENIR SELECCIÓN MÚLTIPLE EN MENÚ =====
    const menuLinks = document.querySelectorAll('.menu a');
    
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Solo remover active de otros links, no de este
            menuLinks.forEach(otherLink => {
                if (otherLink !== this && !otherLink.hasAttribute('data-no-active')) {
                    otherLink.classList.remove('active');
                }
            });
        });
    });
});

// Cerrar alerta manualmente
function closeAlert(button) {
    const alert = button.closest('.alert');
    if (alert) {
        alert.style.transition = 'opacity 0.3s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }
}

// ============================================
// FORMULARIOS Y VALIDACIÓN
// ============================================

// Toggle para tipo de incidente "Otro"
function toggleOtro() {
    const select = document.getElementById('tipo_incidente');
    const otroDiv = document.getElementById('otroTipo');
    if (select && otroDiv) {
        otroDiv.style.display = select.value === 'Otro' ? 'block' : 'none';
    }
}

// Confirmar eliminaciones
function confirmarEliminacion(mensaje) {
    return confirm(mensaje || '¿Estás seguro de que deseas eliminar este elemento?');
}

// Validar formulario antes de enviar
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    // Validación básica
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let esValido = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('input-error');
            esValido = false;
            setTimeout(() => input.classList.remove('input-error'), 3000);
        }
    });
    
    return esValido;
}

// ============================================
// UTILIDADES DE TABLA
// ============================================

// Seleccionar todas las filas
function seleccionarTodas(checkboxId) {
    const checkbox = document.getElementById(checkboxId);
    const filas = document.querySelectorAll('.tabla-fila');
    
    filas.forEach(fila => {
        const inputCheck = fila.querySelector('input[type="checkbox"]');
        if (inputCheck) {
            inputCheck.checked = checkbox.checked;
        }
    });
}

// Obtener filas seleccionadas
function obtenerSeleccionadas() {
    const checkboxes = document.querySelectorAll('.tabla-fila input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

// ============================================
// BÚSQUEDA Y FILTROS
// ============================================

// Búsqueda en tiempo real
function buscar(inputId, targetClass) {
    const input = document.getElementById(inputId);
    const items = document.querySelectorAll(`.${targetClass}`);
    
    if (!input) return;
    
    input.addEventListener('keyup', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        
        items.forEach(item => {
            if (item.textContent.toLowerCase().includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Filtrar por status
function filtrarPorStatus(status) {
    const items = document.querySelectorAll('[data-status]');
    
    items.forEach(item => {
        if (status === 'todos' || item.getAttribute('data-status') === status) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// ============================================
// UTILIDADES DE FECHA Y HORA
// ============================================

// Formatear fecha
function formatearFecha(fecha) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(fecha).toLocaleDateString('es-ES', options);
}

// Formatear hora
function formatearHora(hora) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(`2000-01-01 ${hora}`).toLocaleTimeString('es-ES', options);
}

// ============================================
// UTILITARIOS DE DOM
// ============================================

// Mostrar elemento con animación
function mostrarElemento(elementoId, velocidad = 300) {
    const elemento = document.getElementById(elementoId);
    if (elemento) {
        elemento.style.display = 'block';
        elemento.style.animation = `fadeIn ${velocidad}ms ease-in`;
    }
}

// Ocultar elemento con animación
function ocultarElemento(elementoId, velocidad = 300) {
    const elemento = document.getElementById(elementoId);
    if (elemento) {
        elemento.style.animation = `fadeOut ${velocidad}ms ease-out`;
        setTimeout(() => {
            elemento.style.display = 'none';
        }, velocidad);
    }
}

// Copiar al portapapeles
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        mostrarNotificacion('Copiado al portapapeles', 'success');
    }).catch(() => {
        mostrarNotificacion('Error al copiar', 'error');
    });
}

// ============================================
// NOTIFICACIONES
// ============================================

// Mostrar notificación tipo toast
function mostrarNotificacion(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${tipo} shadow-lg fixed top-4 right-4 max-w-xs z-50`;
    toast.innerHTML = `
        <i class="mdi mdi-${
            tipo === 'success' ? 'check-circle' : 
            tipo === 'error' ? 'alert-circle' : 
            tipo === 'warning' ? 'alert' : 
            'information'
        }"></i>
        <span>${mensaje}</span>
        <button onclick="this.parentElement.remove()" class="btn btn-sm btn-ghost">
            <i class="mdi mdi-close"></i>
        </button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

// ============================================
// LOADING Y PROCESAMIENTO
// ============================================

// Mostrar loader
function mostrarLoader(mensaje = 'Cargando...') {
    const loader = document.createElement('div');
    loader.id = 'main-loader';
    loader.className = 'fixed inset-0 bg-black/50 flex items-center justify-center z-50';
    loader.innerHTML = `
        <div class="text-center">
            <div class="loading loading-spinner loading-lg text-primary mb-4"></div>
            <p class="text-white text-lg">${mensaje}</p>
        </div>
    `;
    document.body.appendChild(loader);
}

// Ocultar loader
function ocultarLoader() {
    const loader = document.getElementById('main-loader');
    if (loader) {
        loader.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => loader.remove(), 300);
    }
}

// ============================================
// MANEJO DE ERRORES
// ============================================

// Capturar errores globales
window.addEventListener('error', (e) => {
    console.error('Error:', e.message);
    mostrarNotificacion('Ocurrió un error. Por favor, intenta de nuevo.', 'error');
});

// ============================================
// UTILIDADES DE DESARROLLO
// ============================================

// Log con estilo
function log(titulo, contenido, tipo = 'info') {
    const estilos = {
        info: 'color: #3b82f6; font-weight: bold;',
        success: 'color: #10b981; font-weight: bold;',
        warning: 'color: #f59e0b; font-weight: bold;',
        error: 'color: #ef4444; font-weight: bold;'
    };
    
    console.log(`%c[${titulo}]`, estilos[tipo], contenido);
}

// ============================================
// INICIALIZACIÓN
// ============================================

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    log('Sistema', 'Sistema de Incidencias iniciado', 'success');
    
    // Agregar animaciones CSS si no existen
    if (!document.getElementById('animations-style')) {
        const style = document.createElement('style');
        style.id = 'animations-style';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; transform: translateY(0); }
                to { opacity: 0; transform: translateY(-10px); }
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-100%); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            .input-error {
                border-color: #ef4444 !important;
                animation: slideIn 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }
});
