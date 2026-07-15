from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='16233406-9'); u.set_password('admin'); u.save(); print('Password set to admin for', u.username)
