from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from zipfile import ZipFile
from plotly.offline import plot
from . import plots
from . import scratch_analysis
from . import unetmodel
from .forms import UploadImageForm
from .models import UploadImage
from skimage.io import imread
import re
import glob
import os
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]


def home(request):
    data = glob.glob(MEDIA_ROOT + '/*.png')
    data.sort(key=natural_keys)
    runtime = 5.75 * len(data)
    runtime = (len(data)*2.5*runtime // runtime) * 100
    context = {
        'runtime':runtime,
    }
    return render(request, 'run.html', context)

"""
#Simple example
def analyze_images(request):
    def plotScratch(fig):
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    scratchWidth=[[456,43],[345,43],[256,22],[233,21],[12,1]]
    frames=['1','4','7','10','13']
    woundArea=[456,421,123,22,11]
    size=144444
    context = {
        'swidth': plotScratch(plots.plotScratchWidth(scratchWidth, frames)),
        'wound': plotScratch(plots.plotWoundArea(woundArea, frames)),
        'RWD': plotScratch(plots.plotRWD(woundArea, frames, size)),
    }
    return render(request, 'index.html', context)
"""
def analyze_images(request):
    def plotScratch(fig):
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    LABEL_ROOT = os.path.join(BASE_DIR, 'labels')
    path = glob.glob(LABEL_ROOT + '/*.png')
    if path != []:
        for i in path:
            os.remove(i)

    data = glob.glob(MEDIA_ROOT + '/*.png')
    data.sort(key=natural_keys)
    testImages = scratch_analysis.preprocessing(data)
    predictions = unetmodel.ModelPredictions(testImages)
    woundArea, scratchWidth = scratch_analysis.analyze_the_scratch(predictions, data, rect=False)
    h, w = imread(data[0], 0).shape[:2]
    size = h * w
    frames=[i.split("\\")[-1].split(".")[0] for i in data]

    context = {
        'swidth': plotScratch(plots.plotScratchWidth(scratchWidth, frames)),
        'wound': plotScratch(plots.plotWoundArea(woundArea, frames)),
        'RWD': plotScratch(plots.plotRWD(woundArea, frames, size)),
    }
    return render(request, 'index.html', context)
    
     #{% plotly_app name='SimpleExample' ratio=0.45 %} index.html de bak buna


def saveImages(request):
    path = glob.glob(MEDIA_ROOT + '/*.png')
    if path != []:
        for i in path:
            os.remove(i)
    return render(request, 'save_images.html', {})


def Upload(request):
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open(MEDIA_ROOT + '/' + str(count) + '.png', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        process(x)
    return redirect('home')


def download_images(request):
    return download(request)


def download(request):
    LABEL_ROOT = os.path.join(BASE_DIR, 'labels')
    data = glob.glob(LABEL_ROOT + '/*.png')
    # create a ZipFile object
    with ZipFile(LABEL_ROOT + '/labels.zip', 'w') as zipObj:
        for filename in data:
            zipObj.write(filename)
    try:
        response = FileResponse(open(LABEL_ROOT + '/labels.zip', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(LABEL_ROOT + '/labels.zip')
        return response
    except Exception:
        raise Http404
