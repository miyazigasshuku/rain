from photoremake.models import Photo
from django.shortcuts import render
from django.views import generic
from .forms import UploadForm
from django.shortcuts import redirect
import cv2
from PIL import Image, ImageDraw, ImageFilter
from django.conf import settings
from profiles.models import Profile
from django.contrib.auth.decorators import login_required

# 関数型でしか書いたことないから関数でまず書くわ


@login_required
def index(request):
    photos = Photo.objects.all()
    profile = Profile.objects.get(user=request.user)
    context = {
        'photos': photos,
        'profile': profile
    }
    return render(request, 'index.html', context)


face_cascade_path = '/usr/local/opt/opencv/share/'\
    'OpenCV/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)  # 顔認識


def upload_photo(request):
    obj = Photo.objects.all()
    form = UploadForm()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, request.POST)
        if form.is_valid():
            form.save()
            print("セーブ完了")
            return redirect('photoremake:index')
    # else:
    #     form = UploadForm()
    #     obj = Photo.objects.all()

    #     # エラー処理のつもり🥺
    #     if obj.exists() == False:
    #         return render(request, 'upload.html', {'form': form, 'obj': obj, })

    #     max_id = Photo.objects.latest('id').id
    #     obj = Photo.objects.get(id=max_id)
    #     x = settings.BASE_DIR + "/" + obj.photo.url
    #     y = settings.BASE_DIR + "/" + obj.photo.url
    #     # gray(x,y)

    #     print(x)
    #     back_aogaku(x, y)

    return render(request, 'upload.html', {
        'form': form,
        'obj': obj,
    })


###########ここをカスタマイズ############

def gray(input_path, output_path):
    img = cv2.imread(input_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, img_gray)


def back_aogaku(input_path, output_path):
    face = Image.open(input_path)
    back_img = settings.BASE_DIR + "/images/aogaku.jpg"
    judge = cv2.imread(input_path)  # 顔の位置を判別するために使用
    back = Image.open(back_img)
    faces = face_cascade.detectMultiScale(judge)
    for x, y, w, h in faces:
        mask_im = Image.new("L", face.size, 0)  # Lがよく分からない
        draw = ImageDraw.Draw(mask_im)
        draw.rectangle((x, y, x+w, y+h), fill=255)  # 写真を顔の位置だけくり抜く
    back = back.copy()
    back.paste(face, (0, 0), mask_im)  # im1にくり抜いた写真を貼り付け
    back.save(input_path, quality=95)
    img = cv2.imread(input_path)
    cv2.putText(img, 'AOYAMAGAKUIN', (20, 500), cv2.FONT_HERSHEY_COMPLEX,
                3, (255, 0, 255), 4, lineType=cv2.LINE_AA)  # 文字書く！
    cv2.imwrite(output_path, img)  # 保存
