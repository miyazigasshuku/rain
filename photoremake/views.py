from photoremake.models import Photo
from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect, get_object_or_404
import cv2
from PIL import Image, ImageDraw, ImageFilter
from django.conf import settings
from django.http.response import JsonResponse
from photoremake.models import Photo, Images
from .forms import UploadForm, ImageForm
from django.utils.timezone import now
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

# 関数型でしか書いたことないから関数でまず書くわ
import cognitive_face as CF
from django.conf import settings

KEY = 'ce8eaf1cb30c45ada745055d2ebfd63b'
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)


@login_required
def index(request):
    '''
    新規投稿、一覧表示
    '''
    photos = Photo.objects.all()
    profile = Profile.objects.get(user=request.user)
    p_form = UploadForm()
    post_added = False
    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = UploadForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile  # 投稿者
            instance.save()
            p_form = UploadForm()  # 更新
            post_added = True
    context = {
        'photos': photos,
        'profile': profile,
        'p_form': p_form,
        'post_added': post_added
    }
    return render(request, 'index.html', context)


class PhotoUpdateView(LoginRequiredMixin, generic.UpdateView):
    '''
    投稿編集
    '''
    form_class = UploadForm
    model = Photo
    template_name = 'post_update.html'
    success_url = reverse_lazy('photoremake:index')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        # 投稿者本人しか編集できないようにする
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, '権限がありません。')
            return super().form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, generic.DeleteView):
    '''
    投稿削除
    '''
    model = Photo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('photoremake:index')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Photo.objects.get(pk=pk)
        # 投稿者本人しか編集できないようにする
        if not obj.author.user == self.request.user:
            messages.warning(self.request, '権限がありません。')
        return obj


face_cascade_path = '/usr/local/opt/opencv/share/'\
    'OpenCV/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)  # 顔認識


def upload_photo(request):
    obj = Photo.objects.all()
    form = UploadForm()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            usr = Profile.objects.get(user=request.user)
            img = Photo()
            img.title = request.POST['title']
            img.photo = request.FILES['photo']
            img.author = usr
            img.save()
            print("セーブ完了")
            return redirect('photoremake:index')
    else:
        form = UploadForm()
        obj = Photo.objects.all()

        # エラー処理のつもり
        if obj.exists() == False:
            return render(request, 'upload.html', {'form': form, 'obj': obj, })

        max_id = Photo.objects.latest('id').id
        obj = Photo.objects.get(id=max_id)
        x = settings.BASE_DIR + "/" + obj.photo.url
        y = settings.BASE_DIR + "/" + obj.photo.url
        # gray(x,y)
        back_aogaku(x, y)

    return render(request, 'upload.html', {
        'form': form,
        'obj': obj,
    })


def upload_image(request):
    objs = Images.objects.all()
    if request.method == 'POST':
        print("POSTはされてる")
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = Images()
            img.title = request.POST['title']
            img.image = request.FILES['image']
            img.action = request.POST['action']
            img.user = request.user.id
            img.uploaded_at = now()
            img.save()
            print("セーブ完了")
            return redirect('photoremake:index')
        else:
            print("失敗")
    else:
        form = ImageForm()

    return render(request, 'upload_image.html', {
        'form': form,
        'objs': objs,
    })


def emotion(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            usr = Profile.objects.get(user=request.user)
            img = Photo()
            img.title = request.POST['title']
            img.photo = request.FILES['photo']
            img.author = usr
            img.save()
            print("セーブ完了")
            return redirect('photoremake:emotion')
        else:
            print("失敗")
    else:
        form = UploadForm()
        obj = Photo.objects.all()
        if obj.exists() == False:
            return render(request, 'upload.html', {'form': form})
        max_id = Photo.objects.latest('id').id
        obj = Photo.objects.get(id=max_id)
        print(obj.photo.url)
        x = settings.BASE_DIR + "/" + obj.photo.url
        y = settings.BASE_DIR + "/" + obj.photo.url
        emo = analyze_emotion(x, y)
        one, two, three = emo[0], emo[1], emo[2]

    return render(request, 'emotion.html', {
        'form': form,
        'obj': obj,
        'emo': emo,
        "one": one,
        "two": two,
        "three": three,
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


def analyze_emotion(input_path, output_path):
    print(input_path)
    result = CF.face.detect(input_path, attributes='emotion')
    if result == []:
        result = [{"faceAttributes": {"emotion": {'anger': 0.0, 'contempt': 0.0, 'disgust': 0.0,
                                                  'fear': 0.0, 'happiness': 0.0, 'neutral': 0.0, 'sadness': 0.0, 'surprise': 0.0}}}]
    img = cv2.imread(input_path)
    print(result)
    emotion = result[0]["faceAttributes"]['emotion']
    print(emotion)
    sorted_dict = sorted(
        emotion.items(), key=lambda item: item[1], reverse=True)
    rank = sorted_dict[0:3]
    ranking = japanese(rank)
    text = str(rank)

    for i in range(len(rank)):
        text = str(rank[i][0])
        fifty = (i + 1) * 50
        cv2.putText(img, text, (0, fifty), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 0, 0), 6, lineType=cv2.LINE_AA)  # 文字書く！

    # cv2.putText(img, text,(0, 50),cv2.FONT_HERSHEY_PLAIN,3,(3,184,115),1, lineType=cv2.LINE_AA) #文字書く！
    cv2.imwrite(output_path, img)  # 保存
    return ranking


def japanese(ranking):
    for i in range(len(ranking)):
        integer = ranking[i][1]
        if ranking[i][0] == 'anger':
            text = "(' m '#)"
            if integer > 0.5:
                text = "このアプリに怒りをぶつけて！！"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "contempt":
            text = "-_-"
            if integer > 0.5:
                text = "ここまで蔑まれたらご褒b((ry"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "disgust":
            text = ">_<;"
            if integer > 0.5:
                text = "不愉快になるのは冬かい？"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "fear":
            text = "@_@;"
            if integer > 0.5:
                text = "畏れとは、、、悪い感情ではない"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "happiness":
            text = "❤︎_$"
            if integer > 0.5:
                text = "幸せのパラダイスや"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "neutral":
            text = "o_o"
            if integer > 0.5:
                text = "その感情「凪」"
            ranking[i] = (text, integer)
        elif ranking[i][0] == "sadness":
            text = "（ ;  ; ）"
            if integer > 0.5:
                text = "ひどく悲しいみたいだね"
            ranking[i] = (text, integer)
        else:
            text = "q (o ~ o) p"
            if integer > 0.5:
                text = "ひゃああああ"
            ranking[i] = (text, integer)
    print(ranking)
    return ranking
