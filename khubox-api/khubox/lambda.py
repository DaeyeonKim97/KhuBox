import os
import django
from .aws import s3_delete, s3_update_and_return_size
from .models import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def process_upload(event, context):
    file_id = event['Records'][0]['s3']['object']['key']
    file = File.objects.filter(id=file_id, deleted_at__isnull=True)

    # File Gone
    if len(file) == 0:
        s3_delete([file_id])
        return

    # Update
    file[0].size = s3_update_and_return_size(file_id, file[0].name)
    file[0].save()
