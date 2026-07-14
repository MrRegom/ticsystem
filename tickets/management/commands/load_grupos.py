from django.core.management.base import BaseCommand
from tickets.models import GrupoResolutor, Categoria

class Command(BaseCommand):
    help = 'Carga los grupos resolutores por defecto'

    def handle(self, *args, **kwargs):
        g_equipamiento, _ = GrupoResolutor.objects.get_or_create(
            nombre="Soporte Equipamiento y Hardware",
            defaults={"descripcion": "Reparación de PCs, Impresoras, Periféricos"}
        )
        g_sistemas, _ = GrupoResolutor.objects.get_or_create(
            nombre="Sistemas y Software Médico",
            defaults={"descripcion": "Soporte para HIS, LIS, RIS, ERP y software ofimático"}
        )
        g_redes, _ = GrupoResolutor.objects.get_or_create(
            nombre="Redes e Infraestructura",
            defaults={"descripcion": "Problemas de WiFi, cableado, switches y telefonía"}
        )

        # Asignar a algunas categorías por defecto para prueba
        # Asumiendo que existen categorías como 'Hardware', 'Software', 'Redes'
        Categoria.objects.filter(nombre__icontains="Hardware").update(grupo_resolutor=g_equipamiento)
        Categoria.objects.filter(nombre__icontains="Impresora").update(grupo_resolutor=g_equipamiento)
        Categoria.objects.filter(nombre__icontains="Software").update(grupo_resolutor=g_sistemas)
        Categoria.objects.filter(nombre__icontains="Red").update(grupo_resolutor=g_redes)
        Categoria.objects.filter(nombre__icontains="Internet").update(grupo_resolutor=g_redes)

        self.stdout.write(self.style.SUCCESS('Grupos resolutores inicializados y asignados a categorías coincidentes.'))
