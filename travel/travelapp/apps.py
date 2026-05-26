from django.apps import AppConfig


class TravelappConfig(AppConfig):
    name = 'travelapp'

    def ready(self):
        import travelapp.signals