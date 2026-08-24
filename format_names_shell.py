from core.models import Funcionario
from django.contrib.auth.models import User

f_count = 0
for f in Funcionario.objects.all():
    f.save(update_fields=['nombres', 'apellidos', 'rut'])
    f_count += 1
print(f"Actualizados {f_count} Funcionarios a mayúsculas.")

u_count = 0
for u in User.objects.all():
    u.save(update_fields=['first_name', 'last_name'])
    u_count += 1
print(f"Actualizados {u_count} Usuarios a mayúsculas.")
