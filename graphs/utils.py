import os.path
import uuid
from django.apps import apps


def handle_uploaded_file(file, user):
    file_path = f'/{user.id}/{file}'
    # print(file, title, type_, user_id)
    if not os.path.exists(f'graph_storage/{user.id}'):
        os.mkdir(f'graph_storage/{user.id}/')
    with open(f"graph_storage{file_path}", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    graph, is_created = apps.get_model('graphs', 'Graph').objects.get_or_create(path=file_path, user=user)
    return is_created
