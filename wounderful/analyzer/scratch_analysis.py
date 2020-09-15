import datetime
import cv2
import os
import numpy as np
from skimage.io import imread, imsave
from skimage.transform import resize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'images')
LABEL_ROOT = os.path.join(MEDIA_ROOT, 'labels')
MASK_ROOT = os.path.join(MEDIA_ROOT, 'masks')


def preprocessing(filepath):
    IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS = 256, 256, 3
    testImages = np.zeros((len(filepath), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)

    for n, frame in enumerate(filepath):
        img = imread(frame)[:, :, :IMG_CHANNELS]
        img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
        testImages[n] = img

    return testImages


def measure_width(mask, step=10):
    height, width = mask.shape[:2]
    distances = []

    for h in range(0, height, step):
        boolarr = mask[h] == 255
        dist = np.array(np.where(boolarr))
        if dist.shape != (1, 0):
            distances.append(dist[0].max() - dist[0].min())

    distances = np.array(distances)
    mean_width = 0 if np.isnan(distances.mean()) else distances.mean()

    if mean_width != 0:
        std_dev = np.std(distances)
    else:
        std_dev = 0

    return mean_width, std_dev


def analyze_the_scratch(predictions, frames, user_id, data_set, rect=True):
    now = datetime.datetime.now()
    woundArea = []
    scratchWidth = []

    #find contours module.
    for pred, frame in zip(predictions, frames):
        name = frame.split("\\")[-1]
        pred = np.squeeze(pred)
        img = imread(frame)
        h, w = img.shape[:2]
        pred = resize(pred, (h, w))
        pred = np.where(pred >= 0.5, 1, 0)
        pred = pred * 255
        pred = pred.astype('uint8')
        contours, _ = cv2.findContours(pred, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Check the contours and predicted mask
        size = h * w

        mask = np.zeros((h, w))

        contourArea = 0
        contourAreaIndex = []

        infinite = True
        while infinite:
            for c in range(len(contours)):
                if cv2.contourArea(contours[c]) >= size or cv2.contourArea(contours[c]) >= size // (w // 6):
                    contourArea += (cv2.contourArea(contours[c]))
                    contourAreaIndex.append(int(c))

            if len(contourAreaIndex) > 0:
                for a in range(len(contourAreaIndex)):
                    cv2.drawContours(img, contours, contourAreaIndex[a], (0, 255, 0), 3)
                    cv2.fillPoly(mask, pts=[contours[contourAreaIndex[a]]], color=(255, 255, 255))

                infinite = False
            else:
                size = size - size * 0.05

            if size < 2:
                contourArea = 0
                contourAreaIndex.append(0)
                infinite = False

        swidth, std_dev = measure_width(mask)

        # Put the text for info
        cv2.putText(img, 'File: {}'.format(name), (2, 32), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'File: {}'.format(name), (0, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'Wound Area: {} pixels'.format(contourArea), (2, 62), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(img, 'Wound Area: {} pixels'.format(contourArea), (0, 60), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(img, 'Scratch Width: {:.2f} +- {:.2f} pixels'.format(swidth, std_dev), (2, 92),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'Scratch Width: {:.2f} +- {:.2f} pixels'.format(swidth, std_dev), (0, 90),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'Date: {}/{}/{}'.format(now.day, now.month, now.year), (2, 122), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, 'Date: {}/{}/{}'.format(now.day, now.month, now.year), (0, 120), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (0, 255, 0), 2, cv2.LINE_AA)

        # Put the rectangle for info
        if rect and contours != []:
            for c in contourAreaIndex:
                rect = cv2.minAreaRect(contours[c])
                boxPts = cv2.boxPoints(rect)
                boxPts = np.int0(boxPts)
                cv2.drawContours(img, [boxPts], 0, (0, 0, 255), 3)

        # Add calculated width and area.
        woundArea.append(contourArea)
        scratchWidth.append([swidth, std_dev])

        # Save mask and labelled image
        #cv2.imwrite(MASK_ROOT + '/' + name, mask)
        if not os.path.exists(os.path.join(LABEL_ROOT, str(user_id) + '/' + data_set)):
            os.makedirs(os.path.join(LABEL_ROOT, str(user_id) + '/' + data_set))

        name = 'lb' + name
        fp = os.path.join(LABEL_ROOT, str(user_id) + '/' + data_set + '/' + name)
        # cv2.imwrite(os.path.join(fp), img)
        imsave(fp, img)

    return woundArea, scratchWidth