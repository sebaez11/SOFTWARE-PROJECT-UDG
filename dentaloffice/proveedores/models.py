from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre
