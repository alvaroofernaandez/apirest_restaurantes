from django.contrib.auth.models import AbstractUser
from django.db import models

# Aquí añadimos los modelos, en este caso, añado el modelo Restaurante, con sus distintos atributos

class Restaurante(models.Model):
    name=models.CharField(max_length=100)
    web=models.URLField(max_length=100)
    yearFoundation=models.PositiveIntegerField()
