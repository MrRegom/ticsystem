import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticsystem.settings')
django.setup()

from core.models import Funcionario
from django.contrib.auth.models import User

# Update Funcionarios
f_count = 0
for f in Funcionario.objects.all():
    f.save(update_fields=['nombres', 'apellidos', 'rut'])  # Will trigger uppercase
    f_count += 1
print(f"Actualizados {f_count} Funcionarios a mayúsculas.")

# Update Users
u_count = 0
for u in User.objects.all():
    u.save(update_fields=['first_name', 'last_name']) # Will trigger pre_save signal
    u_count += 1
print(f"Actualizados {u_count} Usuarios a mayúsculas.")
