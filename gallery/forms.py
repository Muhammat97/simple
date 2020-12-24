from django import forms


class DownloadForm(forms.Form):
    your_name = forms.CharField(
        label='Your Thing',
        max_length=50
    )
