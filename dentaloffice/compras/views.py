from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import CompraForm, EditCompraStatusForm
from .models import CompraProducto, Compra
from productos.models import Producto, Iva
from django.db.models import Sum, F
from datetime import datetime
import json


def cambiar_estado_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)

    nuevo_estado = request.GET.get('estado')
    if nuevo_estado == 'entregado' and compra.status != 'entregado':
        compra.status = 'entregado'
        compra.save()

        for compra_producto in compra.compraproducto_set.all():
            producto = compra_producto.producto
            producto.stock += compra_producto.cantidad
            producto.save()

    return redirect('lista_compras')


def lista_compras(request):

    filtro_compra_id = request.GET.get('filtro_compra')
    ultimo_iva = Iva.objects.latest('fecha').porcentaje

    if filtro_compra_id:
        compras = Compra.objects.filter(id=filtro_compra_id).annotate(
            subtotal_compra=Sum(F('compraproducto__cantidad') * F('compraproducto__precio')),
            total_compra=F('subtotal_compra') + F('subtotal_compra') * ultimo_iva / 100
        )
    
    else:
        compras = Compra.objects.annotate(
            subtotal_compra=Sum(F('compraproducto__cantidad') * F('compraproducto__precio')),
            total_compra=F('subtotal_compra') + F('subtotal_compra') * ultimo_iva / 100
        ).all()

    return render(request, 'lista_compras.html', {'compras': compras})


def registrar_compra(request):
    productos = Producto.objects.all()

    ultima_compra_id = Compra.objects.latest('id').id if Compra.objects.exists() else 0
    folio_compra = ultima_compra_id + 1

    fecha_compra = datetime.now().strftime("%d-%m-%Y")

    ultimo_iva = Iva.objects.latest('fecha')

    metadata = {"folio_compra": folio_compra, "fecha_compra": fecha_compra, "ultimo_iva": ultimo_iva.porcentaje}

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)  # No guardes la compra aún, ya que necesitas agregar los productos primero
            compra.save()  # Guarda la compra para obtener su ID

            selected_productos_str = request.POST.get('selected_productos')
            selected_productos = json.loads(selected_productos_str)

            for producto in selected_productos:
                producto_id = producto['id']
                cantidad = producto['cantidad']
                precio = producto['precio']
                compra_producto = CompraProducto(compra=compra, producto_id=producto_id, cantidad=cantidad, precio=precio)
                compra_producto.save()

        return redirect('lista_compras')

    else:
        form = CompraForm()
    
    return render(request, 'registrar_compra.html', {'form': form, 'productos': productos, "metadata": metadata})
