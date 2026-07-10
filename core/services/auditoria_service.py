from core.models import LogAuditoria
from core.repositories.auditoria_repository import AuditoriaRepository

class AuditoriaService:
    """
    Servicio de negocio para gestionar la auditoría y trazabilidad del sistema.
    """

    @classmethod
    def registrar_accion(cls, usuario: str, accion: str, tabla: str, 
                         registro_id: str, detalles: str, ip_address: str) -> LogAuditoria:
        log = LogAuditoria(
            usuario=usuario,
            accion=accion,
            tabla=tabla,
            registro_id=str(registro_id) if registro_id else None,
            detalles=detalles,
            ip_address=ip_address
        )
        return AuditoriaRepository.save(log)
