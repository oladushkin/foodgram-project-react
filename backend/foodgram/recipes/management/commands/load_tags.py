import json

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            'recipes/management/commands/data/tags.json', 'rb'
        ) as file:
            data = json.load(file)
            for tag in data:
                Tag.objects.create(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug']
                )
