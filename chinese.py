from abc import ABC

import numpy as np
import csv
import os
import cv2
import matplotlib.image as img
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, layers

tf.random.set_seed(22)
np.random.seed(22)

g = os.walk("chineseminst/train_data/")
for path, d, file_list in g:
    pass
train_data = []
train_label = []
for i in range(len(file_list)):
    img_temp = img.imread(r'chineseminst/train_data/%s' % file_list[i])
    sp = file_list[i].split('_')
    label = sp[3].split('.')
    temp = [img_temp, int(label[0])]
    train_data.append(np.array([np.dot(img_temp, [0.299, 0.587, 0.114])]).transpose())
    train_label.append(int(label[0]))


train_data = np.array(train_data)
train_label = np.array(train_label)
sf_idx = list(range(len(train_data)))
np.random.shuffle(sf_idx)
train_data = train_data[sf_idx]
train_label = train_label[sf_idx]

g = os.walk("chineseminst/test_data/")
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
        batch_label.append(int(item[1] - 1))
        if len(batch_data) == batch_size:
            yield batch_data, batch_label
            batch_data = []
            batch_label = []


class MyModel(tf.keras.Model, ABC):

    def __init__(self):
        super(MyModel, self).__init__()
        self.CNN = Sequential([
            tf.keras.layers.Conv2D(filters=1, kernel_size=5, activation='sigmoid'),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Conv2D(filters=1, kernel_size=5, activation='sigmoid'),
            tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation='sigmoid'),
            tf.keras.layers.Dense(84, activation='sigmoid'),
            tf.keras.layers.Dense(15, activation='softmax')
        ])

    def call(self, inputs, training=False):
        x = self.CNN(inputs)
        return x


train_db = tf.data.Dataset.from_tensor_slices((train_data, train_label))
train_db = train_db.batch(100)

model = MyModel()
model.build(input_shape=(100, 64, 64, 1))
model.summary()

lr, num_epochs = 0.01, 5
optimizer = tf.optimizers.SGD(lr=lr)

for i in range(num_epochs):
    train_iter = ImgLoader(train_data, batch_size=100)
    test_iter = ImgLoader(test_data, batch_size=100)

    for step, (X, y) in enumerate(train_db):

        with tf.GradientTape() as tape:
            y_pred = model(X)
            loss = tf.losses.sparse_categorical_crossentropy(y, y_pred)
            loss_mean = tf.reduce_mean(loss)
        print(y, tf.math.argmax(y_pred, axis=1))
        print(loss)

        grads = tape.gradient(loss_mean, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
        print(loss_mean)


