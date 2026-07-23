import re

def add_delete_acta_view(py_path):
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()

    new_view = """
class ActaDeleteView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'ELIMINAR_ACTAS'
    
    def post(self, request, acta_id):
        try:
            acta = ActaEntrega.objects.get(id=acta_id)
            
            # Liberar equipos
            for detalle in acta.detalles.all():
                if detalle.tipo_item == 'EQUIPO':
                    from equipos.models import Equipo
                    try:
                        equipo = Equipo.objects.get(id=detalle.id_item)
                        equipo.estado = 'bodega'
                        equipo.save()
                    except:
                        pass
                elif detalle.tipo_item == 'ANEXO':
                    from anexos.models import AnexoIP
                    try:
                        anexo = AnexoIP.objects.get(id=detalle.id_item)
                        anexo.estado = 'DISPONIBLE'
                        anexo.save()
                    except:
                        pass
                        
            # Registrar auditoría
            AuditoriaService.registrar(
                usuario=request.user,
                accion='ELIMINAR',
                modulo='ACTAS',
                entidad='ActaEntrega',
                entidad_id=acta.id,
                ip_address=get_client_ip(request),
                detalles={'codigo_acta': acta.codigo}
            )
            
            acta.delete()
            return JsonResponse({'status': 'success'})
            
        except ActaEntrega.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Acta no encontrada.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

"""
    # Just append it to the end of the file
    with open(py_path, 'a', encoding='utf-8') as f:
        f.write(new_view)
        
    print("Delete view added to views.py")

add_delete_acta_view(r'c:\proyectos\ticsystem\actas\views.py')
