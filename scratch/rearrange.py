import re

def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find Tickets Block
    tickets_start = html.find('<div class="fluent-card" style="height: 100%; display: flex; flex-direction: column;">\n        <div class="fluent-card-header">\n          <span>Últimos Tickets Pendientes</span>')
    tickets_end_search = html.find('</div>\n      </div>', tickets_start)
    if tickets_end_search != -1:
        tickets_end = html.find('</div>', tickets_end_search + 10) + 6 # Closes the fluent-card
    else:
        print("Tickets block not found.")
        return

    tickets_html = html[tickets_start:tickets_end]

    # Find Anexos Block
    anexos_start = html.find('<div class="fluent-card" style="height: 100%; display: flex; flex-direction: column;">\n        <div class="fluent-card-header">\n          <span>Últimos Anexos Registrados</span>')
    anexos_end_search = html.find('</div>\n      </div>', anexos_start)
    if anexos_end_search != -1:
        anexos_end = html.find('</div>', anexos_end_search + 10) + 6 # Closes the fluent-card
    else:
        print("Anexos block not found.")
        return

    anexos_html = html[anexos_start:anexos_end]

    # Find EXTRA TABLES wrapper
    extra_tables_start = html.find('<!-- EXTRA TABLES -->')
    extra_tables_end = html.find('</div>', extra_tables_start)
    if extra_tables_end != -1:
        extra_tables_end = html.find('</div>', html.find('</div>', html.find('</div>', extra_tables_end+1)+1)+1) # approximate, actually let's just use regex or extract the exact block.
        
    # Better approach: remove the EXTRA TABLES block entirely.
    # The block looks like:
    # <!-- EXTRA TABLES -->
    # <div style="margin-top: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; align-items: start;">
    #   [Anexos]
    #   [Tickets]
    # </div>
    # 
    # Let's find exactly this block.
    
    wrapper_start = html.find('<!-- EXTRA TABLES -->')
    wrapper_end = html.find('    </div>\n', anexos_end)
    if wrapper_start != -1 and wrapper_end != -1:
        wrapper_end += 11 # skip the </div>\n
        # Extract the whole wrapper and replace with empty string
        html = html[:wrapper_start] + html[wrapper_end:]

    # Now we need to re-insert Tickets and Anexos into the Left Column.
    # Left Column starts at:
    # <div class="dashboard-grid">
    #   <div>
    #     <div class="fluent-card" style="margin-bottom: 24px;">
    #       <div class="fluent-card-header">Vigilancia de Calidad de Inventario</div>
    
    left_col_start = html.find('<div class="fluent-card" style="margin-bottom: 24px;">\n          <div class="fluent-card-header">Vigilancia de Calidad de Inventario</div>')
    
    if left_col_start != -1:
        # Insert tickets above Vigilancia
        tickets_html_fixed = tickets_html.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="margin-bottom: 24px;"')
        html = html[:left_col_start] + tickets_html_fixed + '\n        ' + html[left_col_start:]
    else:
        print("Left column start not found.")
        return

    # Now find Actividad Reciente del Inventario
    # <div class="fluent-card" style="margin-top: 24px;">
    #   <div class="fluent-card-header">
    #     <span>Actividad Reciente del Inventario</span>
    
    act_rec_start = html.find('<div class="fluent-card" style="margin-top: 24px;">\n        <div class="fluent-card-header">\n          <span>Actividad Reciente del Inventario</span>')
    if act_rec_start == -1:
        print("Actividad Reciente not found")
        return
        
    # Find the end of Actividad Reciente
    act_rec_end_search = html.find('</div>\n        </div>\n      </div>', act_rec_start)
    act_rec_end = act_rec_end_search + 35 # closes fluent-card
    
    act_rec_html = html[act_rec_start:act_rec_end]
    
    # We want to replace Actividad Reciente with a grid containing Actividad Reciente and Anexos
    act_rec_html_fixed = act_rec_html.replace('style="margin-top: 24px;"', 'style="height: 100%; display: flex; flex-direction: column;"')
    anexos_html_fixed = anexos_html.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="height: 100%; display: flex; flex-direction: column;"')
    
    act_rec_html_fixed = act_rec_html_fixed.replace('<tr>\n                <td>\n                  <div style="display: flex; gap: 12px; align-items: center;">', '<tr style="font-size: 12px;">\n                <td>\n                  <div style="display: flex; gap: 8px; align-items: center;">')
    
    combined_grid = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 24px;">
          {act_rec_html_fixed.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="height: 100%;"')}
          {anexos_html_fixed.replace('style="height: 100%; display: flex; flex-direction: column;"', 'style="height: 100%;"')}
        </div>
    """
    
    html = html[:act_rec_start] + combined_grid + html[act_rec_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")

fix_layout(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
