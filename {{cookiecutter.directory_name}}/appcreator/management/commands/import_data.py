from django.core.management.base import BaseCommand
from appcreator.import_utils import run_import


class Command(BaseCommand):
    help = "Import Data"

    def handle(self, *args, **kwargs):
        run_import("archiv", file_class_map_dict=None, limit=None)
