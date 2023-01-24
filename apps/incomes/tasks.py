from pathlib import Path

from django.core.files import File
from django.core.files.storage import FileSystemStorage

from celery import shared_task
from cloudinary.uploader import upload_image

from apps.incomes.models import Income


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def upload_image_task(self, file_name, path, id):

    storage = FileSystemStorage()
    path_object = Path(path)

    with path_object.open(mode="rb") as file:
        picture = File(file, name=path_object.name)
        image_url = upload_image(picture)

    storage.delete(file_name)
    income = Income.objects.get(id=id)
    income.image = image_url
    income.save()
