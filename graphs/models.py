import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.FileField(verbose_name='Путь до файла', upload_to='graph_storage')
    name = models.CharField(verbose_name='Название датасета', max_length=50, default='')
    columns = models.JSONField('Столбцы', default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("graphs:open_dataset", kwargs={'dataset_id': str(self.id)})

    def __str__(self):
        return self.name
