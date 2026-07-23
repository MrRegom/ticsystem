import re

def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find Tickets Block (currently above Vigilancia, with margin-bottom 24px)
    tickets_match = re.search(r'<div class="fluent-card" style="margin-bottom: 24px;">\s*<div class="fluent-card-header">\s*<span>Últimos Tickets Pendientes</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
    if tickets_match:
        tickets_html = tickets_match.group(0)
        html = html.replace(tickets_html, '')
    else:
        print("Tickets block not found.")
        return

    # Find the combined grid containing Actividad Reciente and Anexos
    # We'll just find the grid wrapper and the two cards inside it.
    grid_match = re.search(r'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">\s*<div class="fluent-card" style="height: 100%;">\s*<div class="fluent-card-header">\s*<span>Actividad Reciente del Inventario</span>.*?</table>\s*</div>\s*</div>\s*<div class="fluent-card" style="height: 100%;">\s*<div class="fluent-card-header">\s*<span>Últimos Anexos Registrados</span>.*?</table>\s*</div>\s*</div>\s*</div>', html, re.DOTALL)
    
    if grid_match:
        grid_html = grid_match.group(0)
        
        # Extract Actividad Reciente
        act_match = re.search(r'<div class="fluent-card" style="height: 100%;">\s*<div class="fluent-card-header">\s*<span>Actividad Reciente del Inventario</span>.*?</table>\s*</div>\s*</div>', grid_html, re.DOTALL)
        act_html = act_match.group(0).replace('style="height: 100%;"', 'style="margin-top: 24px;"')
        
        # Extract Anexos
        anexos_match = re.search(r'<div class="fluent-card" style="height: 100%;">\s*<div class="fluent-card-header">\s*<span>Últimos Anexos Registrados</span>.*?</table>\s*</div>\s*</div>', grid_html, re.DOTALL)
        anexos_html = anexos_match.group(0)
        
        # We want Actividad Reciente to just be where the grid was.
        html = html.replace(grid_html, act_html)
        
    else:
        print("Combined Grid not found.")
        # let's try to find them separately if the grid didn't match perfectly
        act_match = re.search(r'<div class="fluent-card"[^>]*>\s*<div class="fluent-card-header">\s*<span>Actividad Reciente del Inventario</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
        anexos_match = re.search(r'<div class="fluent-card"[^>]*>\s*<div class="fluent-card-header">\s*<span>Últimos Anexos Registrados</span>.*?</table>\s*</div>\s*</div>', html, re.DOTALL)
        
        if act_match and anexos_match:
             act_html = act_match.group(0)
             anexos_html = anexos_match.group(0)
             
             # find the grid wrapper and remove it
             grid_wrapper_match = re.search(r'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">\s*' + re.escape(act_html) + r'\s*' + re.escape(anexos_html) + r'\s*</div>', html, re.DOTALL)
             if grid_wrapper_match:
                 html = html.replace(grid_wrapper_match.group(0), act_html.replace('height: 100%;', 'margin-top: 24px;'))
             else:
                 print("Could not find grid wrapper exactly")
                 return
        else:
             print("Could not find Actividad or Anexos")
             return

    # Now create the new top grid for Anexos and Tickets
    tickets_html_fixed = tickets_html.replace('style="margin-bottom: 24px;"', 'style="height: 100%;"')
    anexos_html_fixed = anexos_html.replace('style="margin-top: 24px;"', 'style="height: 100%;"') # just in case
    
    top_grid = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
          {anexos_html_fixed}
          {tickets_html_fixed}
        </div>
    """
    
    vigilancia_match = re.search(r'<div class="fluent-card" style="margin-bottom: 24px;">\s*<div class="fluent-card-header">Vigilancia de Calidad de Inventario</div>', html)
    if vigilancia_match:
        html = html[:vigilancia_match.start()] + top_grid + html[vigilancia_match.start():]
    else:
        print("Vigilancia not found")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")

fix_layout(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
