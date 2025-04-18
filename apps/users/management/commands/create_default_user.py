from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a default admin user if not exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(email='admin@gmail.com').exists():
            User.objects.create_superuser('admin@gmail.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created default admin user.'))
        else:
            self.stdout.write('Default admin user already exists.')
