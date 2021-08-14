from photoremake.models import Photo, Back, Coordinated
from django.shortcuts import render
from django.views import generic
from .forms import UploadForm
from django.shortcuts import redirect, get_object_or_404
import cv2
from PIL import Image, ImageDraw, ImageFilter


# 関数型でしか書いたことないから関数でまず書くわ

def index(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos})

face_cascade_path = '/usr/local/opt/opencv/share/'\
                   'OpenCV/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path) #顔認識

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
    

    if request.method == "POST":
        coordinate = Coordinated()
        coordinate.photo_id = p
        coordinate.title = request.title
        coordinate.image = photo2image(request.back_id.back_img, request.p.photo)
        coordinate.save()
        url = '/after/' + str(coordinate.id)
        return redirect(url)

    return render(request, 'coordinate.html', {'p': p})

def after(request, pk):
    image = get_object_or_404(Coordinated, pk=pk)
    return render(request, 'after.html', {"image":image})