from django.db import models
from productos.models import Producto
from pacientes.models import Paciente

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='VentaProducto')


class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
