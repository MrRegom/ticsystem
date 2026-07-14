import io
import re

path = 'core/templates/core/base.html'
with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

script_match = re.search(r'<script>\s*// Configuración global de CSRF.*?</script>', content, flags=re.DOTALL)
if script_match:
    js_code = script_match.group(0).replace('<script>', '').replace('</script>', '').strip()
    js_code = js_code.replace("{% url 'logout' %}", "window.BASE_CONFIG.logoutUrl")
    
    with io.open('static/js/base.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    new_script = '''<script>
    window.BASE_CONFIG = {
        logoutUrl: "{% url 'logout' %}"
    };
</script>
<script src="/static/js/base.js?v=1"></script>'''

    content = content.replace(script_match.group(0), new_script)
    
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
