"""
import os
import glob
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images')
LABEL_ROOT = os.path.join(MEDIA_ROOT, 'labels')
MASK_ROOT = os.path.join(MEDIA_ROOT, 'masks')


request_user_id = 1
#print(next(os.walk(os.path.join(IMAGE_ROOT, str(request_user_id))))[1])


paths = next(os.walk(IMAGE_ROOT))[1]
if not os.path.exists(os.path.join(IMAGE_ROOT, str(request_user_id))):
    os.makedirs(os.path.join(IMAGE_ROOT, str(request_user_id)))

# This is a data set path makedir
if paths != []:
    os.makedirs(os.path.join(IMAGE_ROOT, str(request_user_id) + '/' + str(int(paths[-1])+1)))
else:
    os.makedirs(os.path.join(IMAGE_ROOT, str(request_user_id) + '/1'))

data = glob.glob(os.path.join(IMAGE_ROOT, str(request_user_id) + '/1') + '/*.png')
print(data)

print(paths)


import glob
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images')
LABEL_ROOT = os.path.join(MEDIA_ROOT, 'labels')
MASK_ROOT = os.path.join(MEDIA_ROOT, 'masks')
images = os.path.join(IMAGE_ROOT, str(2) + '/' + str(2))
images = glob.glob(images + '/*.png')
print(images[0].split("media")[-1].replace("\\","/"))


from django.contrib.auth.models import User

Upload():
    user = User.objects.get(id=request.user.id)
    resimleri kayıt için:
    new = Department()
    new.user = user
    new.name = sube[0]
    new.save()

    örnek display için : user.data.all()












"""
