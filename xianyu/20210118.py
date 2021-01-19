from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QUrl
import sys
import time


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)


class VideoTimer(QtCore.QThread):

    def __init__(self, frequent=1):
        QtCore.QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()

    def run(self):
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("视频自动播放")

        # 一些全局变量
        self.idx = 0
        self.file_list = []
        self._fullscreen = False
        self.current_video = 0
        self.play_type = 0
        self.play_type_text = ['队列循环播放', '分时循环播放']
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        self.start_time = '09:00:00'
        self.stop_time = '16:00:00'

        self.running = False

        # self.center()
        # 布局
        self.main_widget = QWidget(self)
        mlayout = QHBoxLayout(self.main_widget)
        llayout = QFormLayout()
        rlayout = QVBoxLayout()

        self.addForm(llayout)  # 表单初始化
        addTable(self, rlayout)  # 表格初始化
        self.addMenu()  # 菜单栏初始化

        # 窗口初始化
        mlayout.addLayout(llayout)
        mlayout.addLayout(rlayout)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.changeStatus)
        self.timer.start()

    # 居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 添加菜单
    def addMenu(self):
        self.file_menu = QMenu('视频', self)
        self.file_menu.addAction('导入视频', self.loadVideo)
        self.file_menu.addAction('清空视频', self.clearVideo)
        self.menuBar().addMenu(self.file_menu)

        self.opt_menu = QMenu('运行', self)
        self.opt_menu.addAction('开始运行', self.playList)
        self.opt_menu.addAction('停止运行', self.stopRunning)
        self.menuBar().addMenu(self.opt_menu)

    def mouseDoubleClickEvent(self, event):
        self.toggle_fullscreen()
        # self.player.play()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        print('setFullScreen', self._fullscreen)
        self.video_widget.setFullScreen(self._fullscreen)

    def changeStatus(self):
        self.idx += 1
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        if self.start_time < self.now_time < self.stop_time and self.running:

            if self.player.state() == QMediaPlayer.StoppedState:
                print('running', self.player.state(), self.current_video)
                self.current_video += 1
                self.playList()

        else:
            self._fullscreen = False
            self.video_widget.setFullScreen(self._fullscreen)
            self.player.stop()

    def loadVideo(self):
        self.file_list.append(QFileDialog.getOpenFileName()[0])
        self.file_label.setText('已导入视频\n' + '\n'.join(self.file_list))

    def clearVideo(self):
        self.file_label.setText('请按顺序导入视频')
        self.file_list = []
        self.running = False

    def stopRunning(self):
        self.running = False

    def playVideo(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_list[0])))  # 选取视频文件
        self.player.play()

    def playList(self):
        self.running = True
        if self.current_video == len(self.file_list):
            self.current_video = 0
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_list[self.current_video])))
        self.player.play()

    def toggle_play_type(self):
        self.play_type = 0 if self.play_type else 1
        self.type_label.setText('当前模式：' + self.play_type_text[self.play_type])

    def start_time_change(self, value):
        self.start_time = QtCore.QTime.toString(value)

    def stop_time_change(self, value):
        self.start_time = QtCore.QTime.toString(value)

    def addForm(self, llayout):
        # llayout.setLabelAlignment(QtCore.Qt.AlignRight)  # 标签右对齐
        self.type_label = QLabel('当前模式：' + self.play_type_text[self.play_type])
        self.type_btn = QPushButton('切换')
        self.type_btn.setFixedWidth(200)
        self.type_btn.clicked.connect(self.toggle_play_type)
        llayout.addRow(self.type_label, self.type_btn)

        self.file_label = QLabel('请按顺序导入视频')
        self.file_label.setFixedWidth(300)
        llayout.addRow(self.file_label)

        self.set_time_label = QLabel('\n设置播放时间段')
        llayout.addRow(self.set_time_label)

        self.start_time_label = QLabel('开始时间')
        self.start_time_btn = QTimeEdit(QtCore.QTime.fromString(self.start_time))
        self.start_time_btn.setFixedWidth(200)
        self.start_time_btn.timeChanged.connect(self.start_time_change)
        llayout.addRow(self.start_time_label, self.start_time_btn)

        self.stop_time_label = QLabel('停止时间')
        self.stop_time_btn = QTimeEdit(QtCore.QTime.fromString(self.stop_time))
        self.stop_time_btn.setFixedWidth(200)
        self.stop_time_btn.timeChanged.connect(self.stop_time_change)
        llayout.addRow(self.stop_time_label, self.stop_time_btn)


def addTable(self, rlayout):
    self.player = QMediaPlayer()
    self.video_widget = QVideoWidget()
    self.video_widget.show()
    rlayout.addWidget(self.video_widget)
    self.player.setVideoOutput(self.video_widget)  # 视频输出的widget
    QtWidgets.QShortcut(
        QtGui.QKeySequence(QtCore.Qt.Key_Escape),
        self,
        self.toggle_fullscreen,
        context=QtCore.Qt.ApplicationShortcut
    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.showMaximized()
    sys.exit(app.exec_())
