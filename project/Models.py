import numpy as np
from keras.layers import *
from keras.models import Sequential, Model
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras import regularizers
from keras import optimizers, initializers
from keras.utils import plot_model
from keras.applications.inception_v3 import InceptionV3
from keras.applications.resnet50 import ResNet50

dataset = np.load("./withflip/299_dataset.npz")


def train_inception_v3_bottleneck():
    # lets create some variations of the thata so we augment the features 
    train_x = np.load("./withflip/inception_train.npy")
    train_x2 = train_x**2
    sin_train_x = np.sin(train_x)
    test_x = np.load("./withflip/inception_test.npy")
    test_x2 = test_x**2
    sin_test_x = np.sin(test_x)

    train_y = dataset["train_y"]/299
    test_y = dataset["test_y"]/299

    tbCallBack = TensorBoard(log_dir='./inceptionBottleneck',
                             histogram_freq=0,
                             write_graph=True,
                             write_images=True,
                             write_grads=True)


    checkpointer = ModelCheckpoint(filepath='best.inceptionBottleneck.hdf5',
                                   verbose=1,
                                   save_best_only=True)

    early_stopping = EarlyStopping(monitor='val_loss',
                                   verbose=1,
                                   patience=20)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  verbose=1,
                                  factor=0.1,
                                  patience=10, min_lr=0.0001)

    normal_input = Input(shape=train_x.shape[1:])
    squared_input = Input(shape=train_x2.shape[1:])
    sin_input = Input(shape=sin_train_x.shape[1:])

    normal_model = Dense(1000)(normal_input)
    normal_model = BatchNormalization()(normal_model)
    normal_model = Activation('relu')(normal_model)
    normal_model = Dropout(0.3)(normal_model)


    squared_model = Dense(1000)(squared_input)
    squared_model = BatchNormalization()(squared_model)
    squared_model = Activation('relu')(squared_model)
    squared_model = Dropout(0.3)(squared_model)


    sin_model = Dense(1000)(sin_input)
    sin_model = BatchNormalization()(sin_model)
    sin_model = Activation('relu')(sin_model)
    sin_model = Dropout(0.3)(sin_model)



    concat = concatenate([normal_model, squared_model, sin_model])


    concat = Dense(1024)(concat)
    concat = BatchNormalization()(concat)
    concat = Activation('relu')(concat)
    concat = Dropout(0.3)(concat)
    concat = Dense(512)(concat)

    output = Dense(152,activation='linear')(concat)

    inceptionV3Bottleneck = Model(inputs=[normal_input, squared_input, sin_input],
                                  outputs=[output])

    model_json = inceptionV3Bottleneck.to_json()
    with open("inceptionBottleneck.json", "w") as json_file:
        json_file.write(model_json)


    print(inceptionV3Bottleneck.summary())

    inceptionV3Bottleneck.compile(loss='mse',
                                  optimizer='nadam',
                                  metrics=['acc'])

    plot_model(inceptionV3Bottleneck, to_file='inceptionBottleneck.png')
    inceptionV3Bottleneck.fit([train_x,train_x2,sin_train_x],
                train_y,
                validation_data=([test_x,test_x2,sin_test_x],test_y),
                callbacks=[checkpointer, tbCallBack, early_stopping, reduce_lr],
                epochs=500,
                batch_size=100,
                verbose=1,
                shuffle=True)


def train_inception_v3_with_extra_layers(layers_to_train):

    train_x = dataset["train_x"]
    train_y = dataset["train_y"]/299
    test_x = dataset["test_x"]
    test_y = dataset["test_y"]/299

    tbCallBack = TensorBoard(log_dir='./inception' + str(layers_to_train) + 'layers',
                             histogram_freq=0,
                             write_graph=True,
                             write_images=True)


    checkpointer = ModelCheckpoint(filepath='best.inception' +
                                   str(layers_to_train) + 'layers.hdf5',
                                   verbose=1,
                                   save_best_only=True)

    early_stopping = EarlyStopping(monitor='val_loss',
                                   verbose=1,
                                   patience=20)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  verbose=1,
                                  factor=0.1,
                                  patience=10, min_lr=0.0001)

    base_model = InceptionV3(weights='imagenet',
                             input_shape=(299,299,3),
                             include_top=False)



    inputs = base_model.output
    model = GlobalAveragePooling2D()(inputs)
    output = Dense(152,activation='linear')(model)


    fm = Model(base_model.input, outputs=output)

    for layer in fm.layers[:layers_to_train]:
        layer.trainable = False
    for layer in fm.layers[layers_to_train:]:
        layer.trainable = True

    fm.compile(loss='mse', optimizer="adam" ,metrics=['acc'])

    model_json = fm.to_json()
    with open('inception' + str(layers_to_train) + 'layers.json', "w") as json_file:
        json_file.write(model_json)

    print(fm.summary())

    plot_model(fm, to_file='inception' + str(layers_to_train) + 'layers.png')

    fm.fit(train_x, train_y,
           validation_data=(test_x,test_y),
           callbacks=[checkpointer,tbCallBack,early_stopping],
           epochs=200, batch_size=10, verbose=1, shuffle=True)


def train_resnet_with_extra_layers(layers_to_train):

    train_x = dataset["train_x"]
    train_y = dataset["train_y"]/299
    test_x = dataset["test_x"]
    test_y = dataset["test_y"]/299

    tbCallBack = TensorBoard(log_dir='./resnet' + str(layers_to_train) + 'layers',
                             histogram_freq=0,
                             write_graph=True,
                             write_images=True)


    checkpointer = ModelCheckpoint(filepath='best.resnet' +
                                   str(layers_to_train) + 'layers.hdf5',
                                   verbose=1,
                                   save_best_only=True)

    early_stopping = EarlyStopping(monitor='val_loss',
                                   verbose=1,
                                   patience=20)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  verbose=1,
                                  factor=0.1,
                                  patience=10, min_lr=0.0001)

    base_model = ResNet50(weights='imagenet',
                          input_shape=(299,299,3),
                          include_top=False)



    inputs = base_model.output
    model = GlobalAveragePooling2D()(inputs)
    output = Dense(152,activation='linear')(model)


    fm = Model(base_model.input, outputs=output)

    for layer in fm.layers[:layers_to_train]:
        layer.trainable = False
    for layer in fm.layers[layers_to_train:]:
        layer.trainable = True

    fm.compile(loss='mse', optimizer="adam" ,metrics=['acc'])

    model_json = fm.to_json()
    with open('resnet' + str(layers_to_train) + 'layers.json', "w") as json_file:
        json_file.write(model_json)

    print(fm.summary())

    plot_model(fm, to_file='resnet' + str(layers_to_train) + 'layers.png')

    fm.fit(train_x, train_y,
           validation_data=(test_x,test_y),
           callbacks=[checkpointer,
                      tbCallBack,
                      early_stopping,
                      reduce_lr],
           epochs=200, batch_size=10, verbose=1, shuffle=True)


def convlayer(model, filters, kernel_size, dropout):
    m = Conv2D(filters=filters,
               kernel_size=kernel_size,
               padding="same")(model)
    m = BatchNormalization()(m)
    m = Activation('relu')(m)
    m = Dropout(dropout)(m)
    return m

def own_model():

    train_x = dataset["train_x"]
    train_y = dataset["train_y"]/299
    test_x = dataset["test_x"]
    test_y = dataset["test_y"]/299

    tbCallBack = TensorBoard(log_dir='./mymodel',
                             histogram_freq=0,  
                             write_graph=True,
                             write_images=True)


    checkpointer = ModelCheckpoint(filepath='best.mymodel.hdf5', 
                                   verbose=1,
                                   save_best_only=True)

    early_stopping = EarlyStopping(monitor='val_loss',
                                   verbose=1,
                                   patience=20)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                  verbose=1,
                                  factor=0.1,
                                  patience=10, min_lr=0.0001)


    inputs = Input(shape=(299,299,3))

    model1 = convlayer(inputs, 64, 6, 0.3)
    model1 = convlayer(model1, 64, 6, 0.3)
    model1 = MaxPooling2D(pool_size=2, strides=2)(model1)
    model1 = convlayer(model1, 128, 6, 0.3)
    model1 = convlayer(model1, 128, 6, 0.3)
    model1 = MaxPooling2D(pool_size=2, strides=2)(model1)
    model1 = convlayer(model1, 256, 6, 0.3)
    model1 = convlayer(model1, 256, 6, 0.3)
    model1 = MaxPooling2D(pool_size=2, strides=2)(model1)



    model2 = convlayer(inputs, 64, 3, 0.3)
    model2 = convlayer(model2, 64, 3, 0.3)
    model2 = MaxPooling2D(pool_size=2, strides=2)(model2)
    model2 = convlayer(model2, 128, 3, 0.3)
    model2 = convlayer(model2, 128, 3, 0.3)
    model2 = MaxPooling2D(pool_size=2, strides=2)(model2)
    model2 = convlayer(model2, 256, 3, 0.3)
    model2 = convlayer(model2, 256, 3, 0.3)
    model2 = MaxPooling2D(pool_size=2, strides=2)(model2)


    model = concatenate([model1,model2])
    model = convlayer(model, 512, 3, 0.3)
    model = GlobalAveragePooling2D()(model)
    model = Dense(1024,activation='relu')(model)
    model = Dropout(0.3)(model)
    model = Dense(512,activation='relu')(model)
    model = Dropout(0.3)(model)

    output = Dense(152,activation='linear')(model)



    fm = Model(inputs=inputs, outputs=output)

    fm.compile(loss='mse', optimizer="adam" ,metrics=['acc'])

    model_json = fm.to_json()
    with open("mymodel.json", "w") as json_file:
        json_file.write(model_json)

    print(fm.summary())

    plot_model(fm, to_file='mymodel.png')

    fm.fit(train_x, train_y,
           validation_data=(test_x,test_y),
           callbacks=[checkpointer,
                      tbCallBack,
                      early_stopping,
                      reduce_lr],
           epochs=200, batch_size=10, verbose=1, shuffle=True)


def main():
    train_inception_v3_bottleneck()
    train_inception_v3_with_extra_layers(249)
    train_inception_v3_with_extra_layers(197)
    train_resnet_with_extra_layers(173)
    train_resnet_with_extra_layers(129)
    own_model()


if __name__ == "__main__":
    main()
