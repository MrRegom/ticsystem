import io
import re

path = 'tickets/templates/tickets/tickets.html'
with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

script_match = re.search(r'<script>(.*?)</script>', content, flags=re.DOTALL)
if script_match:
    js_code = script_match.group(1).strip()
    
    # We need to remove the Django variables from js_code or handle them.
    # The first few lines are:
    # document.addEventListener('DOMContentLoaded', function() {
    #     var CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]') ? ...
    #     var kanbanData = {{ kanban_data|safe }};
    
    js_code = js_code.replace("{{ csrf_token }}", "window.TICKET_CONFIG.csrfToken")
    js_code = js_code.replace("{{ kanban_data|safe }}", "window.TICKET_CONFIG.kanbanData")
    
    with io.open('static/js/tickets-kanban.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    new_script = '''<script>
    window.TICKET_CONFIG = {
        csrfToken: '{{ csrf_token }}',
        kanbanData: {{ kanban_data|safe }}
    };
</script>
<script src="{% static 'js/tickets-kanban.js' %}?v=1"></script>'''

    content = content.replace(script_match.group(0), new_script)
    
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
