document.addEventListener('DOMContentLoaded', () => {
  loadIdentities();
  
  // Search with debounce
  let searchTimeout;
  document.getElementById('search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      loadIdentities(e.target.value);
    }, 400);
  });

  // Auto-search Funcionario when typing RUT
  let rutTimeout;
  document.getElementById('form-rut').addEventListener('input', (e) => {
    if (currentAction !== 'crear') return; // Only auto-fill on create
    const rut = e.target.value.trim();
    let feedback = document.getElementById('rut-feedback');
    if (!feedback) {
        // Create it dynamically if HTML is cached
        feedback = document.createElement('small');
        feedback.id = 'rut-feedback';
        feedback.style = 'display:block; margin-bottom: 12px; color:#0078d4; font-size: 12px; min-height:16px;';
        e.target.parentNode.insertBefore(feedback, e.target.nextSibling);
    }
    
    if (rut.length < 8) {
        feedback.innerText = '';
        return;
    }
    
    clearTimeout(rutTimeout);
    rutTimeout = setTimeout(() => {
      feedback.style.color = '#605e5c';
      feedback.innerText = 'Buscando en tabla de Funcionarios...';
      
      fetch(`/api/funcionarios/search/?q=${encodeURIComponent(rut)}`)
        .then(res => res.json())
        .then(data => {
          const results = data.results || [];
          // Buscar coincidencia exacta por RUT
          const func = results.find(f => f.id.replace(/[^0-9Kk]/g, '').toUpperCase() === rut.replace(/[^0-9Kk]/g, '').toUpperCase());
          
          if (func) {
            document.getElementById('form-nombres').value = func.nombres || '';
            document.getElementById('form-apellidos').value = func.apellidos || '';
            if (func.correo) document.getElementById('form-email').value = func.correo;
            if (func.unidad) {
               const unidadSelect = document.getElementById('form-unidad');
               for(let i=0; i<unidadSelect.options.length; i++) {
                 if(unidadSelect.options[i].text.toUpperCase() === func.unidad.toUpperCase()) {
                   unidadSelect.selectedIndex = i;
                   break;
                 }
               }
            }
            feedback.style.color = '#107c10'; // Green
            feedback.innerHTML = '<i class="fas fa-check-circle"></i> Funcionario encontrado. Datos cargados.';
          } else {
            feedback.innerHTML = `
              <div style="color: #a4262c; margin-bottom: 5px;"><i class="fas fa-exclamation-circle"></i> Funcionario no encontrado.</div>
              <button type="button" class="ms-btn-primary" onclick="abrirModalFuncionario('${rut}')" style="font-size: 11px; padding: 2px 8px; height: 24px;"><i class="fas fa-plus"></i> Añadir Funcionario</button>
            `;
          }
        })
        .catch(() => {
            feedback.innerText = '';
        });
    }, 600);
  });
  
  // Submit new funcionario
  const formFunc = document.getElementById('form-crear-usuario');
  if (formFunc) {
      formFunc.addEventListener('submit', function(e) {
          e.preventDefault();
          const btn = document.getElementById('btn-submit-usuario-rapido');
          btn.disabled = true;
          btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
          
          const formData = new FormData(this);
          const payload = {
              rut: formData.get('rut_nuevo'),
              nombres: formData.get('nombres_nuevo'),
              apellidos: formData.get('apellidos_nuevo'),
              correo: formData.get('correo_nuevo'),
              cargo: formData.get('cargo_nuevo'),
              unidad: formData.get('unidad_nuevo')
          };
          
          fetch('/api/funcionarios/crear/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify(payload)
          })
          .then(res => res.json())
          .then(data => {
              btn.disabled = false;
              btn.innerHTML = '<i class="fas fa-save"></i> Guardar Funcionario';
              if(data.success) {
                  $('#modalCrearUsuario').modal('hide');
                  // Auto-fill form with new data
                  document.getElementById('form-rut').value = payload.rut;
                  document.getElementById('form-nombres').value = payload.nombres;
                  document.getElementById('form-apellidos').value = payload.apellidos;
                  document.getElementById('form-email').value = payload.correo;
                  const unidadSelect = document.getElementById('form-unidad');
                  if (payload.unidad) {
                      for(let i=0; i<unidadSelect.options.length; i++) {
                         if(unidadSelect.options[i].text === payload.unidad) {
                             unidadSelect.selectedIndex = i;
                             break;
                         }
                      }
                  }
                  const fb = document.getElementById('rut-feedback');
                  fb.style.color = '#107c10';
                  fb.innerHTML = '<i class="fas fa-check-circle"></i> Funcionario creado. Datos cargados.';
                  showToast('Funcionario creado exitosamente.');
              } else {
                  alert(data.error || 'Error al crear funcionario');
              }
          })
          .catch(err => {
              btn.disabled = false;
              btn.innerHTML = '<i class="fas fa-save"></i> Guardar Funcionario';
              alert('Error de conexión');
          });
      });
  }
});

function abrirModalFuncionario(rut) {
    document.getElementById('form-crear-usuario').reset();
    document.getElementById('rut_nuevo').value = rut;
    $('#modalCrearUsuario').modal('show');
}

// ==========================================
// 1. Fetch & Render Identities
// ==========================================
function loadIdentities(searchValue = '') {
  const container = document.getElementById('identities-list');
  container.innerHTML = '<div style="padding: 40px; text-align: center; color: #605e5c;">Cargando identidades...</div>';

  const formData = new FormData();
  formData.append('draw', 1);
  formData.append('start', 0);
  formData.append('length', 100); // Muestra hasta 100 usuarios en la lista
  formData.append('search[value]', searchValue);
  
  // Need CSRF token for POST
  const csrfToken = getCookie('csrftoken');

  fetch('/api/usuarios/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.data && data.data.length > 0) {
      renderList(data.data);
    } else {
      container.innerHTML = '<div style="padding: 40px; text-align: center; color: #605e5c;">No se encontraron identidades.</div>';
    }
  })
  .catch(err => {
    console.error(err);
    container.innerHTML = '<div style="padding: 40px; text-align: center; color: #a4262c;">Ocurrió un error al cargar el directorio.</div>';
  });
}

function renderList(users) {
  const container = document.getElementById('identities-list');
  let html = '';

  const colors = ['#0078d4', '#d13438', '#107c10', '#881798', '#038387', '#498205'];

  users.forEach((u, i) => {
    // Generate avatar initials
    const initial1 = u.nombres ? u.nombres.charAt(0).toUpperCase() : '';
    const initial2 = u.apellidos ? u.apellidos.charAt(0).toUpperCase() : '';
    const initials = (initial1 + initial2) || u.rut.charAt(0) || '?';
    const color = colors[i % colors.length];

    // Status Badge (Fluent UI Dot)
    let statusBadge = '';
    if (u.is_active === "Sí" || u.is_active === true || u.is_active === "Activo") {
      statusBadge = '<div class="ms-status"><span class="ms-status-dot dot-active"></span>Activo</div>';
    } else {
      statusBadge = '<div class="ms-status"><span class="ms-status-dot dot-inactive"></span>Inactivo</div>';
    }
    
    // Role Badge (Fluent UI Clean Text)
    const roleText = u.rol || 'Sin Perfil';
    
    // Asignar colores corporativos según el rol usando puntos de color sutiles en lugar de píldoras gigantes
    let roleDotStyle = '#605e5c'; // Gris por defecto
    if (roleText.includes('Administrador')) {
      roleDotStyle = '#5c2d91'; // Morado
    } else if (roleText.includes('Mesa de Ayuda') || roleText.includes('Operador')) {
      roleDotStyle = '#0078d4'; // Azul
    } else if (roleText.includes('Técnico') || roleText.includes('Terreno')) {
      roleDotStyle = '#107c10'; // Verde
    } else if (roleText !== 'Sin Perfil') {
      roleDotStyle = '#a4262c'; // Rojo oscuro para otros
    }
    const roleIcon = u.rol_icono || 'fas fa-user-circle';
    const roleBadge = `<div class="ms-role-text" title="${roleText}" style="cursor: help;"><i class="${roleIcon}" style="font-size: 20px; color: ${roleDotStyle}"></i></div>`;
    
    const unidad = u.unidad || 'Sin Asignar';
    
    // Convert object to string to pass to edit function
    const userJson = encodeURIComponent(JSON.stringify(u));

    html += `
      <div class="ms-list-row" onclick="openViewModal('${userJson}')">
        <div class="ms-identity">
          <div class="ms-avatar" style="background-color: ${color}">${initials}</div>
          <div class="ms-user-info">
            <span class="ms-user-name">${u.nombres || ''} ${u.apellidos || ''}</span>
            <span class="ms-user-email" style="color: #605e5c;">${u.rut}</span>
          </div>
        </div>
        <div style="font-size: 13px; color: #323130; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${u.email || ''}">${u.email || 'Sin correo'}</div>
        <div style="font-size: 13px; color: #323130;">${unidad}</div>
        <div>${roleBadge}</div>
        <div>${statusBadge}</div>
        <div class="ms-row-actions">
          <button class="ms-icon-btn" onclick="event.stopPropagation(); openDrawer('editar', '${userJson}')" title="Modificar Identidad">
            <i class="fas fa-edit"></i>
          </button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// ==========================================
// 2. Offcanvas Drawer Logic
// ==========================================
let currentAction = 'crear';

function openDrawer(action, userJsonStr = null) {
  currentAction = action;
  const overlay = document.getElementById('drawer-overlay');
  const drawer = document.getElementById('identity-drawer');
  const title = document.getElementById('drawer-title');
  const form = document.getElementById('identity-form');
  
  form.reset();

  if (action === 'crear') {
    title.innerText = 'Nueva Identidad';
    document.getElementById('form-id').value = '';
    document.getElementById('lbl-password').innerText = 'Contraseña *';
    document.getElementById('form-password').required = true;
    const feedback = document.getElementById('rut-feedback');
    if (feedback) feedback.innerText = '';
  } else {
    title.innerText = 'Modificar Identidad';
    document.getElementById('lbl-password').innerText = 'Nueva Contraseña (Opcional)';
    document.getElementById('form-password').required = false;
    
    if (userJsonStr) {
      const u = JSON.parse(decodeURIComponent(userJsonStr));
      document.getElementById('form-id').value = u.id || u.rut; // fallback to rut
      document.getElementById('form-rut').value = u.rut || '';
      document.getElementById('form-nombres').value = u.nombres || '';
      document.getElementById('form-apellidos').value = u.apellidos || '';
      document.getElementById('form-email').value = u.email || '';
      
      // Select dropdowns
      if(u.unidad) document.getElementById('form-unidad').value = u.unidad;
      
      // Role needs ID or matching text, simplified mapping needed in backend but trying exact match
      const rolSelect = document.getElementById('form-rol');
      for(let i=0; i<rolSelect.options.length; i++) {
        if(rolSelect.options[i].text === u.rol || rolSelect.options[i].value == u.rol_id) {
          rolSelect.selectedIndex = i;
          break;
        }
      }
      
      const gruposSelect = document.getElementById('form-grupos');
      for (let i = 0; i < gruposSelect.options.length; i++) {
        gruposSelect.options[i].selected = false;
      }
      if (u.grupos && Array.isArray(u.grupos)) {
        const userGrupoIds = u.grupos.map(g => g.id.toString());
        for (let i = 0; i < gruposSelect.options.length; i++) {
          if (userGrupoIds.includes(gruposSelect.options[i].value)) {
            gruposSelect.options[i].selected = true;
          }
        }
      }
      
      document.getElementById('form-activo').checked = (u.is_active === "Sí" || u.is_active === true || u.is_active === "Activo");
    }
  }

  overlay.classList.add('active');
  drawer.classList.add('open');
}

function closeDrawer() {
  document.getElementById('drawer-overlay').classList.remove('active');
  document.getElementById('identity-drawer').classList.remove('open');
}

// ==========================================
// 3. Save Identity (API call)
// ==========================================
function saveIdentity() {
  const form = document.getElementById('identity-form');
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  
  const id = document.getElementById('form-id').value;
  
  const gruposSelect = document.getElementById('form-grupos');
  const selectedGrupos = Array.from(gruposSelect.selectedOptions).map(opt => parseInt(opt.value));
  
  const payload = {
    rut: document.getElementById('form-rut').value,
    nombres: document.getElementById('form-nombres').value,
    apellidos: document.getElementById('form-apellidos').value,
    email: document.getElementById('form-email').value,
    unidad: document.getElementById('form-unidad').value,
    rol: document.getElementById('form-rol').value,
    is_active: document.getElementById('form-activo').checked,
    grupos: selectedGrupos
  };
  
  const pass = document.getElementById('form-password').value;
  if (pass) payload.contrasena = pass;

  let url = '/api/usuarios/crear/';
  if (currentAction === 'editar') {
    url = '/api/usuarios/editar/';
    payload.id = id;
  }

  const csrfToken = getCookie('csrftoken');

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      closeDrawer();
      loadIdentities(document.getElementById('search-input').value);
      showToast(data.mensaje || 'Guardado correctamente');
    } else {
      showToast(data.error || 'Ocurrió un problema.', true);
    }
  })
  .catch(err => {
    showToast('Fallo de conexión.', true);
  });
}

// ==========================================
// 4. Custom Microsoft Toast
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
  }, 3500);
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

// ==========================================
// Modal de Visualización
// ==========================================
function openViewModal(userJsonStr) {
  const u = JSON.parse(decodeURIComponent(userJsonStr));
  
  const nombres = u.nombres || '';
  const apellidos = u.apellidos || '';
  const initial1 = nombres.charAt(0).toUpperCase();
  const initial2 = apellidos.charAt(0).toUpperCase();
  const initials = (initial1 + initial2) || u.rut.charAt(0) || '?';
  
  // Hash simple para dar color al avatar
  let hash = 0;
  const str = u.rut;
  for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
  const colors = ['#0078d4', '#d13438', '#107c10', '#881798', '#038387', '#498205'];
  const color = colors[Math.abs(hash) % colors.length];

  const avatar = document.getElementById('view-avatar');
  avatar.innerText = initials;
  avatar.style.backgroundColor = color;

  document.getElementById('view-nombre').innerText = `${nombres} ${apellidos}`.trim() || 'Sin Nombre';
  document.getElementById('view-rol-header').innerText = u.rol || 'Sin Perfil';
  document.getElementById('view-rut').innerText = u.rut || 'Sin RUT';
  document.getElementById('view-email').innerText = u.email || 'Sin Correo';
  document.getElementById('view-unidad').innerText = u.unidad || 'Sin Unidad';
  
  const divGrupos = document.getElementById('view-grupos');
  if (u.grupos && u.grupos.length > 0) {
    divGrupos.innerHTML = u.grupos.map(g => {
      const icon = g.icono || 'ms-Icon--Group';
      return `<span style="background: #edebe9; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 4px; display: inline-block; margin-bottom: 4px;"><i class="ms-Icon ${icon}" style="margin-right: 4px; color: #002a54;"></i>${g.nombre}</span>`;
    }).join('');
  } else {
    divGrupos.innerText = 'No asignado';
  }

  let estadoText = (u.is_active === "Sí" || u.is_active === true || u.is_active === "Activo") ? "Activo" : "Inactivo";
  document.getElementById('view-estado').innerText = estadoText;

  document.getElementById('view-modal-overlay').classList.add('active');
}

function closeViewModal() {
  document.getElementById('view-modal-overlay').classList.remove('active');
}
