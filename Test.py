from PyQt5 import QtCore,QtGui,QtWidgets
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
import sys
import requests
class MainUi(QtWidgets.QMainWindow):
    #构造函数
    def __init__(self):
        super().__init__()
        # self.test =  QtWidgets.QPushButton()
        # self.getObjectFun_Attr(self.test.geometry())
        splash = QtWidgets.QSplashScreen()
        splash.setGeometry(600, 300,200, 200)
        Label= QtWidgets.QLabel("本工具由【清枫冥月】制作",splash)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setWeight(75)
        Label.setFont(font)
        Label.setAlignment(QtCore.Qt.AlignCenter)
        Label.setGeometry(0, 0,200,25)

        icoBtn = QtWidgets.QPushButton(splash)
        icoBtn_icon = QIcon()
        req = requests.get("http://resource.ink-cloud.xyz/lpf/paycode.png")
        img  = QPixmap()
        img.loadFromData(req.content)
        icoBtn_icon.addPixmap(img, QIcon.Normal, QIcon.Off)
        icoBtn.setIcon(icoBtn_icon)
        icoBtn.setIconSize(QSize(100, 100))
        icoBtn.setGeometry(50, 30, 100, 100)

        Label= QtWidgets.QLabel("如果觉得不错，扫码赞助一下如何？",splash)
        Label.adjustSize()
        Label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(8)
        Label.setFont(font)
        Label.setAlignment(QtCore.Qt.AlignCenter)
        Label.setGeometry(0, 140,200,25)

        closeBtn = QtWidgets.QPushButton("确定",splash)
        closeBtn.setObjectName('showBtn')
        closeBtn.setProperty("id","closeBtnTrue")
        closeBtn.setGeometry(50, 170,100,30)

        splash.show()
        QtWidgets.qApp.processEvents()
        time.sleep(2)
        splash.finish(self)



        #self.getObjectFun_Attr(QtWidgets.QSplashScreen())

        # splash = QtWidgets.QSplashScreen()
        # splash.setGeometry(600, 300,200, 100)
        # splashLabel =QtWidgets.QLabel("",splash)
        # splashgif = QtGui.QMovie("./source/Loading.gif")
        # splashLabel.setMovie(splashgif)
        # splashLabel.setGeometry(65, 10,65,65)
        # content =QtWidgets.QLabel("爬取英雄数据",splash)
        # content.setGeometry(0, 80,200,20)
        # content.setAlignment(QtCore.Qt.AlignCenter)
        # splashgif.start()
        #
        # #splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        # splash.show()                           # 显示启动界面
        # for i in range(1, 11):              #模拟主程序加载过程
        #     time.sleep(1)                   # 加载数据
        #     QtWidgets.qApp.processEvents()
        #     content.setText("爬取。。。")
        #     #splash.showMessage("加载... {0}%".format(i * 10), QtCore.Qt.AlignHCenter |QtCore.Qt.AlignBottom, QtCore.Qt.black)
        # splash.finish(self)

    def getObjectFun_Attr(self,object):
        list = dir(object)
        for i in range(0,len(list)):
            print(list[i])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
