"""
Copyright 2017 Willian Ver Valem Paiva

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import shutil
import os
from subprocess import call
import math
import argparse
import pandas as pd
import numpy as np
import cv2
import dlib
import progressbar
import numpy as np
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19

DETECTOR = dlib.get_frontal_face_detector()
PROGBAR = progressbar.ProgressBar(redirect_sdtdout=True)
PARSER = argparse.ArgumentParser(description='generate dataset')

def decompress_dataset():
    """this function will call a bash script that create the
    folders and decompress all the files"""
    call(['bash', 'untarData.sh'])


def split_dataset():
    """this function copy the first 82 subjects of
    the dataset to a training set"""

    for camera in ['a', 'b', 'c', 'd', 'e']:
        from_directory = './decompressed_dataset/'+camera+'/jpg'
        directory = './decompressed_dataset/'+camera+'_test/jpg'
        # walk all folders
        if not os.path.exists(directory):
            os.makedirs(directory)
        for _, _, filelist in os.walk(from_directory):
            if filelist[0] != '.DS_Store':
                for picture in filelist[:249]:
                    # move the file to the new path
                    shutil.move(from_directory+'/'+picture,
                                directory+'/'+picture)


def load_labels():
    """loads the landmarks into a pandas dataframe"""
    return pd.read_csv('./decompressed_dataset/' +
                       'muct-landmarks/muct76-opencv.csv')


def flip_image(image, label, direction, width, heigth):
    """flips a image and its labels based on the direction and return the new
    image and new labels"""
    flip = cv2.flip(image, direction)
    labels = []
    for i in range(0, 151, 2):
        if direction == 0:
            labels.append(label[i])
            labels.append(heigth - label[i+1])
        else:
            labels.append(width - label[i])
            labels.append(label[i+1])
    return (flip, labels)


def crop_image(image, size):
    """
    crop the image around the face with a square of a given size
    and returns the new image and the bounding box
    """
    faces = DETECTOR(image, 0)
    # all trainign and testing images has just 1 peson so any number diffrent
    # of one means dlib missclassified it
    if len(faces) != 1:
        return None
    else:
        for _, positions in enumerate(faces):
            top = positions.top()
            left = positions.left()
            bottom = top + size
            right = left + size
            box = {"top": top,
                   "left": left,
                   "bottom": bottom,
                   "right": right}

            constant = cv2.copyMakeBorder(image,
                                          0,
                                          50,
                                          0,
                                          50,
                                          cv2.BORDER_CONSTANT)

            res = constant[top:bottom, left:right]
            if res.shape != (size, size, 3):
                return None
            return (res, box)


def replace_landmarks(box, label):
    """recalculate and replace the landmarks on for a croped image"""
    labels = []
    for i in range(0, 151, 2):
        labels.append(label[i]-box["left"])
        labels.append(label[i+1]-box["top"])
    return labels


def get_label(name, labels):
    return labels.loc[labels['name'] == name].values.tolist()[0][2:]


def creae_dataset(size, flip_horizontal=True, flip_vertical=True):
    """generate the data-set with data augmentation and
    returns the the repective train and test set"""

    labels = load_labels()
    if not os.path.exists('./decompressed_dataset'):
        print("please decompress the data first and" +
              " create the test and train sets")
        return

    # the result dataset
    dataset = {"train_set": [],
               "train_labels": [],
               "test_set": [],
               "test_labels": []}
    # for the progress bar
    progress = 0
    factor = 100/3755

    for camera in ['a', 'b', 'c', 'd', 'e']:
        train_directory = './decompressed_dataset/'+camera+'/jpg'
        test_directory = './decompressed_dataset/'+camera+'_test/jpg'

        for _, _, filelist in os.walk(train_directory):
            # avoids the useless anoying osx file
            if filelist[0] != '.DS_Store':
                for picture in filelist:

                    # load the image on a numpy array
                    numpy_pic = cv2.imread(train_directory+"/"+picture)
                    numpy_pic = cv2.cvtColor(numpy_pic, cv2.COLOR_BGR2RGB)

                    # crop the image on the given size
                    image = crop_image(numpy_pic, size)
                    if image is not None:
                        numpy_pic = image[0]
                        name = picture.split(".")[0]
                        label = replace_landmarks(image[1],
                                                  get_label(name, labels))

                        # creates a horizontal mirror image
                        if flip_vertical:
                            vflip = flip_image(numpy_pic, label, 0, size, size)
                            dataset["train_set"].append(vflip[0])
                            dataset["train_labels"].append(vflip[1])

                        # creates a vertical mirror image
                        if flip_horizontal:
                            hflip = flip_image(numpy_pic, label, 1, size, size)
                            dataset["train_set"].append(hflip[0])
                            dataset["train_labels"].append(hflip[1])

                        dataset["train_set"].append(numpy_pic)
                        dataset["train_labels"].append(label)

                    progress += 1
                    PROGBAR.update(progress*factor)

        for _, _, filelist in os.walk(test_directory):
            if filelist[0] != '.DS_Store':
                for picture in filelist:
                    numpy_pic = cv2.imread(test_directory+"/"+picture)
                    numpy_pic = cv2.cvtColor(numpy_pic, cv2.COLOR_BGR2RGB)
                    image = crop_image(numpy_pic, size)
                    if image is not None:
                        numpy_pic = image[0]
                        name = picture.split(".")[0]
                        label = replace_landmarks(image[1],
                                                  get_label(name, labels))

                        # creates a horizontal mirror image
                        if flip_vertical:
                            vflip = flip_image(numpy_pic, label, 0, size, size)
                            dataset["test_set"].append(vflip[0])
                            dataset["test_labels"].append(vflip[1])

                        # creates a vertical mirror image
                        if flip_horizontal:
                            hflip = flip_image(numpy_pic, label, 1, size, size)
                            dataset["test_set"].append(hflip[0])
                            dataset["test_labels"].append(hflip[1])

                        dataset["test_set"].append(numpy_pic)
                        dataset["test_labels"].append(label)

                    progress += 1
                    PROGBAR.update(progress*factor)

    return dataset


def save_dataset(dataset, name):
    np.savez_compressed(name,
                        train_x=np.array(dataset["train_set"],
                                         dtype='float32'),
                        train_y=np.asarray(dataset["train_labels"],
                                           dtype='float32'),
                        test_x=np.array(dataset["test_set"],
                                        dtype='float32'),
                        test_y=np.asarray(dataset["test_labels"],
                                          dtype='float32'))


def inception_bottleneck(nameIn, nameOut):
    model = InceptionV3(weights='imagenet')
    train_data = np.load(nameIn)
    np.save(nameOut, model.predict(train_data, verbose=1))


def resnet_bottleneck(nameIn, nameOut):
    model = ResNet50(weights='imagenet')
    train_data = np.load(nameIn)
    np.save(nameOut, model.predict(train_data, verbose=1))


def vgg16_bottleneck(nameIn, nameOut):
    model = VGG16(weights='imagenet')
    train_data = np.load(nameIn)
    np.save(nameOut, model.predict(train_data, verbose=1))


def VGG19_bottleneck(nameIn, nameOut):
    model = VGG19(weights='imagenet')
    train_data = np.load(nameIn)
    np.save(nameOut, model.predict(train_data, verbose=1))
