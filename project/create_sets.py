""" high level support for file manipulation. """
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





def untar_files():
    """this function will call a bash script that create the folders and decompress all the files"""
    call(['bash', 'untarData.sh'])


def create_test_set():
    """this function copy the first 82 subjects of the dataset to a training set"""
    for camera in ['a', 'b', 'c', 'd', 'e']:
        from_directory = './decompressed_dataset/'+camera+'/jpg'
        directory = './decompressed_dataset/'+camera+'_test/jpg'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for _, _, filelist in os.walk(from_directory):
            if filelist[0] != '.DS_Store':
                for picture in filelist[:249]:
                    shutil.move(from_directory+'/'+picture, directory+'/'+picture)


def load_csv():
    """loads the landmarks into a pandas dataframe"""
    opencv_format = pd.read_csv('./decompressed_dataset/muct-landmarks/muct76-opencv.csv')
    return opencv_format

def get_flip(image, label, direction, width, heigth):
    """flips a image and its labels"""
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

def crop_picture(image, size):
    """crop the picture around the face with a square of a given size"""
    faces = DETECTOR(image, 1)
    # all trainign and testing images has just 1 peson so any number diffrent
    # of one means dlib missclassified it
    if len(faces) != 1:
        return None
    else:
        for _, positions in enumerate(faces):
            box_size = positions.bottom() - positions.top()
            change = size - box_size
            change_top = 0
            change_bottom = 0
            if change % 2 == 0:
                change_bottom = int(change/2)
                change_top = int(change/2)
            else:
                change_bottom = int(math.floor(change/2)) +1
                change_top = int(math.floor(change/2))



            top = positions.top()-change_top
            left = positions.left()-change_top
            bottom = positions.bottom()+change_bottom
            right = positions.right()+change_bottom
            box = {"top":top,
                   "left":left,
                   "bottom":bottom,
                   "right":right}

            return (image[top:bottom, left:right], box)

def recalculate_landmarks(box, label):
    """recalculate the landmarks on for a croped image"""
    labels = []
    for i in range(0, 151, 2):
        labels.append(label[i]-box["left"])
        labels.append(label[i+1]-box["top"])
    return labels

def load_dataset(size):
    """generate the data-set with data augmentation and
    returns the the repective train and test set"""

    if not os.path.exists('./decompressed_dataset'):
        print("please decompress the data first and create the test and train sets")
        return

    dataset = {"train_set":[], "train_labels":[], "test_set":[], "test_labels":[]}
    progress = 0
    factor = 100/3755
    for camera in ['a', 'b', 'c', 'd', 'e']:
        train_directory = './decompressed_dataset/'+camera+'/jpg'
        test_directory = './decompressed_dataset/'+camera+'_test/jpg'

        for _, _, filelist in os.walk(train_directory):
            if filelist[0] != '.DS_Store':
                for picture in filelist:
                    numpy_pic = cv2.imread(train_directory+"/"+picture)
                    numpy_pic = cv2.cvtColor(numpy_pic, cv2.COLOR_BGR2RGB)
                    image = crop_picture(numpy_pic, size)
                    if image != None:
                        #numpy_pic = image[0]
                        label = recalculate_landmarks(image[1],
                                                      LABELS.loc[LABELS['name']
                                                                 == picture.split(".")[0]]
                                                      .values.tolist()[0][2:])
                        vflip = get_flip(numpy_pic, label, 0, size, size)
                        hflip = get_flip(numpy_pic, label, 1, size, size)
                        dataset["train_set"].append(numpy_pic)
                        dataset["train_labels"].append(label)
                        dataset["train_set"].append(vflip[0])
                        dataset["train_labels"].append(vflip[1])
                        dataset["train_set"].append(hflip[0])
                        dataset["train_labels"].append(hflip[1])

                    progress += 1
                    PROGBAR.update(progress*factor)

        for _, _, filelist in os.walk(test_directory):
            if filelist[0] != '.DS_Store':
                for picture in filelist:
                    numpy_pic = cv2.imread(test_directory+"/"+picture)
                    numpy_pic = cv2.cvtColor(numpy_pic, cv2.COLOR_BGR2RGB)
                    image = crop_picture(numpy_pic, size)
                    if image != None:
                        label = recalculate_landmarks(image[1],
                                                      LABELS.loc[LABELS['name']
                                                                 == picture.split(".")[0]]
                                                      .values.tolist()[0][2:])
                        dataset["test_set"].append(numpy_pic)
                        dataset["test_labels"].append(label)

                    progress += 1
                    PROGBAR.update(progress*factor)

    return dataset






def gen_dataset(size):
    """genera the data set """
    if not os.path.exists('./decompressed_dataset'):
        print("decompresssing files")
        untar_files()

    if not os.path.exists('./decompressed_dataset/a_test/'):
        print("spliting the training and test set")
        create_test_set()

    print("generating the training and test set")
    sets = load_dataset(size)
    print("total of "+str(len(sets["train_set"]))+" training images")
    print("total of "+str(len(sets["test_set"]))+" testing images")
    return sets




DETECTOR = dlib.get_frontal_face_detector()
LABELS = load_csv()
PROGBAR = progressbar.ProgressBar(redirect_sdtdout=True)
PARSER = argparse.ArgumentParser(description='generate dataset')

def main():
    args = PARSER.parse_args()
    dataset = gen_dataset(args.size)
    print("saving sets")
    np.save("train_set.npy", np.array(dataset["train_set"], dtype="float32"))
    np.save("train_labels.npy", np.asarray(dataset["train_labels"], dtype="float32"))
    np.save("test_set.npy", np.array(dataset["test_set"], dtype="float32"))
    np.save("test_labels.npy", np.asarray(dataset["test_labels"], dtype="float32"))




if  __name__ == '__main__':
    PARSER.add_argument('-s',
                        action="store",
                        dest="size",
                        type=int,
                        default=299,
                        help="size to crop the image, the default is 299")
    main()
