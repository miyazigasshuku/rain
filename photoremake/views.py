from photoremake.models import Back, Photo, Coordinated
from django.shortcuts import render
from django.views import generic
from .forms import UploadForm
from django.shortcuts import redirect, get_object_or_404
from . import edit
import cv2
from PIL import Image, ImageDraw, ImageFilter
import numpy
import torch

face_cascade_path = '/usr/local/opt/opencv/share/'\
                   'OpenCV/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path) #顔認識

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

def upload_photo(request):
    if request.method == "POST":
        form = UploadForm(request.POST)
        if form.is_valid():
            photo = Photo()
            print(request)
            photo.user = request.user.id
            photo.photo = request.FILES['photo']
            photo.save()
            return redirect('/')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def photo2image(back, photo):
    #加工部分
    im1 = Image.open(back) #ベースになる写真
    im2 = Image.open(photo) #顔だけくり抜く時に使用
    src = cv2.imread(photo) #顔の位置を判別するために使用
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(src_gray)
            # 顔認識

    for x, y, w, h in faces:
        mask_im = Image.new("L", im2.size, 0) # Lがよく分からない
        draw = ImageDraw.Draw(mask_im)
        draw.rectangle((x, y, x+w, y+h), fill=255) # 写真を顔の位置だけくり抜く

    im1.paste(im2, (0, 0), mask_im) #im1にくり抜いた写真を貼り付け
    cv2.putText(im1,'AOYAMAGAKUIN',(20, 500),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),4, lineType=cv2.LINE_AA) #文字書く！
    return im1

def coordinate(request, pk):
    p = get_object_or_404(Photo, pk=pk)
    back = Back.objects.get(title="サガ祭")

    if request.method == "POST":
        coordinate = Coordinated()
        coordinate.photo_id = p
        coordinate.back_id = back.id
        coordinate.title = request.title
        coordinate.image = photo2image(request.back_id.back_img, request.p.photo)
        coordinate.save()
        url = '/after/' + str(coordinate.id)
        return redirect(url)

    return render(request, 'coordinate.html', {'p': p})

def after(request, pk):
    image = get_object_or_404(Coordinated, pk=pk)
    return render(request, 'after.html', {"image":image})

# def coordinate(request, pk):
#     photo = get_object_or_404(Photo, pk=pk)

#     if request.method == "POST":
#         form = CoordinateForm(request.POST)
#         if form.is_valid():

#             im1 = Image.open('images/aogaku.jpg') #ベースになる写真
#             im2 = Image.open(photo.photo) #顔だけくり抜く時に使用
#             im3 = numpy.array(im2)
#             print(torch.from_numpy(cv2.imread(im3.dtype)))
#             src = cv2.imread(type(im3)) #顔の位置を判別するために使用
#             #ここがちょっとよくわかってなくて、同じ写真を2回読み込んじゃってる

#             src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(src_gray)
#             # 顔認識

#             for x, y, w, h in faces:
#                 mask_im = Image.new("L", im2.size, 0) # Lがよく分からない
#                 draw = ImageDraw.Draw(mask_im)
#                 draw.rectangle((x, y, x+w, y+h), fill=255) # 写真を顔の位置だけくり抜く

#             back_im = im1.copy() #imgが上書き保存されないようにコピー ファイル名変えて保存するならいらない気がする
#             back_im.paste(im2, (0, 0), mask_im) #im1にくり抜いた写真を貼り付け
#             back_im.save('unit_output.jpg', quality=95) #保存

#             src2 = cv2.imread('unit_output.jpg') #文字を書くために合成した写真を呼び出し
#             cv2.putText(src2,'AOYAMAGAKUIN',(20, 500),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),4, lineType=cv2.LINE_AA) #文字書く！

#             cv2.imwrite('images/unit_output.jpg', src2) #保存
#             print("加工終了")



#             coordinate = Coordinated()
#             coordinate.photo_id = photo
#             coordinate.image = back_im
#             coordinate.save()
#             return redirect('/after/' + coordinate.pk)
#     else:
#         form = UploadForm()
#     return render(request, 'coordinate.html', {'p': photo, "form":form})

