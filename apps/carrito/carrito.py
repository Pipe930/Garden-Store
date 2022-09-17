from django.contrib import messages

class CarritoCompras:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad, request):
        descuento = producto.idOferta
        if (str(producto.id) not in self.carrito.keys()):
            self.carrito[producto.id] = {
                'producto_id': producto.id,
                'nombreProducto': producto.nombreProducto,
                'cantidad': 1,
                'precio': str(producto.precio),
                'imagen': producto.imagen.url
            }
            for key, value in self.carrito.items():
                if descuento is not None:
                    value['precio'] = self.productoDescuento(producto)
            messages.success(request, 'El producto se agrego con exito al carrito')

        else:
            for key, value in self.carrito.items():
                if key == str(producto.id) and value['cantidad'] < cantidad:
                    if descuento is not None:
                        precioTotal = self.productoDescuento(producto)
                        value['cantidad'] = value['cantidad'] + 1
                        value['precio'] = int(value['precio']) + precioTotal
                        break
                    value['cantidad'] = value['cantidad'] + 1
                    value['precio'] = int(value['precio']) + producto.precio
                    break
        self.guardar()
    
    def productoDescuento(self, producto):
        descuentoProducto = producto.idOferta.descuento
        precio = producto.precio

        descuentoDecimal = descuentoProducto / 100
        precioDescuento = float(precio) * descuentoDecimal
        precioTotal = int(precio) - int(precioDescuento)
        return precioTotal
    
    def guardar(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True
    
    def eliminar(self, producto):
        producto_id= str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()
    
    def restar(self, producto):
        for key, value in self.carrito.items():
            if key == str(producto.id):
                descuento = producto.idOferta
                if descuento is not None:
                    precioTotal = self.productoDescuento(producto)
                    value['cantidad'] = value['cantidad'] - 1
                    value['precio'] = int(value['precio']) - precioTotal
                    if value['cantidad'] < 1:
                        self.eliminar(producto)
                    break
                value['cantidad'] = value['cantidad'] - 1
                value['precio'] = int(value['precio']) - producto.precio
                if value['cantidad'] < 1:
                    self.eliminar(producto)
                break
        self.guardar()
    
    def limpiar(self):
        carrito = self.session['carrito'] = {}
        self.session.modified = True