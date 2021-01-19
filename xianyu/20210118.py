from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QUrl
import sys


class VideoWidget(QVideoWidget):
    doubleClickedItem = QtCore.pyqtSignal(str)  # 创建双击信号

    def __init__(self, parent=None):
        super(QVideoWidget, self).__init__(parent)
    #
    # def mouseDoubleClickEvent(self, event):
    #     self.doubleClickedItem.emit("double clicked")
    #     print('removeFullScreen')
    #     self.setFullScreen(False)


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("视频自动播放")

        # 一些全局变量
        self.file_list = []
        self._fullscreen = False

        # self.center()
        # 布局
        self.main_widget = QWidget(self)
        mlayout = QHBoxLayout(self.main_widget)
        llayout = QFormLayout()
        rlayout = QVBoxLayout()

        addForm(self, llayout)  # 表单初始化
        addTable(self, rlayout)  # 表格初始化
        self.addMenu()  # 菜单栏初始化

        # 窗口初始化
        mlayout.addLayout(llayout)
        mlayout.addLayout(rlayout)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    # 居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 添加菜单
    def addMenu(self):
        self.file_menu = QMenu('操作', self)
        self.file_menu.addAction('导入视频', lambda: loadVideo(self))
        self.file_menu.addAction('开始播放', lambda: playVideo(self))
        self.menuBar().addMenu(self.file_menu)

    def mouseDoubleClickEvent(self, event):
        self.toggle_fullscreen()
        # self.player.play()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        print('setFullScreen', self._fullscreen)
        self.video_widget.setFullScreen(self._fullscreen)


def loadVideo(self):
    self.file_list.append(QFileDialog.getOpenFileName()[0])


def playVideo(self):
    self.player.setVideoOutput(self.video_widget)  # 视频输出的widget
    QtWidgets.QShortcut(
        QtGui.QKeySequence(QtCore.Qt.Key_Escape),
        self,
        self.toggle_fullscreen,
        context=QtCore.Qt.ApplicationShortcut
    )
    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_list[0])))  # 选取视频文件
    self.player.play()
    # self.video_widget.setFullScreen(True)


def addForm(self, llayout):
    print('addForm')


def addTable(self, rlayout):
    self.player = QMediaPlayer()
    self.video_widget = QVideoWidget()
    self.video_widget.show()
    rlayout.addWidget(self.video_widget)
    # print('addTable')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.showMaximized()
    sys.exit(app.exec_())
