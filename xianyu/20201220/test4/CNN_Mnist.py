import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import numpy as np
import matplotlib.image as img  # img 用于读取图片
import matplotlib.pyplot as plt  # plt 用于显示图片

# 设置随机数种子，确保每次运行结果一致
np.random.seed(10)
tf.random.set_seed(10)

# 加载数据集并进行预处理
(x_Train, y_Train), (x_Test, y_Test) = tf.keras.datasets.mnist.load_data()
x_Train4D = x_Train.reshape(x_Train.shape[0], 28, 28, 1).astype('float32')
x_Test4D = x_Test.reshape(x_Test.shape[0], 28, 28, 1).astype('float32')
x_Train4D_normalize = x_Train4D / 255
x_Test4D_normalize = x_Test4D / 255
y_Train = to_categorical(y_Train)
y_Test = to_categorical(y_Test)

# 模型构建
model = Sequential()
model.add(Conv2D(filters=16,
                 kernel_size=(5, 5),
                 padding='same',
                 input_shape=(28, 28, 1),
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=36,
                 kernel_size=(5, 5),
                 padding='same',
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

# 使用交叉熵损失函数、adam优化器、准确率指标
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
train_history = model.fit(x=x_Train4D_normalize,
                          y=y_Train, validation_split=0.2,
                          epochs=20, batch_size=300, verbose=2)
scores = model.evaluate(x_Test4D_normalize, y_Test)
print(scores[1])

# 读取自定义图片进行测试
# 可自行使用长宽为 28*28 的图片进行测试，修改文件路径即可
img_temp = img.imread('8.png')
r, g, b = [img_temp[:, :, i] for i in range(3)]
img_gray = r * 0.299 + g * 0.587 + b * 0.114
img_gray = (img_gray - img_gray.min()) * (1 / (img_gray.max() - img_gray.min()))
img_gray = img_gray.reshape(1, 28, 28, 1)

# 展示灰度化后的图片
# plt.imshow(img_gray, cmap='gray')
# plt.show()

# 预测并输出各类概率，并输出概率最大的类别
label_pred = model.predict([img_gray])
print(label_pred)
print(np.argmax(label_pred))
