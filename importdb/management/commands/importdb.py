from django.core.management.base import BaseCommand
from tcm.utils import sys_tcm, sys_literatures, sys_product, sys_xingwei, sys_prescription

TABLE_NAME = {
    'tcm': sys_tcm,
    'literature': sys_literatures,
    'product': sys_product,
    'xingwei': sys_xingwei,
    'prescription': sys_prescription,
}


class Command(BaseCommand):
    help = 'Add data to db'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--tablename', help='导入的数据表')

    def handle(self, *args, **options):
        tablename = options.get('tablename')

        if not tablename:
            sys_literatures()
            sys_tcm()
            sys_product()
            sys_xingwei()
            sys_prescription()
            return

        table_list = tablename.split(',')

        for tb in table_list:
            if tb.lower() in TABLE_NAME.keys():
                TABLE_NAME.get(tb.lower())()
            else:
                self.stdout.write(self.style.ERROR('%s查看表名是否错误' % tb.lower()))

        self.stdout.write(self.style.SUCCESS('执行成功'))
