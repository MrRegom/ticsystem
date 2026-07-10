# config package init.
# La migracion de datos MySQL/MariaDB→PostgreSQL (Fase 5) se hace con PyMySQL
# directo en el management command 'migrar_desde_mysql', sin pasar por el ORM de
# Django (Django 6.0 exige MariaDB 10.6+ y XAMPP trae 10.4.32).
