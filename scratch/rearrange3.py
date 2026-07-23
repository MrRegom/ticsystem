import re

def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Find Tickets Block
    tickets_match = re.search(r'<div class="fluent-card" style="height: 100%; display: flex; flex-direction: column;">\s*<div class="fluent-card-header">\s*<span>Últimos Tickets Pendientes</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
    if not tickets_match:
        print("Tickets block not found.")
        return
    tickets_html = tickets_match.group(0)

    # 2. Find Anexos Block
    anexos_match = re.search(r'<div class="fluent-card" style="height: 100%; display: flex; flex-direction: column;">\s*<div class="fluent-card-header">\s*<span>Últimos Anexos Registrados</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
    if not anexos_match:
        print("Anexos block not found.")
        return
    anexos_html = anexos_match.group(0)

    # 3. Find and remove EXTRA TABLES wrapper
    extra_match = re.search(r'<!-- EXTRA TABLES -->\s*<div[^>]*>.*?</div>\s*</div>', html, re.DOTALL)
    if extra_match:
        if 'Últimos Tickets Pendientes' in extra_match.group(0):
            html = html.replace(extra_match.group(0), '')
    else:
        start_idx = html.find('<!-- EXTRA TABLES -->')
        if start_idx != -1:
            end_idx = html.find('<!-- RIGHT COLUMN -->', start_idx)
            html = html[:start_idx] + html[end_idx:]

    # 4. Insert Tickets above Vigilancia
    vigilancia_match = re.search(r'<div class="fluent-card" style="margin-bottom: 24px;">\s*<div class="fluent-card-header">Vigilancia de Calidad de Inventario</div>', html)
    if vigilancia_match:
        tickets_fixed = tickets_html.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="margin-bottom: 24px;"')
        html = html[:vigilancia_match.start()] + tickets_fixed + '\n        ' + html[vigilancia_match.start():]
    else:
        print("Vigilancia not found")
        return

    # 5. Replace Actividad Reciente with Grid (Actividad + Anexos)
    act_match = re.search(r'<div class="fluent-card">\s*<div class="fluent-card-header">\s*<span>Actividad Reciente del Inventario</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
    if act_match:
        act_html = act_match.group(0)
        # make it full height
        act_html = act_html.replace('<div class="fluent-card">', '<div class="fluent-card" style="height: 100%;">')
        anexos_html_fixed = anexos_html.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="height: 100%;"')
        
        combined_grid = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
          {act_html}
          {anexos_html_fixed}
        </div>
        """
        html = html.replace(act_match.group(0), combined_grid)
    else:
        print("Actividad Reciente not found")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")

fix_layout(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
