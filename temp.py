from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='16233406-9'); u.is_active = True; u.save(); print('User active status:', u.is_active)
