import os

from django.core.management.base import BaseCommand

from apps.common.models import Media


class Command(BaseCommand):
    help = 'Clean up unused files'

    def handle(self, *args, **options):
        # Get a list of all image files in the upload directory
        upload_dir = 'media/'
        existing_files = set(os.listdir(upload_dir))

        # Get a list of filenames from the database
        filenames_in_db = set(Media.objects.values_list('image', flat=True))

        # Find orphaned files and delete them
        orphaned_files = existing_files - filenames_in_db
        for filename in orphaned_files:
            file_path = os.path.join(upload_dir, filename)
            os.remove(file_path)
            self.stdout.write(self.style.SUCCESS(f'Deleted: {filename}'))
