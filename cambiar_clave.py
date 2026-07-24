from django.contrib.auth.models import User
from core.models import PerfilUsuario

try:
    u = User.objects.get(username__iexact='17944996-k')
    u.username = '17944996-K'
    u.set_password('dEMO2026..')
    u.save()
    
    # Update PerfilUsuario too just in case
    p = PerfilUsuario.objects.filter(rut__iexact='17944996-k').first()
    if p:
        p.rut = '17944996-K'
        p.save()
        
    print("Contraseña y RUT actualizados con éxito")
except Exception as e:
    print(f"Error: {e}")
