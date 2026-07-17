from mantenedores.models import EstadoEquipo

baja = EstadoEquipo.objects.filter(nombre__icontains='baja').first()
if baja:
    baja.color_hex = '#a4262c'
    baja.save()
    print('Baja updated to #a4262c')

soporte = EstadoEquipo.objects.filter(nombre__icontains='soporte').first()
if soporte:
    soporte.color_hex = '#ffb900'
    soporte.save()
    print('Soporte updated to #ffb900')

funcional = EstadoEquipo.objects.filter(nombre__icontains='funcional').first()
if funcional:
    funcional.color_hex = '#107c10'
    funcional.save()
    print('Funcional updated to #107c10')

no_funcional = EstadoEquipo.objects.filter(nombre__icontains='no funcional').first()
if no_funcional:
    no_funcional.color_hex = '#d13438'
    no_funcional.save()
    print('No Funcional updated to #d13438')

en_bodega = EstadoEquipo.objects.filter(nombre__icontains='bodega').first()
if en_bodega:
    en_bodega.color_hex = '#797775'
    en_bodega.save()
    print('En Bodega updated to #797775')