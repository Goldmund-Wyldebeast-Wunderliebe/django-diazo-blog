from django.core.management.base import BaseCommand

from diazo_blog.tests import create_admin_user

class Command(BaseCommand):
    def handle(self, *args, **options):
        create_admin_user()
