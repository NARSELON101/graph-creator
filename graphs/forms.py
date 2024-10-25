from django import forms

from graph_creator.types import ContentTypeRestrictedFileField


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = ContentTypeRestrictedFileField(content_types=['application/json', 'text/csv'])
