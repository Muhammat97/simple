from django import forms


class DownloadForm(forms.Form):
    your_name = forms.CharField(
        label='Your Name',
        max_length=50
    )
