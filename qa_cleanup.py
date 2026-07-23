import os
import django
import sys

# Append current directory to python path
sys.path.append('/var/www/ticsystem')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.contrib.auth.models import User
from core.models import PerfilUsuario
from tickets.models import Ticket, GrupoResolutor, Categoria

def run():
    print("Deleting Tickets...")
    Ticket.objects.all().delete()
    print("Tickets deleted.")

    print("Deleting Categorias...")
    Categoria.objects.all().delete()
    print("Categorias deleted.")

    print("Deleting Grupo Resolutor...")
    GrupoResolutor.objects.all().delete()
    print("Grupo Resolutor deleted.")

    print("Deleting Usuarios...")
    # Get the user to keep
    try:
        user_to_keep = User.objects.get(username='16233406-9')
        print(f"Keeping user: {user_to_keep.username}")
        users_to_delete = User.objects.exclude(id=user_to_keep.id).exclude(is_superuser=True)
    except User.DoesNotExist:
        try:
            # Maybe the username is without dash
            user_to_keep = User.objects.get(username='162334069')
            print(f"Keeping user: {user_to_keep.username}")
            users_to_delete = User.objects.exclude(id=user_to_keep.id).exclude(is_superuser=True)
        except User.DoesNotExist:
            print("Super admin user not found by username. Searching by perfil rut...")
            try:
                perfil_keep = PerfilUsuario.objects.get(rut='16233406-9')
                user_to_keep = perfil_keep.user
                print(f"Keeping user: {user_to_keep.username}")
                users_to_delete = User.objects.exclude(id=user_to_keep.id).exclude(is_superuser=True)
            except PerfilUsuario.DoesNotExist:
                print("Could not find user 16233406-9. Aborting to be safe.")
                return

    count = 0
    protected_count = 0
    for u in users_to_delete:
        try:
            u.delete()
            count += 1
        except Exception as e:
            print(f"Could not delete {u.username}: {e}")
            # Deactivate instead
            u.is_active = False
            u.save()
            protected_count += 1

    print(f"Deleted {count} users. Deactivated {protected_count} users that were protected.")
    print("QA Cleanup Complete.")

if __name__ == '__main__':
    run()
