from django.shortcuts import render, redirect
from .models import ImageModel
from .forms import ImageForm, ImageFormUpdate
from django.views import generic
from django.contrib import messages
from django.core.files import File
from urllib.parse import urlparse
from urllib.request import urlopen
from PIL import Image
from backend.settings import MEDIA_URL, MEDIA_DIR
from backend.urls import URL_IMAGES


class Home(generic.ListView):
    model = ImageModel
    context_object_name = 'images'
    template_name = 'home.html'


class ImageCreateView(generic.CreateView):
    model = ImageModel
    form_class = ImageForm
    template_name = 'image_create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        instance = form.save(commit=False)

        have_url = bool(request.POST['url'])
        have_image = 'image' in request.FILES
        check = (have_image + have_url) % 2

        if not check:
            return render(request, 'error.html')
        
        if have_url:
            instance.name = urlparse(request.POST['url']).path.split('/')[-1]
            content = urlopen(request.POST['url'])
            instance.image.save(instance.name, File(content), save=False)
        elif have_image:
            instance.name = str(request.FILES['image'])
            instance.image.save(instance.name, request.FILES['image'], save=False)
        
        instance.save()
        return redirect(instance)


class ImageUpdateView(generic.UpdateView):
    model = ImageModel
    form_class = ImageFormUpdate
    template_name = 'image_edit.html'
    context_object_name = 'image'


    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        width = instance.image.width
        height = instance.image.height

        if request.POST['height']:
            height = int(request.POST['height'])
        
        if request.POST['width']:
            width = int(request.POST['width'])

        
        src_path = MEDIA_DIR / URL_IMAGES / instance.name
        dst_path = MEDIA_DIR / URL_IMAGES / f'new_{instance.name}'
        url_new_image = f'{MEDIA_URL}{URL_IMAGES}new_{instance.name}'
        orig_image = Image.open(src_path)
        new_image = orig_image.copy()
        new_image.thumbnail((width, height), Image.ANTIALIAS)
        new_image.save(dst_path)

        new_image = Image.open(dst_path)

        width, height = new_image.size

        return render(
            request,
            'image_edit.html',
            context={
                'form': ImageFormUpdate,
                'image': url_new_image,
                'width': width,
                'height': height,
                'flag': True
            }
        )
