import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

file_table = {
    'ingredients.csv': Ingredient,
    'tags.csv': Tag,
}


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        for file, table in file_table.items():
            with open(f'data/{file}', 'r', encoding='utf8') as f:
                if file == 'ingredients.csv':
                    fieldnames = ['name', 'measurement_unit']
                elif file == 'tags.csv':
                    fieldnames = ['name', 'color', 'slug']
                dr = csv.DictReader(f, delimiter=',', fieldnames=fieldnames)
                for row in dr:
                    if file == 'ingredients.csv':
                        name = row.pop('name')
                        unit = row.pop('measurement_unit')
                        table.objects.get_or_create(name=name,
                                                    measurement_unit=unit)
                    elif file == 'tags.csv':
                        name = row.pop('name')
                        color = row.pop('color')
                        slug = row.pop('slug')
                        table.objects.get_or_create(name=name, color=color,
                                                    slug=slug)
                self.stdout.write(f'Таблица {table.__name__} заполнена!')
