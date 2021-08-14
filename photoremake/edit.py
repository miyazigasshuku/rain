import cv2
from PIL import Image, ImageDraw, ImageFilter

face_cascade_path = '/usr/local/opt/opencv/share/'\
                   'OpenCV/haarcascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path) #顔認識
image_path = "../../../images/"


def main():
    im1 = Image.open('images/aogaku.jpg') #ベースになる写真
    im2 = Image.open('images/doumo.png') #顔だけくり抜く時に使用
    src = cv2.imread('images/unnamed.jpg') #顔の位置を判別するために使用
    #ここがちょっとよくわかってなくて、同じ写真を2回読み込んじゃってる

    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(src_gray)
    # 顔認識

    for x, y, w, h in faces:
        mask_im = Image.new("L", im2.size, 0) # Lがよく分からない
        draw = ImageDraw.Draw(mask_im)
        draw.rectangle((x, y, x+w, y+h), fill=255) # 写真を顔の位置だけくり抜く

    im1.paste(im2, (0, 0), mask_im) #im1にくり抜いた写真を貼り付け
    im1.save('unit_output.jpg', quality=95) #保存

    src2 = cv2.imread('unit_output.jpg') #文字を書くために合成した写真を呼び出し
    cv2.putText(src2,'AOYAMAGAKUIN',(20, 500),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),4, lineType=cv2.LINE_AA) #文字書く！

    cv2.imwrite('unit_output.jpg', src2) #保存
    return src2

main()