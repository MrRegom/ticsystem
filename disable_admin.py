from django.contrib.auth.models import User
User.objects.filter(username='admin').update(is_active=False)
