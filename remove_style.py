import io
import re

path = 'tickets/templates/tickets/tickets.html'
with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<style>.*?</style>', '{% load static %}\n<link rel="stylesheet" href="{% static \'css/tickets.css\' %}?v=1">', content, flags=re.DOTALL)

with io.open(path, 'w', encoding='utf-8') as f:
    f.write(content)
