from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import VentaProducto, Venta
from pacientes.models import Paciente
from .forms import VentaForm
from productos.models import Producto, Iva
from datetime import datetime
import json
from django.db.models import Sum, F

def lista_ventas(request):

    filtro_venta_id = request.GET.get('filtro_venta')

    # Obtén el último valor de IVA
    ultimo_iva = Iva.objects.latest('fecha').porcentaje

    if filtro_venta_id:
        # Si se proporciona un ID de venta, filtra las ventas solo por ese ID
        ventas = Venta.objects.filter(id=filtro_venta_id).annotate(
            subtotal_venta=Sum(F('ventaproducto__cantidad') * F('ventaproducto__precio')),
            total_venta=F('subtotal_venta') + F('subtotal_venta') * ultimo_iva / 100
        )
    
    else:
        # Calcula el subtotal y el total para cada venta
        ventas = Venta.objects.annotate(
            subtotal_venta=Sum(F('ventaproducto__cantidad') * F('ventaproducto__precio')),
            total_venta=F('subtotal_venta') + F('subtotal_venta') * ultimo_iva / 100
        ).all()

    return render(request, 'lista_ventas.html', {'ventas': ventas, 'ultimo_iva': ultimo_iva})


def registrar_venta(request):
    pacientes = Paciente.objects.all()
    productos = Producto.objects.all()

    ultima_venta_id = Venta.objects.latest('id').id if Venta.objects.exists() else 0
    folio_venta = ultima_venta_id + 1

    fecha_venta = datetime.now().strftime("%d-%m-%Y")

    ultimo_iva = Iva.objects.latest('fecha')


    metadata = {"folio_venta": folio_venta, "fecha_venta": fecha_venta, "ultimo_iva": ultimo_iva.porcentaje}

    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            paciente_nombre = form.cleaned_data['paciente_nombre']
            paciente = get_object_or_404(Paciente, nombre=paciente_nombre)
            venta.paciente = paciente
            venta.save()

            selected_productos_str = request.POST.get('selected_productos')
            selected_productos = json.loads(selected_productos_str)


            for producto in selected_productos:
                producto_id = producto['id']
                cantidad = producto['cantidad']
                precio = producto['precio']
                venta_producto = VentaProducto(venta=venta, producto_id=producto_id, cantidad=cantidad, precio=precio)
                venta_producto.save()

                # Restar la cantidad comprada del stock del producto
                producto_actual = Producto.objects.get(id=producto_id)
                producto_actual.stock -= cantidad
                producto_actual.save()
            
        else:
            print("ERRORES DEL FORM: \n")
            print(form.errors)

        return redirect('lista_ventas')

    else:
        form = VentaForm()
    
    return render(request, 'registrar_venta.html', {'form': form, 'productos': productos, 'pacientes': pacientes, "metadata": metadata, 'errores': form.errors})
