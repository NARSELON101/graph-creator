from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps

from graphs.forms import UploadFileForm


# Create your views here.


def open_graph(request, graph_id):
    graph = apps.get_model('graphs', 'Graph').objects.get(pk=graph_id)

    return render(request, 'graphs/html/main.html', {'graph': graph})


def upload_dataset(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            # handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "graphs/html/upload_dataset.html", {"form": form})