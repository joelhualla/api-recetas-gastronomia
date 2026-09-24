from django.db import models
from django.contrib.auth.models import User

# Catálogo maestro de ingredientes
class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=50)
    unidad_medida_base = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

# Entidad principal de recetas
class Receta(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En Revisión'),
        ('publicada', 'Publicada'),
        ('archivada', 'Archivada'),
    ]
    DIFICULTADES = [
        ('facil', 'Fácil'),
        ('media', 'Media'),
        ('dificil', 'Difícil'),
    ]

    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    tiempo_preparacion = models.PositiveIntegerField(help_text="Tiempo en minutos")
    porciones = models.PositiveIntegerField(default=1)
    dificultad = models.CharField(max_length=10, choices=DIFICULTADES, default='facil')
    visibilidad = models.CharField(
        max_length=10, 
        choices=[('publica', 'Pública'), ('privada', 'Privada')], 
        default='publica'
    )
    estado = models.CharField(max_length=15, choices=ESTADOS, default='borrador')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"

# Relación N:M entre Recetas e Ingredientes
class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes_detalle')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)

    class Meta:
        unique_together = ('receta', 'ingrediente')

    def __str__(self):
        return f"{self.cantidad} {self.unidad_medida} de {self.ingrediente.nombre}"

# Pasos secuenciales de la receta
class PasoPreparacion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='pasos')
    orden_paso = models.PositiveIntegerField()
    instruccion = models.TextField()
    tiempo_estimado = models.PositiveIntegerField(blank=True, null=True, help_text="Tiempo en minutos")

    class Meta:
        ordering = ['orden_paso']

    def __str__(self):
        return f"Paso {self.orden_paso} - {self.receta.titulo}"

# Auditoría de transiciones de estado
class AuditoriaEstado(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='auditorias')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    motivo = models.TextField(blank=True, null=True)
    fecha_evento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receta.titulo}: {self.estado_anterior} -> {self.estado_nuevo}"

# Create your models here.
