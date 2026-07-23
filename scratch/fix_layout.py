import re

def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Find the two cards
    anexos_start = html.find('<div class="fluent-card" style="margin-top: 24px;">\n        <div class="fluent-card-header">\n          <span>Últimos Anexos Registrados</span>')
    tickets_end = html.find('    </div> <!-- END LEFT COLUMN -->')
    
    if anexos_start == -1 or tickets_end == -1:
        print("Could not find the cards")
        return
        
    cards_html = html[anexos_start:tickets_end]
    
    # Remove the cards from the left column
    new_html = html[:anexos_start] + html[tickets_end:]
    
    # Replace margin-top with flex/grid sizing 
    cards_html = cards_html.replace('style="margin-top: 24px;"', 'style="height: 100%; display: flex; flex-direction: column;"')
    
    responsive_container = f"""
    <div style="margin-top: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; align-items: start;">
      {cards_html.strip()}
    </div>
"""
    
    # 2. Find the end of the right column / dashboard-grid
    # The right column ends with:
    #       </div>
    #     </div>
    # 
    #     {% if user|has_permiso:'VER_RESUMEN_GLOBAL' %}
    # We will insert it right before the {% if user|has_permiso:'VER_RESUMEN_GLOBAL' %}
    
    insert_pos = new_html.find('    {% if user|has_permiso:\'VER_RESUMEN_GLOBAL\' %}')
    if insert_pos == -1:
        print("Could not find insert pos")
        return
        
    final_html = new_html[:insert_pos] + responsive_container + new_html[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Success")

fix_layout(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
