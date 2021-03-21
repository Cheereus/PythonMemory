from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.Qt import QUrl
import sys
import time
import sip
import os
from pptx_tools import utils
import fitz
import datetime
from win32com.client import gencache
from win32com.client import constants, gencache


# 将PPT转为图片
def get_ppt_img(filePath, png_folder):
    utils.save_pptx_as_png(png_folder, filePath, overwrite_folder=True)
    return True


def word_to_pdf(wordPath, pdfPath):
    """
    word转pdf
    :param wordPath: word文件路径
    :param pdfPath:  生成pdf文件路径
    """
    word = gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(wordPath, ReadOnly=1)
    doc.ExportAsFixedFormat(pdfPath,
                            constants.wdExportFormatPDF,
                            Item=constants.wdExportDocumentWithMarkup,
                            CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
    word.Quit(constants.wdDoNotSaveChanges)


def get_pdf_img(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)

    return True


# 建立线程间通讯
class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)


# 建立视频时钟线程
class ListenTimer(QtCore.QThread):

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


# 建立视频时钟线程
class ImageTimer(QtCore.QThread):

    def __init__(self, frequent=1):
        QtCore.QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()

    def run(self):
        while True:
            if not self.stopped:
                self.timeSignal.signal.emit("1")
                time.sleep(self.frequent)

    def stop(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped


# 视频控件初始化
def addVideo(self, rlayout):
    self.player = QMediaPlayer()
    self.video_widget = QVideoWidget()
    # self.video_widget.setStyleSheet("background-color:black;")

    rlayout.addWidget(self.video_widget)
    self.video_widget.hide()
    self.player.setVideoOutput(self.video_widget)  # 视频输出的widget
    QtWidgets.QShortcut(
        QtGui.QKeySequence(QtCore.Qt.Key_Escape),
        self,
        self.toggle_fullscreen,
        context=QtCore.Qt.ApplicationShortcut
    )


def toggleWidgetsVisible(widgets, visible=True):
    for widget in widgets:
        widget.setVisible(visible)


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("视频自动播放")

        # 一些全局变量
        self.idx = 0
        self.image_idx = 0
        self._fullscreen = False
        self.file_type = 0
        self.file_type_list = ['视频', 'PPT', 'Word', 'PDF']
        self.play_type = 0
        self.play_type_text = ['队列循环播放', '分时循环播放']
        self.current_file = 0

        # 队列循环
        self.file_list = []
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        self.start_time = '00:00:00'
        self.stop_time = '23:59:59'
        self.interval_time = 2

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
        self.imagePlaying = False

        # 布局
        self.main_widget = QWidget(self)
        mlayout = QHBoxLayout(self.main_widget)
        self.llayout = QFormLayout()
        self.rlayout = QVBoxLayout()
        # self.rlayout.setStyleSheet("background-color:black;")

        # 表单初始化
        self. addForm(self.llayout)

        # 窗口初始化
        mlayout.addLayout(self.llayout)
        mlayout.addLayout(self.rlayout)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # 视频播放窗口初始化
        addVideo(self, self.rlayout)

        # 图片展示窗口初始化
        # self.main_widget.showMinimized()
        # img = QtGui.QPixmap('data/ppt_img/幻灯片1.PNG').scaled(self.image_widget.width(), self.image_widget.height())
        # self.image_widget.setPixmap(img)

        # 初始化菜单
        self.file_menu = QMenu('视频', self)
        self.file_menu.addAction('导入视频', self.loadVideo)
        self.file_menu.addAction('清空视频', self.clearFiles)
        self.menuBar().addMenu(self.file_menu)

        self.file_menu = QMenu('PPT', self)
        self.file_menu.addAction('导入PPT', self.loadPPT)
        self.file_menu.addAction('清空PPT', self.clearFiles)
        self.menuBar().addMenu(self.file_menu)

        self.file_menu = QMenu('Word', self)
        self.file_menu.addAction('导入Word', self.loadWord)
        self.file_menu.addAction('清空Word', self.clearFiles)
        self.menuBar().addMenu(self.file_menu)

        self.file_menu = QMenu('PDF', self)
        self.file_menu.addAction('导入PDF', self.loadPDF)
        self.file_menu.addAction('清空PDF', self.clearFiles)
        self.menuBar().addMenu(self.file_menu)

        self.opt_menu = QMenu('运行', self)
        self.opt_menu.addAction('开始运行', self.startRunning)
        self.opt_menu.addAction('停止运行', self.stopRunning)
        self.menuBar().addMenu(self.opt_menu)

        # self.menuBar().hide()

    def loadSepFile(self, fileName):
        if len(fileName) > 0:
            if self.play_type == 0:
                self.file_list.append(fileName)
                self.file_label.setText('已导入' + self.file_type_list[self.file_type] + '\n' + '\n'.join(self.file_list))
            else:
                self.sep_file_label.setText('已导入' + self.file_type_list[self.file_type] + '\n')
                self.idx += 1
                self.sep_file_list[self.idx] = fileName
                self.file_label_list[self.idx] = QLabel('\n' + fileName)
                self.file_label_list[self.idx].setFixedWidth(340)
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

    def loadVideo(self):
        if self.file_type != 0:
            self.file_type = 0
            self.clearFiles()
        file_name = QFileDialog.getOpenFileName()[0]
        self.loadSepFile(file_name)

    def loadPPT(self):
        if self.file_type != 1:
            self.file_type = 1
            self.clearFiles()
        file_path = QFileDialog.getOpenFileName()[0]
        if len(file_path) > 0:
            file_path = file_path.replace('/', '\\')
            file_name = file_path.split('\\')[-1].split('.')[0]
            # print('\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name)
            file_folder = '\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name
            get_ppt_img(file_path, file_folder)
            self.loadSepFile(file_folder)

    def loadWord(self):
        if self.file_type != 2:
            self.file_type = 2
            self.clearFiles()
        file_path = QFileDialog.getOpenFileName()[0]
        if len(file_path) > 0:
            file_path = file_path.replace('/', '\\')
            file_name = file_path.split('\\')[-1].split('.')[0]
            # print('\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name)
            file_folder = '\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name
            print(file_path, file_folder + '.pdf')
            word_to_pdf(file_path, file_folder + '.pdf')
            get_pdf_img(file_folder + '.pdf', file_folder)
            self.loadSepFile(file_folder)

    def loadPDF(self):
        if self.file_type != 3:
            self.file_type = 3
            self.clearFiles()
        if self.file_type != 3:
            self.file_type = 3
            self.clearFiles()

        file_path = QFileDialog.getOpenFileName()[0]
        if len(file_path) > 0:
            file_path = file_path.replace('/', '\\')
            file_name = file_path.split('\\')[-1].split('.')[0]
            # print('\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name)
            file_folder = '\\'.join(file_path.split('\\')[0:-1]) + '\\' + file_name
            get_pdf_img(file_path, file_folder)
            self.loadSepFile(file_folder)

    def clearFiles(self):

        self.file_label.setText('请按顺序导入文件')
        self.sep_file_label.setText('请按顺序导入文件')
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
        self.current_file = 0
        self.running = False

    def nextFile(self):
        self.current_file += 1
        print('cccc', self.current_file)
        if self.current_file == len(self.file_list):
            self.current_file = 0

    def startRunning(self):
        # 监听线程初始化
        self.timer = ListenTimer()
        self.timer.timeSignal.signal[str].connect(self.changeStatus)
        self.timer.start()
        self.running = True
        self.stop_play_btn.setDisabled(False)
        self.start_play_btn.setDisabled(True)
        # if self.play_type == 0:
        #     self.playList()
        # else:
        #     self.playSep()

    def stopRunning(self):
        self.timer.stop()
        self.running = False
        self.stop_play_btn.setDisabled(True)
        self.start_play_btn.setDisabled(False)

    # 播放视频
    def playVideo(self, video):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video)))  # 选取视频文件
        self.player.play()

    def playList(self):
        if self.file_type == 0:
            self.playVideo(self.file_list[self.current_file])
        if self.file_type != 0:
            self.playImage()

    # 分时循环播放
    # 根据时间计算当前应该播放的视频，如果没有则返回 0
    def checkTime(self):
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        file_to_play = 0
        for i in range(self.idx):
            if self.start_time_list[i+1] < self.now_time < self.stop_time_list[i+1]:
                file_to_play = i + 1

        return file_to_play

    # 分时循环播放
    def playSep(self):
        self.current_file = self.checkTime()
        if self.current_file > 0:
            if self.file_type == 0:
                self.playVideo(self.sep_file_list[self.current_file])
            if self.file_type != 0:
                self.playImage()

    def showImage(self, imagePath):
        # self.setCentralWidget(self.image_widget)
        img = QtGui.QPixmap(imagePath)
        img_width = img.width()
        img_height = img.height()
        img = img.scaled(img_width * self.image_widget.height() // img_height, self.image_widget.height())
        self.image_widget.setPixmap(img)
        self.image_widget.setAlignment(QtCore.Qt.AlignCenter)

    def playImage(self):
        self.imagePlaying = True
        self.image_widget = QLabel()
        self.image_widget.showFullScreen()
        self.image_widget.setFocus()
        self._fullscreen = True
        # 图片播放监听线程初始化
        self.image_timer = ImageTimer(frequent=self.interval_time)
        self.image_timer.timeSignal.signal[str].connect(self.imageStatusPulse)
        self.image_timer.start()

    def imageStatusPulse(self):
        print('Image running', self.current_file)
        file_folder = self.file_list[self.current_file]
        images = os.listdir(file_folder)
        self.showImage(file_folder + '\\' + images[self.image_idx])
        self.image_idx += 1
        if self.image_idx == len(images):
            self.image_idx = 0
            self.nextFile()

    def hideImage(self):
        self.imagePlaying = False
        self.image_timer.stop()
        sip.delete(self.image_widget)

    # 切换播放模式
    def toggle_play_type(self):
        self.play_type = 0 if self.play_type else 1
        self.type_label.setText('当前模式：' + self.play_type_text[self.play_type] + self.file_type_list[self.file_type])
        if self.play_type == 1:
            toggleWidgetsVisible([self.file_label, self.set_time_label, self.start_time_label, self.start_time_btn,
                                  self.stop_time_label, self.stop_time_btn], False)
            self.sep_file_label.setVisible(True)
            for i in range(self.idx):
                toggleWidgetsVisible([self.file_label_list[i+1], self.start_label_list[i+1], self.start_btn_list[i+1], self.stop_label_list[i+1],
                                      self.stop_btn_list[i+1]], True)
        else:
            toggleWidgetsVisible([self.file_label, self.set_time_label, self.start_time_label, self.start_time_btn,
                                  self.stop_time_label, self.stop_time_btn], True)
            self.sep_file_label.setVisible(False)
            for i in range(self.idx):
                toggleWidgetsVisible([self.file_label_list[i+1], self.start_label_list[i+1], self.start_btn_list[i+1], self.stop_label_list[i+1],
                                      self.stop_btn_list[i+1]], False)

    # 队列循环播放的时间设置
    def start_time_change(self, value):
        self.start_time = QtCore.QTime.toString(value)

    def stop_time_change(self, value):
        self.stop_time = QtCore.QTime.toString(value)

    def interval_time_change(self,value):
        self.interval_time = int(value)


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
        self.type_label = QLabel('当前模式：' + self.play_type_text[self.play_type] + self.file_type_list[self.file_type])
        self.type_btn = QPushButton('切换')
        self.type_btn.setFixedWidth(200)
        self.type_btn.clicked.connect(self.toggle_play_type)
        llayout.addRow(self.type_label, self.type_btn)

        self.file_label = QLabel('请按顺序导入文件')
        self.file_label.setFixedWidth(300)
        llayout.addRow(self.file_label)
        self.sep_file_label = QLabel('请按顺序导入文件')
        self.sep_file_label.setFixedWidth(300)
        self.sep_file_label.setVisible(False)
        llayout.addRow(self.sep_file_label)

        self.set_time_label = QLabel('\n设置播放时间段')
        llayout.addRow(self.set_time_label)
        # 开始时间
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







        # 设置播放间隔
        self.set_time_label = QLabel('\n设置PPT播放间隔，PPT的默认播放间隔时间为2秒')
        llayout.addRow(self.set_time_label)


        self.interval_time_label = QLabel('间隔时间')
        self.interval_time_btn = QLineEdit(str(self.interval_time))
        self.interval_time_btn.setFixedWidth(200)
        self.interval_time_btn.textChanged.connect(self.interval_time_change)
        llayout.addRow(self.interval_time_label, self.interval_time_btn)


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





    def mouseDoubleClickEvent(self, event):
        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if not self._fullscreen:
            self._fullscreen = not self._fullscreen
            if self.file_type == 0:
                self.video_widget.setFullScreen(self._fullscreen)
            if self.file_type != 0:
                self.playImage(self.file_list[self.current_file])
        else:
            self._fullscreen = not self._fullscreen
            if self.file_type == 0:
                self.video_widget.setFullScreen(self._fullscreen)
            if self.file_type != 0:
                print('ESC')
                self.stopRunning()
                self.hideImage()
                pass

    # 由时钟线程触发的播放状态管理
    def changeStatus(self):
        self.now_time = time.strftime("%H:%M:%S", time.localtime())
        if self.play_type == 0:
            print(self.start_time, self.now_time, self.stop_time, self.running)
            if self.start_time < self.now_time < self.stop_time:
                if self.file_type == 0 and self.running:
                    if self.player.state() == QMediaPlayer.StoppedState:
                        print('running', self.player.state(), self.current_file)
                        self.nextFile()
                        self.playList()

                if self.file_type != 0 and not self.imagePlaying:
                    self.playList()

            else:
                if self.file_type == 0:
                    self.video_widget.setFullScreen(self._fullscreen)
                    self.player.stop()
                    self.current_file = 0
                if self.file_type != 0:
                    self.current_file = 0
                    self.hideImage()
        else:
            file_to_play = self.checkTime()
            if file_to_play > 0 and self.running:
                if self.file_type == 0:
                    if self.player.state() == QMediaPlayer.StoppedState:
                        self.playSep()
                        print('running', self.player.state(), self.current_file)
                if self.file_type != 0 and not self.imagePlaying:
                    self.playSep()

            else:
                if self.file_type == 0:
                    # self._fullscreen = False
                    self.video_widget.setFullScreen(self._fullscreen)
                    self.player.stop()
                    self.current_file = 0
                if self.file_type != 0:
                    self.current_file = 0
                    self.hideImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.showMaximized()
    sys.exit(app.exec_())

