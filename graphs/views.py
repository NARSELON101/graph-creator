from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.apps import apps
from graphs.forms import UploadFileForm
from graphs.utils import handle_uploaded_file
from django.contrib import messages


# Create your views here.


def open_graph(request, graph_id):
    graph = apps.get_model('graphs', 'Graph').objects.get(pk=graph_id)

    return render(request, 'graphs/html/main.html', {'graph': graph})


def upload_dataset(request, is_created: str = None):
    if request.method == "POST":
        # print(request.POST, request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            is_created = handle_uploaded_file(request.FILES["file"], request.user)  # TODO Передать selery
            messages.info(request, "УРААА") if is_created else messages.warning(request, 'НЕЕЕТ')
    else:
        form = UploadFileForm()
    return render(request, "graphs/html/upload_dataset.html", {"form": form})
