from django.db import models
from productos.models import Producto

class Compra(models.Model):

    ESTADO_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('entregado', 'Entregado'),
    ]

    fecha = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='solicitado',
    )
    productos = models.ManyToManyField(Producto, through='CompraProducto')


class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
