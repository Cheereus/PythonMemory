from abc import ABC

import numpy as np
import csv
import os
import cv2
import matplotlib.image as img
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, layers

batch_size = 100

g = os.walk("../chineseminst/train_data/")
for path, d, file_list in g:
    pass
train_data = []
train_label = []
for i in range(len(file_list)):
    img_temp = img.imread(r'chineseminst/train_data/%s' % file_list[i])
    sp = file_list[i].split('_')
    label = sp[3].split('.')
    # temp = [img_temp, int(label[0])]
    train_data.append(np.array([np.dot(img_temp, [0.299, 0.587, 0.114]) / 255]).transpose())
    # if i == 0:
    #     np.savetxt('out.csv', train_data[0].transpose()[0], delimiter=',')
    #     print(train_data[0])
    train_label.append(int(label[0]) - 1)


train_data = np.array(train_data)
train_label = np.array(train_label)
sf_idx = list(range(len(train_data)))
np.random.shuffle(sf_idx)
train_data = train_data[sf_idx]
train_label = train_label[sf_idx]


def accuracy(predict_labels, true_labels):
    if len(predict_labels) != len(true_labels):
        print('Label Length Error')
        return 0
    label_length = len(predict_labels)
    correct = 0
    for i in range(label_length):
        if predict_labels[i] == true_labels[i]:
            correct += 1
    return correct / label_length


g = os.walk("../chineseminst/test_data/")
for path, d, file_list in g:
    pass
test_data = []
for i in range(len(file_list)):
    img_temp = img.imread(r'chineseminst/test_data/%s' % file_list[i])
    sp = file_list[i].split('_')
    label = sp[3].split('.')
    temp = [img_temp, int(label[0])]
    test_data.append(temp)


def ImgLoader(data, batch_size, shuffle=True):
    data = np.array(data)
    if shuffle:
        sf_idx = list(range(len(data)))
        np.random.shuffle(sf_idx)
        data = data[sf_idx]
    batch_data = []
    batch_label = []
    for item in data:
        batch_data.append(np.array([np.dot(item[0][..., :3], [0.299, 0.587, 0.114])]).transpose())
        batch_label.append(int(item[1]))
        if len(batch_data) == batch_size:
            yield batch_data, batch_label
            batch_data = []
            batch_label = []


class MyModel(tf.keras.Model, ABC):

    def __init__(self):
        super(MyModel, self).__init__()
        self.CNN = Sequential([
            tf.keras.layers.Conv2D(filters=6, kernel_size=3, activation=tf.nn.leaky_relu),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=16, kernel_size=3, activation=tf.nn.leaky_relu),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation=tf.nn.sigmoid),
            tf.keras.layers.Dense(84, activation=tf.nn.sigmoid),
            tf.keras.layers.Dense(15),
            tf.keras.layers.Activation('softmax')
        ])

    def call(self, inputs, training=False):
        x = self.CNN(inputs)
        return x


train_db = tf.data.Dataset.from_tensor_slices((train_data, train_label))
train_db = train_db.batch(batch_size)

model = MyModel()
model.build(input_shape=(batch_size, 64, 64, 1))
model.summary()

lr, num_epochs = 0.9, 50
optimizer = tf.optimizers.SGD(lr=lr)

for i in range(num_epochs):
    train_iter = ImgLoader(train_data, batch_size=batch_size)
    test_iter = ImgLoader(test_data, batch_size=batch_size)

    for step, (X, y) in enumerate(train_db):

        # print(y[10])
        with tf.GradientTape() as tape:
            y_pred = model(X)
            max_index = tf.argmax(y_pred, axis=1)
            loss = tf.losses.sparse_categorical_crossentropy(y, y_pred)
            loss_mean = tf.reduce_mean(loss)
        # print(max_index)
        print(loss_mean)
        print(accuracy(y.numpy(), max_index))

        grads = tape.gradient(loss_mean, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))


