from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.apps import apps
from graphs.forms import UploadFileForm
from graphs.utils import handle_uploaded_file
from django.contrib import messages
import polars as pl
from repositories.vizualizer import HTMLFormatter
from django.views.decorators.cache import cache_page, never_cache
from polars.exceptions import ComputeError
from asgiref.sync import sync_to_async, async_to_sync
from cache_clients.redis_client import RedisCache

separators = [',', '\t', '\n']


# Create your views here.


# @cache_page(60*15)
async def open_graph(request, graph_id):
    include_columns = request.POST.getlist("include_columns[]")
    rows_count = request.POST.get("rows_count", '')
    if rows_count.isdecimal():
        rows_count = int(rows_count)
    else:
        rows_count = None
    if include_columns is None:
        include_columns = []
    graph = await apps.get_model('graphs', 'Graph').objects.aget(pk=graph_id)
    html_table = ""
    columns = []

    for sep in separators:
        try:
            pl_ = pl.read_csv(str(graph.path), separator=sep)

            if len(pl_.columns) == 1:
                continue
            html_table, columns = await HTMLFormatter().convert_df_to_table(pl.read_csv(str(graph.path), separator=sep),
                                                                            rows_count=rows_count,
                                                                            include_columns=include_columns)
        except ComputeError:
            pass
    return render(request, 'graphs/html/main.html', {'table': html_table, 'columns': columns,
                                                     'graph_id': graph_id,
                                                     'rows_count': rows_count,
                                                     'include_columns': include_columns or columns})


def upload_dataset(request, is_created: str = None):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            is_created = handle_uploaded_file(request.FILES["file"], request.user)  # TODO Передать selery
            messages.info(request, "УРААА") if is_created else messages.warning(request, 'НЕЕЕТ')
        else:
            messages.warning(request, 'Для загрузки доступны только форматы JSON и CSV')

    else:
        form = UploadFileForm()
    return render(request, "graphs/html/upload_dataset.html", {"form": form})
