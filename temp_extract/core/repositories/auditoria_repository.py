from core.models import LogAuditoria

class AuditoriaRepository:
    """
    Repositorio de datos para el modelo LogAuditoria.
    Encapsula la creación e inserción de logs de auditoría en la base de datos.
    """

    @staticmethod
    def save(log: LogAuditoria) -> LogAuditoria:
        log.save()
        return log
