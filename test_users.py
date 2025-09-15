#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutra.settings')
django.setup()

from django.contrib.auth.models import User

# Verificar usuários existentes
users = User.objects.all()
print(f"Total de usuários: {users.count()}")

for user in users:
    print(f"Username: {user.username}, Email: {user.email}")


