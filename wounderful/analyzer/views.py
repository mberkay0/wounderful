from django.shortcuts import render, redirect
from django.http import Http404, FileResponse
from django.contrib import messages
from zipfile import ZipFile
from plotly.offline import plot
from . import plots
from . import scratch_analysis
from . import unetmodel
from .dash_apps.finished_apps import simpleexample
#from .models import UploadImage
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from skimage.io import imread
import re
import glob
import os
import shutil


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images')
LABEL_ROOT = os.path.join(MEDIA_ROOT, 'labels')
MASK_ROOT = os.path.join(MEDIA_ROOT, 'masks')

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]


def usage(request):
    return render(request, 'usage.html')


@login_required(login_url='/user/login')
def home(request):
    try:
        paths = next(os.walk(os.path.join(IMAGE_ROOT, str(request.user.id))))[1]
        data = glob.glob(os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + paths[-1]) + '/*.png')
        runtime = 5.75 * len(data)
        runtime = (len(data)*2.5*runtime // runtime) * 100
        context = {
            'runtime':runtime,
        }
        return render(request, 'run.html', context)
    except:
        messages.error(request, 'Please add a data-set!')
        return render(request, 'run.html')


@login_required(login_url='/user/login')
def analyze_images(request, pmk=-1):
    def plotScratch(fig):
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    if pmk != -1:
        data = glob.glob(os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(pmk)) + '/*.png')
        data_set = str(pmk)
    else:
        paths = next(os.walk(os.path.join(IMAGE_ROOT, str(request.user.id))))[1]
        data = glob.glob(os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + paths[-1]) + '/*.png')
        data_set = paths[-1]
    data.sort(key=natural_keys)
    testImages = scratch_analysis.preprocessing(data)
    predictions = unetmodel.ModelPredictions(testImages)
    woundArea, scratchWidth = scratch_analysis.analyze_the_scratch(predictions, data, request.user.id, data_set, rect=False)
    h, w = imread(data[0], 0).shape[:2]
    size = h * w
    frames=[i.split("\\")[-1].split(".")[0] for i in data]

    context = {
        'swidth': plotScratch(plots.plotScratchWidth([scratchWidth], frames)),
        'wound': plotScratch(plots.plotWoundArea([woundArea], frames)),
        'RWD': plotScratch(plots.plotRWD([woundArea], frames, [size])),
    }
    return render(request, 'index.html', context)


@login_required(login_url='/user/login')
def saveImages(request):
    return render(request, 'save_images.html', {})


@login_required(login_url='/user/login')
def Upload(request):
    if not os.path.exists(os.path.join(IMAGE_ROOT, str(request.user.id))):
        os.makedirs(os.path.join(IMAGE_ROOT, str(request.user.id)))

    paths = next(os.walk(os.path.join(IMAGE_ROOT, str(request.user.id))))[1]
    if paths != []:
        os.makedirs(os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(int(paths[-1]) + 1)))
        media_dir = os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(int(paths[-1]) + 1))
    else:
        os.makedirs(os.path.join(IMAGE_ROOT, str(request.user.id) + '/1'))
        media_dir = os.path.join(IMAGE_ROOT, str(request.user.id) + '/1')
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open(media_dir + '/' + str(count) + '.png', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        process(x)
    return redirect('home')


@login_required(login_url='/user/login')
def download_images(request):
    return download(request)


@login_required(login_url='/user/login')
def download(request):
    paths = next(os.walk(os.path.join(LABEL_ROOT, str(request.user.id))))[1]
    LABELS = os.path.join(LABEL_ROOT, str(request.user.id) + '/' + paths[-1])
    data = glob.glob(LABELS + '/*.png')
    # create a ZipFile object

    with ZipFile(LABELS + '/labels.zip', 'w') as zipObj:
        for filename in data:
            zipObj.write(filename=filename, arcname=filename.split("labels")[-1])
    try:
        response = FileResponse(open(LABELS + '/labels.zip', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(LABELS + '/labels.zip')
        return response
    except Exception:
        raise Http404


@login_required(login_url='/user/login')
def showlabels(request):
    paths = next(os.walk(os.path.join(LABEL_ROOT, str(request.user.id))))[1]
    images = os.path.join(LABEL_ROOT, str(request.user.id) + '/' + paths[-1])
    images = glob.glob(images + '/*.png')
    images.sort(key=natural_keys)
    images = [x.split("media")[-1].replace("\\","/") for x in images]
    context={
        'images':images,
    }
    return render(request, 'labels.html', context)


@login_required(login_url='/user/login')
def dataset(request):
    info = {}
    paths = next(os.walk(os.path.join(IMAGE_ROOT, str(request.user.id))))[1]
    for path in paths:
        data = os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + path)
        data = glob.glob(data + '/*.png')
        info[path] = data[0].split("media")[-1].replace("/","\\")

    if len(paths) != 0:
        context={
            'info':info,
        }
        return render(request, 'dataset.html', context)
    else:
        messages.error(request, 'Please add a data-set!')
        return render(request, 'dataset.html')


@login_required(login_url='/user/login')
def delete_dataset(request, pmk):
    try:
        images = os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(pmk))
        shutil.rmtree(images)
        return redirect('dataset')
    except:
        messages.error(request, 'Something was wrong!')
        return redirect('dataset')


@login_required(login_url='/user/login')
def showdataset(request, pmk):
    images = os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(pmk))
    images = glob.glob(images + '/*.png')
    images.sort(key=natural_keys)
    images = [x.split("media")[-1].replace("\\","/") for x in images]
    context={
        'images':images,
        'key':pmk,
    }
    return render(request, 'showdataset.html', context)


@login_required(login_url='/user/login')
def download_dataset(request, pmk):
    IMAGES = os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + str(pmk))
    data = glob.glob(IMAGES + '/*.png')
    # create a ZipFile object

    with ZipFile(IMAGES + '/dataset' + str(pmk) + '.zip', 'w') as zipObj:
        for filename in data:
            zipObj.write(filename=filename, arcname=filename.split("images")[-1])
    try:
        response = FileResponse(open(IMAGES + '/dataset' + str(pmk) + '.zip', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(IMAGES + '/dataset' + str(pmk) + '.zip')
        return response
    except Exception:
        raise Http404


@login_required(login_url='/user/login')
def multiple_analyze(request, pmks='+'):
    def plotScratch(fig):
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    if pmks != '+':
        pmks = pmks.split("+")
        pmks.remove('')
        pmks.sort(key=natural_keys)
        woundArealist=[]
        scratchWidthlist=[]
        sizelist=[]

        for pmk in pmks:
            data = glob.glob(os.path.join(IMAGE_ROOT, str(request.user.id) + '/' + pmk) + '/*.png')
            data.sort(key=natural_keys)
            testImages = scratch_analysis.preprocessing(data)
            predictions = unetmodel.ModelPredictions(testImages)
            woundArea, scratchWidth = scratch_analysis.analyze_the_scratch(predictions, data, request.user.id, pmk, rect=False)
            woundArealist.append(woundArea)
            scratchWidthlist.append(scratchWidth)
            h, w = imread(data[0], 0).shape[:2]
            size = h * w
            sizelist.append(size)
            frames = [i.split("\\")[-1].split(".")[0] for i in data]

        context = {
            'swidth': plotScratch(plots.plotScratchWidth(scratchWidthlist, frames)),
            'wound': plotScratch(plots.plotWoundArea(woundArealist, frames)),
            'RWD': plotScratch(plots.plotRWD(woundArealist, frames, sizelist)),
        }
        return render(request, 'index.html', context)

    else:
        messages.error(request, 'Please select a data-set!')
        return render(request, 'exceptions.html')

