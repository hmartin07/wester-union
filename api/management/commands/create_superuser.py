# api/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email='johnnyalexanderjuca@gmail.com').exists():
            User.objects.create_superuser(email='johnnyalexanderjuca@gmail.com', password='admin123')
        self.stdout.write(self.style.SUCCESS('Superuser created'))
