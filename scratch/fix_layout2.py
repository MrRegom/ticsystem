def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    lines = html.split('\n')
    
    # 1. Find the two cards
    anexos_start = -1
    tickets_end = -1
    for i, line in enumerate(lines):
        if '<span>Últimos Anexos Registrados</span>' in line:
            anexos_start = i - 2 # Backtrack to the <div class="fluent-card">
        if '<!-- END LEFT COLUMN -->' in line:
            tickets_end = i - 1 # Stop before the </div> for the left column
            break
            
    if anexos_start == -1 or tickets_end == -1:
        print("Could not find cards")
        return
        
    print(f"Cards found from {anexos_start} to {tickets_end}")
    cards_lines = lines[anexos_start:tickets_end]
    
    # Remove from lines
    del lines[anexos_start:tickets_end]
    
    # 2. Find the end of the dashboard grid
    # We'll just look for the end of the "Mapa de Calor" block
    grid_end = -1
    for i in range(len(lines)):
        if 'Mapa de Calor por Unidades' in lines[i]:
            for j in range(i, len(lines)):
                if '{% endfor %}' in lines[j]:
                    # This is the end of the loop, now we just need the 2 </div>
                    grid_end = j + 3
                    break
            break
            
    if grid_end == -1:
        print("Could not find grid end")
        return
        
    print(f"Grid ends at {grid_end}")
    
    cards_html = '\n'.join(cards_lines)
    cards_html = cards_html.replace('style="margin-top: 24px;"', 'style="height: 100%; display: flex; flex-direction: column;"')
    
    responsive_container = f"""
    <!-- EXTRA TABLES -->
    <div style="margin-top: 24px; display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 24px; align-items: start;">
{cards_html}
    </div>
"""
    
    lines.insert(grid_end, responsive_container)
    
    # Also, we have an underflow at line 651: `</div>` before `{% endblock %}`
    # Let's fix that too. We remove the extra `</div>` right before `{% endblock content %}`
    for i in range(len(lines)-1, -1, -1):
        if '{% endblock content %}' in lines[i]:
            # Look at previous line
            if '</div>' in lines[i-1]:
                print(f"Removing extra </div> at {i-1}")
                del lines[i-1]
            break

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Success")

fix_layout(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
