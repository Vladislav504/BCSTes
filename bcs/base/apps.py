from django.apps import AppConfig
from django.conf import settings


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self) -> None:
        return super().ready()
