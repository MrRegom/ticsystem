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
});

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

    // Status Badge
    let statusBadge = '';
    if (u.is_active === "Sí" || u.is_active === true || u.is_active === "Activo") {
      statusBadge = '<span class="ms-badge badge-active">Activo</span>';
    } else {
      statusBadge = '<span class="ms-badge badge-inactive">Inactivo</span>';
    }
    
    // Role Badge
    const roleText = u.rol || 'Sin Perfil';
    
    // Asignar colores corporativos según el rol para identificarlos visualmente
    let roleColorStyle = 'background: #e1dfdd; color: #323130;'; // Gris por defecto
    if (roleText.includes('Administrador')) {
      roleColorStyle = 'background: #f4f0fc; color: #5c2d91; border: 1px solid #c9b1f0;'; // Morado
    } else if (roleText.includes('Mesa de Ayuda') || roleText.includes('Operador')) {
      roleColorStyle = 'background: #eff6fc; color: #0078d4; border: 1px solid #c7e0f4;'; // Azul
    } else if (roleText.includes('Técnico') || roleText.includes('Terreno')) {
      roleColorStyle = 'background: #dff6dd; color: #107c10; border: 1px solid #a3d9a1;'; // Verde
    } else if (roleText !== 'Sin Perfil') {
      roleColorStyle = 'background: #fdf3f4; color: #a4262c; border: 1px solid #f8c1c4;'; // Rojo oscuro para otros
    }

    const roleBadge = `<span class="ms-badge" style="${roleColorStyle}">${roleText}</span>`;
    
    const unidad = u.unidad || 'Sin Asignar';
    
    // Convert object to string to pass to edit function
    const userJson = encodeURIComponent(JSON.stringify(u));

    html += `
      <div class="ms-list-row">
        <div class="ms-identity">
          <div class="ms-avatar" style="background-color: ${color}">${initials}</div>
          <div class="ms-user-info">
            <span class="ms-user-name">${u.nombres || ''} ${u.apellidos || ''}</span>
            <span class="ms-user-email">${u.email || u.rut}</span>
          </div>
        </div>
        <div style="font-size: 13px; color: #323130;">${unidad}</div>
        <div>${roleBadge}</div>
        <div>${statusBadge}</div>
        <div class="ms-row-actions">
          <button class="ms-icon-btn" onclick="openDrawer('editar', '${userJson}')" title="Modificar Identidad">
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
  const payload = {
    rut: document.getElementById('form-rut').value,
    nombres: document.getElementById('form-nombres').value,
    apellidos: document.getElementById('form-apellidos').value,
    email: document.getElementById('form-email').value,
    unidad: document.getElementById('form-unidad').value,
    rol: document.getElementById('form-rol').value,
    is_active: document.getElementById('form-activo').checked,
    grupos: [] // Si implementamos grupos despues
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
      Swal.fire({ toast:true, position: 'top-end', icon: 'success', title: data.mensaje || 'Guardado correctamente', showConfirmButton: false, timer: 3000 });
    } else {
      Swal.fire('Error', data.error || 'Ocurrió un problema.', 'error');
    }
  })
  .catch(err => {
    Swal.fire('Error', 'Fallo de conexión.', 'error');
  });
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
