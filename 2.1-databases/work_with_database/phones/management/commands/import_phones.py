import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open("phones.csv", "r") as file:
            phones = list(csv.DictReader(file, delimiter=";"))

        for phone in phones:
            db_phone = Phone(
                phone["id"],
                phone["name"],
                phone["price"],
                phone["image"],
                phone["release_date"],
                phone["lte_exists"],
            )
            db_phone.save()