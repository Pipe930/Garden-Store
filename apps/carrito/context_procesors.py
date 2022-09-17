
def importar_total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        for key, value in request.session['carrito'].items():
            total = total + (int(value['precio']))
    return {'importar_total_carrito': total}