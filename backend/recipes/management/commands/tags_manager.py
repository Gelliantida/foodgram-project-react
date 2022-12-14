from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Loads tags'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS('Тэги загружены')
        )
