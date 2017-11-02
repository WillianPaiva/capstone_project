import numpy as np
from keras.applications.inception_v3 import InceptionV3



def main():
    model = InceptionV3(weights='imagenet')
    train_data = np.load("train_set.npy")
    np.save("inceptionTrainBottleneck.npy", model.predict(train_data, verbose = 1))
    test_data = np.load("test_set.npy")
    np.save("inceptionTestBottleneck.npy", model.predict(test_data, verbose = 1))

if __name__ == '__main__':
    main()
