import numpy as np
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19


def main():
    model = InceptionV3(weights='imagenet')
    train_data = np.load("train_set299.npy")
    np.save("inceptionTrainBottleneck.npy", model.predict(train_data, verbose = 1))
    test_data = np.load("test_set299.npy")
    np.save("inceptionTestBottleneck.npy", model.predict(test_data, verbose = 1))


    
    model = ResNet50(weights='imagenet')
    train_data = np.load("train_set224.npy")
    np.save("resnetTrainBottleneck.npy", model.predict(train_data, verbose = 1))
    test_data = np.load("test_set224.npy")
    np.save("resnetTestBottleneck.npy", model.predict(test_data, verbose = 1))


    model = VGG16(weights='imagenet')
    train_data = np.load("train_set224.npy")
    np.save("vgg16TrainBottleneck.npy", model.predict(train_data, verbose = 1))
    test_data = np.load("test_set224.npy")
    np.save("vgg16TestBottleneck.npy", model.predict(test_data, verbose = 1))


    model = VGG19(weights='imagenet')
    train_data = np.load("train_set224.npy")
    np.save("vgg19TrainBottleneck.npy", model.predict(train_data, verbose = 1))
    test_data = np.load("test_set224.npy")
    np.save("vgg19TestBottleneck.npy", model.predict(test_data, verbose = 1))

if __name__ == '__main__':
    main()
