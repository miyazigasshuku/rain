from photoremake.models import Photo
from django.shortcuts import render
from django.views import generic
from .forms import UploadForm
from django.shortcuts import redirect

class IndexView(generic.TemplateView):
    template_name = "index.html"


class LoginView(generic.TemplateView):
    template_name = "login.html"


class SignupView(generic.TemplateView):
    template_name = "signup.html"


# Create your views here.


#関数型でしか書いたことないから関数でまず書くわ

def index(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos})

# def index(request):
#     circles = Circles.objects.all().order_by('id')
#     for key in circles:
#         key.image.url_options.update({'secure':True})
#         key.icon.url_options.update({'secure':True})
#         key.matchimg.url_options.update({'secure':True})
#     return render(request, 'search/index.html', {'circles':circles})

def upload_photo(request):
    if request.method == "POST":
        form = UploadForm(request.POST)
        if form.is_valid():
            photo = Photo()
            print(request)
            photo.user = request.user.id
            photo.photo = request.FILES['photo']
            photo.save()
            return redirect('http://127.0.0.1:8000')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})