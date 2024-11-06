from django.urls import path

from graphs import views

app_name = 'graphs'

urlpatterns = [
    path('open_dataset/<str:dataset_id>', views.open_graph_table, name='open_dataset'),
    path('upload_dataset/', views.upload_dataset, name='upload_dataset'),
    path('construct_diagram/', views.construct_diagram, name='construct_diagram'),
    path('upload_dataset/<str:is_created>', views.upload_dataset, name='upload_dataset'),
    path("datasets/", views.DatasetsView.as_view(), name='all_datasets')
]