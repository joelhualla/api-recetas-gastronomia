from django.contrib import admin
from .models import Ingrediente, Receta, RecetaIngrediente, PasoPreparacion, AuditoriaEstado

# Registramos los modelos para verlos en la interfaz web de Django
admin.site.register(Ingrediente)
admin.site.register(Receta)
admin.site.register(RecetaIngrediente)
admin.site.register(PasoPreparacion)
admin.site.register(AuditoriaEstado)
