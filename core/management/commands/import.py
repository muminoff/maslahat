# Django
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _l
from django.conf import settings

# Incogwas
from incogwas.models import Platform

# Misc
import csv
import codecs


class Command(BaseCommand):
    help = "Import sample data"
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('file_type', help='File type')
        parser.add_argument('file_path', help='File path')

    def handle(self, *args, **options):
        if options['file_type'] and options['file_path']:
            file_type = options.get('file_type', 'csv')
            file_path = options.get('file_path', './data.csv')
            file_contents = self.parse_file(file_type, file_path)  # noqa

    def parse_file(self, file_type, file_path):
        self.stdout.write(self.style.SUCCESS(
            _l("Parsing {file_type} file {file_path} ...".format(
                file_type=file_type,
                file_path=file_path))))
        handle = codecs.open(file_path, 'r', 'us-ascii')
        reader = csv.reader(handle, delimiter=',')
        next(reader)
        for sp in reader:
            self.stdout.write(self.style.SUCCESS(sp))
