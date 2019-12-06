from django.core.management.base import BaseCommand
from tcm.utils import sys_tcm, sys_literatures, sys_product


class Command(BaseCommand):
    help = 'Add data to db'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sys_literatures()
        sys_tcm()
        sys_product()
        self.stdout.write(self.style.SUCCESS('执行成功'))
