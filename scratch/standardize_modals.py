import os
import re

html_files = []
for root, dirs, files in os.walk(r'c:\proyectos\ticsystem'):
    if 'templates' in root:
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    if 'class="modal-content' in html:
        # Standardize header
        html = re.sub(r'<div class="modal-header"[^>]*>', '<div class="modal-header bg-primary text-white">', html)
        html = re.sub(r'<div style="background:\s*#006FB3.*?</div>', '<div class="modal-header bg-primary text-white">', html)
        # Standardize title to uppercase
        html = re.sub(r'<h5 class="modal-title"[^>]*>', '<h5 class="modal-title text-uppercase">', html)
        html = re.sub(r'<h5 class="modal-title">', '<h5 class="modal-title text-uppercase">', html)
        # Standardize close button
        html = re.sub(r'<button type="button" class="close" data-dismiss="modal"[^>]*>&times;</button>', '<button type="button" class="close text-white" data-dismiss="modal">&times;</button>', html)
        # Remove rounded corners from modal-content
        html = re.sub(r'class="modal-content"[^>]*>', 'class="modal-content rounded-0 border-0">', html)
        
        if html != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print('Updated modals in:', filepath)
