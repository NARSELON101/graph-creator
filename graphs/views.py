from django.shortcuts import render
from django.apps import apps
from django.views.generic import ListView
from filterer.data_frame_filter import DataFrameFilter
from filterer.df_filter import ColumnsFilter, RowsCountFilter
from graphs.forms import UploadFileForm
from django.contrib import messages

from graphs.graph_constructor.graphs_constructor import GraphConstructor
from repositories.vizualizer import HTMLFormatter
from repositories import services

separators = [',', '\t', '\n']
graph_creator = GraphConstructor()

# Create your views here.


# @cache_page(60*15)
async def open_graph_table(request, dataset_id):
    include_columns = request.POST.getlist("include_columns[]")
    rows_count = request.POST.get("rows_count", '')
    if rows_count.isdecimal():
        rows_count = int(rows_count)
    else:
        rows_count = None
    if include_columns is None:
        include_columns = []
    graph = await apps.get_model('graphs', 'Dataset').objects.aget(pk=dataset_id)

    pl_, columns = services.get_dataframe_from_path(str(graph.path))

    pl_ = await DataFrameFilter([ColumnsFilter(include_columns),
                                 RowsCountFilter(rows_count=rows_count)]
                                ).filter_data(pl_)

    html_table = await HTMLFormatter().convert_df_to_table(pl_)

    return render(request, 'graphs/html/main.html', {'table': html_table, 'columns': columns,
                                                     'graph': graph,
                                                     'rows_count': rows_count,
                                                     'include_columns': include_columns or columns,
                                                     "plot_html": ''})


def construct_diagram(request):
    dataset_columns = None
    dataset = None
    x_name = y_name = None
    diagram = None
    is_sorted = False
    available_diagrams = []
    diagram_method_attr_name = None

    print(request.POST)
    if request.method == 'POST':
        dataset_id = request.POST.get("dataset_id")
        x_name, y_name = request.POST.get("x"), request.POST.get("y")
        is_sorted = request.POST.get("is_sorted", False)
        diagram_method_attr_name = request.POST.get("diagram_method_attr_name")
        if dataset_id:
            dataset = apps.get_model('graphs', 'Dataset').objects.get(pk=dataset_id)
            dataset_columns = dataset.columns.get('columns')
        if (x_name and y_name and
                (x_name in [data.get('name') for data in dataset.columns.get('columns')]
                 and y_name in [data.get('name') for data in dataset.columns.get('columns')])):
            x_value, y_value = services.get_df_column_values(dataset, [x_name, y_name])
            x_type, y_type = services.get_column_type(x_value), services.get_column_type(y_value)
            available_diagrams = graph_creator.get_available_types(x_type, y_type)
            if diagram_method_attr_name:
                values = {key: value for key, value in request.POST.items()}
                values.update({'is_sorted': is_sorted})
                diagram = graph_creator.construct_diagram(**values,
                                                          x_name=x_name, y_name=y_name,
                                                          x_value=x_value, y_value=y_value)

    return render(request, 'graphs/html/diagram_constructor.html',
                  {"graphs": apps.get_model('graphs', "Dataset").objects.all(),
                   "dataset_columns": dataset_columns,
                   'dataset': dataset,
                   "x_name": x_name,
                   "y_name": y_name,
                   'diagram': diagram,
                   'is_sorted': is_sorted,
                   'available_diagrams': available_diagrams,
                   'diagram_method_attr_name': diagram_method_attr_name})


def upload_dataset(request, is_created: str = None):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            is_created = services.handle_uploaded_file(request.FILES["file"], request.user,
                                                       request.POST.get("title"),
                                                       apps.get_model('graphs',
                                                                      'Dataset'))  # TODO Передать selery
            messages.info(request, "Файл загружен") if is_created \
                else messages.warning(request, 'Для загрузки доступны только форматы JSON и CSV')
        else:
            messages.warning(request, 'Для загрузки доступны только форматы JSON и CSV')

    else:
        form = UploadFileForm()
    return render(request, "graphs/html/upload_dataset.html", {"form": form})


class DatasetsView(ListView):
    model = apps.get_model('graphs', 'Dataset')
    paginate_by = 8
    template_name = 'graphs/html/all_datasets.html'

    context_object_name = 'datasets'

    def get_queryset(self):
        return apps.get_model('graphs', 'Dataset').objects.all()
