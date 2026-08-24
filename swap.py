import re

with open(r'c:\proyectos\ticsystem\mantenedores\templates\mantenedores\mantenedores.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find SECCIÓN 1
sec1_start = content.find('<!-- SECCIÓN 1: UBICACIÓN Y RELACIONES (Jerarquía Padre) -->')
sec2_start = content.find('<!-- SECCIÓN 2: DATOS DEL REGISTRO (Hijo) -->')

# The end of SECCIÓN 2 is before the closing </div> of modal-body.
# Let's find the closing </div> of modal-body. 
# It's right before `<div class="modal-footer"`
footer_start = content.find('<div class="modal-footer"')
# The </div> of modal-body is right before footer_start
modal_body_end = content.rfind('</div>', sec2_start, footer_start)

sec1 = content[sec1_start:sec2_start]
sec2 = content[sec2_start:modal_body_end]

# In sec1, we need to remove mb-3 from section-relaciones and add mb-3 to sec2?
# sec1 currently has "mb-3 p-3 bg-white shadow-sm"
# sec2 currently has "p-3 bg-white shadow-sm"
# Let's adjust classes.
sec1_new = sec1.replace('class="mb-3 p-3 bg-white shadow-sm"', 'class="p-3 bg-white shadow-sm mt-3"')
sec2_new = sec2.replace('class="p-3 bg-white shadow-sm"', 'class="p-3 bg-white shadow-sm mb-3"', 1)

new_content = content[:sec1_start] + sec2_new + sec1_new + content[modal_body_end:]

with open(r'c:\proyectos\ticsystem\mantenedores\templates\mantenedores\mantenedores.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Swapped successfully")
