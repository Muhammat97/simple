import io
import os
import magic

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify

from PIL import Image, ImageDraw, ImageFont

from .forms import DownloadForm
from .models import Picture


def index(request):
    image_list = Picture.objects.order_by('-created_at')
    context = {'image_list': image_list}
    return render(request, 'gallery/index.html', context)


def detail(request, image_id):
    image = get_object_or_404(Picture, picture_uuid=image_id)
    context = {'image': image}

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DownloadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            # redirect to a new URL:
            return download_image(request, image_id, your_name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DownloadForm()
        context['form'] = form

    return render(request, 'gallery/detail.html', context)


def download_image(request, image_id, watermark):
    image = get_object_or_404(Picture, picture_uuid=image_id)
    image_path = image.image_path.path
    image_buffer = put_watermark(image_path, watermark)
    content_type = magic.from_buffer(image_buffer, True)
    filename = slugify(watermark) + '.png'
    response = HttpResponse(image_buffer, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def put_watermark(input_image_path, text):
    photo = Image.open(input_image_path)

    w, h = photo.size

    drawing = ImageDraw.Draw(photo)

    font_family = staticfiles_storage.path('font/SansitaSwashed-Regular.ttf')
    font = ImageFont.truetype(font_family, h * 5 // 100)

    text_w, text_h = drawing.textsize(text, font)

    pos = (w - text_w) - (w * 1 // 100), (h - text_h) - (h * 1 // 100)

    watermark = Image.new('RGBA', (text_w, text_h), (0, 0, 0, 0))
    drawing_watermark = ImageDraw.Draw(watermark)
    drawing_watermark.text((0, 0), text, (128, 128, 128, 128), font)

    base = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    base.paste(photo, (0, 0))
    base.paste(watermark, pos, mask=watermark)

    bytes_io = io.BytesIO()
    base.save(bytes_io, format='png')
    byte_array = bytes_io.getvalue()

    return byte_array
