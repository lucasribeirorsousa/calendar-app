from django.contrib import admin
from .models import Event

# Registre o modelo Event no painel de administração
admin.site.register(Event)
