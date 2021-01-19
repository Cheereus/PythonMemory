from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.Qt import QUrl
import sys
import time
import sip


# 建立线程间通讯
class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)


# 建立时钟线程
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
        self._fullscreen = False
        self.play_type = 0
        self.play_type_text = ['队列循环播放', '分时循环播放']
        self.current_video = 0

        # 队列循环
        self.file_list = []
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        self.start_time = '09:00:00'
        self.stop_time = '16:00:00'

        # 分时循环
        self.sep_file_list = {}
        self.file_label_list = {}
        self.start_label_list = {}
        self.start_btn_list = {}
        self.start_time_list = {}
        self.stop_label_list = {}
        self.stop_btn_list = {}
        self.stop_time_list = {}

        self.running = False

        # 布局
        self.main_widget = QWidget(self)
        mlayout = QHBoxLayout(self.main_widget)
        self.llayout = QFormLayout()
        rlayout = QVBoxLayout()

        self.addForm(self.llayout)  # 表单初始化
        addVideo(self, rlayout)  # 视频播放窗口初始化
        self.addMenu()  # 菜单栏初始化

        # 窗口初始化
        mlayout.addLayout(self.llayout)
        mlayout.addLayout(rlayout)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # 监听线程初始化
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
        self.opt_menu.addAction('开始运行', self.startRunning)
        self.opt_menu.addAction('停止运行', self.stopRunning)
        self.menuBar().addMenu(self.opt_menu)

    def mouseDoubleClickEvent(self, event):
        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.running:
            self._fullscreen = not self._fullscreen
            print('setFullScreen', self._fullscreen)
            self.video_widget.setFullScreen(self._fullscreen)

    # 由时钟线程触发的播放状态管理
    def changeStatus(self):
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        if self.play_type == 0:
            print(self.start_time, self.now_time, self.stop_time, self.running)
            if self.start_time < self.now_time < self.stop_time and self.running:

                if self.player.state() == QMediaPlayer.StoppedState:
                    print('running', self.player.state(), self.current_video)
                    self.current_video += 1
                    self.playList()

            else:
                self._fullscreen = False
                self.video_widget.setFullScreen(self._fullscreen)
                self.player.stop()
                self.current_video = 0
        else:
            video_to_play = self.checkTime()
            if video_to_play > 0 and self.running:
                if self.player.state() == QMediaPlayer.StoppedState:
                    self.playSep()
                    print('running', self.player.state(), self.current_video)
                pass
            else:
                self._fullscreen = False
                self.video_widget.setFullScreen(self._fullscreen)
                self.player.stop()
                self.current_video = 0

    # 导入视频
    def loadVideo(self):
        file_name = QFileDialog.getOpenFileName()[0]
        if len(file_name) > 0:
            if self.play_type == 0:
                self.file_list.append(file_name)
                self.file_label.setText('已导入视频\n' + '\n'.join(self.file_list))
            else:
                self.sep_file_label.setText('已导入视频\n')
                self.idx += 1
                self.sep_file_list[self.idx] = file_name
                self.file_label_list[self.idx] = QLabel('\n' + file_name)
                self.llayout.addRow(self.file_label_list[self.idx])
                self.start_label_list[self.idx] = QLabel('开始时间')
                self.start_btn_list[self.idx] = QTimeEdit(QtCore.QTime.fromString('00:00:00'))
                self.start_btn_list[self.idx].setObjectName(str(self.idx))
                self.start_btn_list[self.idx].setFixedWidth(200)
                self.start_time_list[self.idx] = '00:00:00'
                self.start_btn_list[self.idx].timeChanged.connect(self.start_time_list_change)
                self.llayout.addRow(self.start_label_list[self.idx], self.start_btn_list[self.idx])

                self.stop_label_list[self.idx] = QLabel('停止时间')
                self.stop_btn_list[self.idx] = QTimeEdit(QtCore.QTime.fromString('00:00:00'))
                self.stop_btn_list[self.idx].setObjectName(str(self.idx))
                self.stop_btn_list[self.idx].setFixedWidth(200)
                self.stop_time_list[self.idx] = '00:00:00'
                self.stop_btn_list[self.idx].timeChanged.connect(self.stop_time_list_change)
                self.llayout.addRow(self.stop_label_list[self.idx], self.stop_btn_list[self.idx])
            self.start_play_btn.setDisabled(False)

    # 清除已导入的所有视频
    def clearVideo(self):
        self.file_label.setText('请按顺序导入视频')
        self.sep_file_label.setText('请按顺序导入视频')
        self.file_list = []

        for i in range(self.idx):
            self.llayout.removeWidget(self.file_label_list[i+1])
            sip.delete(self.file_label_list[i+1])
            self.llayout.removeWidget(self.start_label_list[i+1])
            sip.delete(self.start_label_list[i+1])
            self.llayout.removeWidget(self.start_btn_list[i+1])
            sip.delete(self.start_btn_list[i+1])
            self.llayout.removeWidget(self.stop_label_list[i+1])
            sip.delete(self.stop_label_list[i+1])
            self.llayout.removeWidget(self.stop_btn_list[i+1])
            sip.delete(self.stop_btn_list[i+1])

        self.sep_file_list = {}
        self.file_label_list = {}
        self.start_label_list = {}
        self.start_btn_list = {}
        self.start_time_list = {}
        self.stop_label_list = {}
        self.stop_btn_list = {}
        self.stop_time_list = {}

        self.idx = 0
        self.current_video = 0
        self.running = False

    # 播放视频
    def playVideo(self, video):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video)))  # 选取视频文件
        self.player.play()

    # 队列循环播放
    def playList(self):
        if self.current_video == len(self.file_list):
            self.current_video = 0
        self.playVideo(self.file_list[self.current_video])

    # 分时循环播放
    # 根据时间计算当前应该播放的视频，如果没有则返回 0
    def checkTime(self):
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        video_to_play = 0
        for i in range(self.idx):
            if self.start_time_list[i+1] < self.now_time < self.stop_time_list[i+1]:
                video_to_play = i + 1

        return video_to_play

    # 分时循环播放
    def playSep(self):
        self.current_video = self.checkTime()
        if self.current_video > 0:
            self.playVideo(self.sep_file_list[self.current_video])

    # 开始运行
    def startRunning(self):
        self.running = True
        self.stop_play_btn.setDisabled(False)
        self.start_play_btn.setDisabled(True)
        if self.play_type == 0:
            self.playList()
        else:
            self.playSep()

    # 停止运行
    def stopRunning(self):
        self.running = False
        self.stop_play_btn.setDisabled(True)
        self.start_play_btn.setDisabled(False)

    # 切换播放模式
    def toggle_play_type(self):
        self.play_type = 0 if self.play_type else 1
        self.type_label.setText('当前模式：' + self.play_type_text[self.play_type])
        if self.play_type == 1:
            self.file_label.setVisible(False)
            self.set_time_label.setVisible(False)
            self.start_time_label.setVisible(False)
            self.start_time_btn.setVisible(False)
            self.stop_time_label.setVisible(False)
            self.stop_time_btn.setVisible(False)

            self.sep_file_label.setVisible(True)
            for i in range(self.idx):
                self.file_label_list[i+1].setVisible(True)
                self.start_label_list[i+1].setVisible(True)
                self.start_btn_list[i+1].setVisible(True)
                self.stop_label_list[i+1].setVisible(True)
                self.stop_btn_list[i+1].setVisible(True)

        else:
            self.file_label.setVisible(True)
            self.set_time_label.setVisible(True)
            self.start_time_label.setVisible(True)
            self.start_time_btn.setVisible(True)
            self.stop_time_label.setVisible(True)
            self.stop_time_btn.setVisible(True)

            self.sep_file_label.setVisible(False)
            for i in range(self.idx):
                self.file_label_list[i+1].setVisible(False)
                self.start_label_list[i+1].setVisible(False)
                self.start_btn_list[i+1].setVisible(False)
                self.stop_label_list[i+1].setVisible(False)
                self.stop_btn_list[i+1].setVisible(False)

    # 队列循环播放的时间设置
    def start_time_change(self, value):
        self.start_time = QtCore.QTime.toString(value)

    def stop_time_change(self, value):
        self.stop_time = QtCore.QTime.toString(value)

    # 分时循环播放的时间设置
    def start_time_list_change(self):
        v_id = int(self.sender().objectName())
        self.start_time_list[v_id] = QtCore.QTime.toString(self.start_btn_list[v_id].time())

    def stop_time_list_change(self):
        v_id = int(self.sender().objectName())
        self.stop_time_list[v_id] = QtCore.QTime.toString(self.stop_btn_list[v_id].time())

    # 表单初始化
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
        self.sep_file_label = QLabel('请按顺序导入视频')
        self.sep_file_label.setFixedWidth(300)
        self.sep_file_label.setVisible(False)
        llayout.addRow(self.sep_file_label)

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

        self.start_play_btn = QPushButton('开始运行')
        self.start_play_btn.clicked.connect(self.startRunning)
        self.start_play_btn.setFixedWidth(340)
        self.start_play_btn.setDisabled(True)
        llayout.addRow(self.start_play_btn)
        self.stop_play_btn = QPushButton('停止运行')
        self.stop_play_btn.clicked.connect(self.stopRunning)
        self.stop_play_btn.setFixedWidth(340)
        self.stop_play_btn.setDisabled(True)
        llayout.addRow(self.stop_play_btn)


# 视频控件初始化
def addVideo(self, rlayout):
    self.player = QMediaPlayer()
    self.video_widget = QVideoWidget()
    self.video_widget.setStyleSheet("background-color:black;")

    rlayout.addWidget(self.video_widget)
    self.video_widget.show()
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
