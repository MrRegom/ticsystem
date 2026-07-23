import re

def fix_alignment_and_buttons(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove padding and card style from the main tab content container
    old_tab_content = r'<div class="tab-content fluent-card p-4 border-top-0" id="actasTabContent">'
    new_tab_content = '<div class="tab-content" id="actasTabContent">'
    html = re.sub(old_tab_content, new_tab_content, html)
    
    # 2. Add text-decoration: none to the buttons
    # Button 1
    old_btn1 = r'style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem;"'
    new_btn1 = 'style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; text-decoration: none !important;"'
    html = re.sub(old_btn1, new_btn1, html)
    
    # Button 2
    old_btn2 = r'style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; background: #fff; border: 1px solid #cbd5e1; color: #334155;"'
    new_btn2 = 'style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; background: #fff; border: 1px solid #cbd5e1; color: #334155; text-decoration: none !important;"'
    html = re.sub(old_btn2, new_btn2, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Alignment and button styles fixed.")

fix_alignment_and_buttons(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
