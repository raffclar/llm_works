from django.apps import AppConfig


class DbDeadlocking(AppConfig):
    name = "concurrent_django"
    verbose_name = "Database Deadlocking Tests"
