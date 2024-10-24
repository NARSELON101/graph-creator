import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Graph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.FileField(verbose_name='Путь до файла', upload_to='graph_storage')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("graphs:open_graph", kwargs={'graph_id': str(self.id)})

    def __str__(self):
        return f'{self.user.first_name}_{self.id}'