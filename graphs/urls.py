from django.urls import path

from graphs import views

app_name = 'graphs'

urlpatterns = [
    path('/open_graph/<str:graph_id>', views.open_graph, name='open_graph'),
    path('/upload_dataset', views.upload_dataset, name='upload_dataset')
]