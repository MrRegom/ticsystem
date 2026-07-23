import re

def fix_actas(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Restore container-fluid
    html = html.replace('<div class="ms-wrap">', '<div class="container-fluid py-4 ms-wrap">')
    
    # 2. Fix the card-body issue where I wrongly used fluent-card-header for the form bodies
    # Wait, the string is exactly:
    # <div class="fluent-card mb-4">
    #    <div class="fluent-card-header">
    #        <div class="row">
    html = html.replace('<div class="fluent-card-header">\n                            <div class="row">', '<div class="card-body">\n                            <div class="row">')
    
    # Check if there are other fluent-card-header that should be card-body
    # Actually, the original was:
    # <div class="card mb-4" ...>
    #     <div class="card-body">
    # In redesign_actas.py I did:
    # html = html.replace('class="card mb-4"', 'class="fluent-card mb-4"')
    # html = html.replace('class="card-body"', 'class="fluent-card-header"')
    # I should revert fluent-card-header back to card-body if it wraps form fields!
    
    html = html.replace('<div class="fluent-card-header">\n                            <textarea', '<div class="card-body">\n                            <textarea')
    
    html = html.replace('btn fluent-btn-primary btn-sm rounded-pill px-3', 'fluent-btn-primary')
    
    # Fix the Generate button at the bottom
    # Original: <button type="button" class="btn btn-primary btn-lg btn-block mb-2" ...>
    # Replaced: <button type="button" class="fluent-btn-primary btn-lg btn-block mb-2" ...>
    # Let's make sure it's properly sized.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Actas fixed successfully.")

fix_actas(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
