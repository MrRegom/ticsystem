document.addEventListener('DOMContentLoaded', () => {
  loadConfig();
});

// ==========================================
// API Calls
// ==========================================

function getPayload() {
  return {
    host: document.getElementById('smtp-host').value.trim(),
    puerto: document.getElementById('smtp-port').value.trim(),
    usuario: document.getElementById('smtp-user').value.trim(),
    password: document.getElementById('smtp-pass').value.trim(),
    remitente_por_defecto: document.getElementById('smtp-sender').value.trim(),
    use_tls: document.getElementById('smtp-tls').checked
  };
}

function loadConfig() {
  fetch('/correos/api/config/')
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById('smtp-host').value = data.data.host || '';
        document.getElementById('smtp-port').value = data.data.puerto || '';
        document.getElementById('smtp-user').value = data.data.usuario || '';
        document.getElementById('smtp-pass').value = data.data.password || '';
        document.getElementById('smtp-sender').value = data.data.remitente_por_defecto || '';
        document.getElementById('smtp-tls').checked = data.data.use_tls;
      }
    })
    .catch(err => console.error("Error cargando config:", err));
}

function saveConfig() {
  const btn = document.getElementById('btn-save');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
  btn.disabled = true;

  const payload = getPayload();

  fetch('/correos/api/config/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    btn.innerHTML = '<i class="fas fa-save"></i> Guardar Configuración';
    btn.disabled = false;
    
    if (data.success) {
      showToast(data.message);
    } else {
      showToast(data.message, true);
    }
  })
  .catch(err => {
    btn.innerHTML = '<i class="fas fa-save"></i> Guardar Configuración';
    btn.disabled = false;
    showToast('Fallo de conexión.', true);
  });
}

function testConnection() {
  const btn = document.getElementById('btn-test');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Probando...';
  btn.disabled = true;

  const payload = getPayload();

  fetch('/correos/api/test/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Correo de Prueba';
    btn.disabled = false;
    
    if (data.success) {
      showToast(data.message);
    } else {
      showToast(data.message, true);
    }
  })
  .catch(err => {
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Correo de Prueba';
    btn.disabled = false;
    showToast('Fallo de conexión o timeout SMTP.', true);
  });
}

// ==========================================
// Custom Microsoft Toast
// ==========================================
function showToast(message, isError = false) {
  const toast = document.getElementById('ms-toast');
  const icon = document.getElementById('ms-toast-icon');
  const text = document.getElementById('ms-toast-text');
  
  if (isError) {
    toast.classList.add('error');
    icon.className = 'fas fa-exclamation-circle ms-toast-icon';
  } else {
    toast.classList.remove('error');
    icon.className = 'fas fa-check-circle ms-toast-icon';
  }
  
  text.innerText = message;
  toast.classList.add('show');
  
  setTimeout(() => {
    toast.classList.remove('show');
  }, 4000);
}

// ==========================================
// Utils
// ==========================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
