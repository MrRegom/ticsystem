with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

if "'sla'," not in content and '"sla",' not in content:
    content = content.replace("'tickets',", "'tickets',\n    'sla',")
    with open('config/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
