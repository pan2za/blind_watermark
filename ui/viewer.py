#!/usr/bin/env python
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import sys 
sys.path.append("..") 
from blind_watermark import WaterMark

import os

class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.vrf_window = VrfWindow()
        self.file_name = ""

        self.decopt_win = DecOptWindow()
        self.decopt_win.sig_opt.connect(self.rundec)        
        self.encopt_win = EncOptWindow()

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Dark)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Ignored)
        #self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum)
        self.imageLabel.setScaledContents(True)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)
        self.createActions()
        self.createMenus()
       
        self.setAcceptDrops(True)#
       
        self.setWindowTitle("盲水印分析器")
        self.resize(500, 400)
        self.encOptAct.setEnabled(True)
        self.decOptAct.setEnabled(True)  
        # Setup tools
        camera_toolbar = QToolBar("Camera")
        camera_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(camera_toolbar)

        photo_action = QAction(QIcon(os.path.join('images', 'camera-black.png')), "添加水印...", self)
        photo_action.setStatusTip("添加水印")
        photo_action.triggered.connect(self.encode)
        camera_toolbar.addAction(photo_action)

        change_folder_action = QAction(QIcon(os.path.join('images', 'blue-folder-horizontal-open.png')), "解析水印...", self)
        change_folder_action.setStatusTip("解析水印")
        change_folder_action.triggered.connect(self.decode)
        camera_toolbar.addAction(change_folder_action)

    def open(self):
        fileName,filetype = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件",
                QtCore.QDir.currentPath())
        if fileName:
            self.file_name = fileName
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "盲水印分析器",
                        "无法加载 %s." % fileName)
                return
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()
            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
    
    def dragEnterEvent(self, event):#拖动开始时，以及刚进入目标控件时调用
        event.acceptProposedAction() #必须要有
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls=event.mimeData().urls()
            try:
                url=urls[0]
                fileName = str(url.toLocalFile())
                if fileName:
                    self.file_name = fileName
                    image = QtGui.QImage(fileName)
                    if image.isNull():
                        QtWidgets.QMessageBox.information(self, "盲水印分析器",
                                "无法加载 %s." % fileName)
                        return
                    self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
                    self.scaleFactor = 1.0
                    self.printAct.setEnabled(True)
                    self.fitToWindowAct.setEnabled(True)
                    self.updateActions()
                    if not self.fitToWindowAct.isChecked():
                        self.imageLabel.adjustSize()
                    self.fitToWindow()
            except:
                pass
        else:
            super(ImageViewer, self).dropEvent(event)
    
    def handlePrint(self, printer):#打印
        painter = QtGui.QPainter(printer)#使用painter 绘制文字、pixmap等在printer上
        painter.setRenderHint(QtGui.QPainter.Antialiasing)#抗锯齿#可有可无
        pix = self.imageLabel.pixmap()
        size = self.scaleFactor * pix.size()
        painter.drawPixmap(0, 0, size.width(), size.height(),pix)
       
    def printPreview(self):#打印预览
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePrint)
        dialog.exec_()
 
    def print_setup(self):#打印，无预览
        printer = QPrinter()
        painter.setRenderHint(QPainter.Antialiasing)#抗锯齿
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QDialog.Accepted:
            self.handlePrint(printer)

    def zoomIn(self):
        self.scaleImage(1.25)
        
    def zoomOut(self):
        self.scaleImage(0.8)
        
    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
        
    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()
        
    def about(self):
        QtWidgets.QMessageBox.about(self, "水印分析器",
                "<p>The <b>水印分析器</b> example shows how to combine "
                "基于QT完成 "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>"
                "<p>In addition the example shows how to use QPainter to "
                "print an image.</p>")

    def xtouch(self, file_name):
        if file_name in os.listdir('.'):
            print("file exist!")
        else:
            fid = open(file_name,'w')
            fid.close()

    def encode(self):
        try:
            bwm1 = WaterMark(password_img=1, password_wm=1)
            bwm1.read_img(self.file_name)
            outf = 'output/embed.png'
            wm = self.encopt_win.plain
            bwm1.read_wm(wm, mode='str')
            if not os.path.exists('output'):
                os.mkdir('output', 755)
            self.xtouch(outf)
            bwm1.embed(outf)
            len_wm = len(bwm1.wm_bit)
            print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
            if len_wm != None and len_wm > 0:
                QtWidgets.QMessageBox.information(self, "添加水印成功",
                            "水印长度： %d \r\n添加水印后文件 %s.\r\n水印内容:%s" % (len_wm, outf, wm))
            else:
                QtWidgets.QMessageBox.information(self, "添加水印失败",
                            "无法添加水印到文件 %s." % self.file_name)    
        except:
                QtWidgets.QMessageBox.information(self, "添加水印失败",
                            "水印数据过长或水印文件不存在，无法添加水印到文件 %s." % self.file_name)    

    @pyqtSlot()
    def decode(self):
        """
        Slot documentation goes here.
        """
        self.decopt_win.setWindowModality(Qt.ApplicationModal)
        self.decopt_win.show()

    @pyqtSlot()
    def rundec(self):
        self.vrf_window.show()
        self.vrf_window.sig_vrf.emit(self.file_name, self.decopt_win.dec_len)#修改5：窗口传递具体的信号

    def decOpt(self):
        """
        解除水印选项.
        """
        self.decopt_win.show()

    def encOpt(self):
        """
        添加水印文本选项.
        """
        self.encopt_win.show()

    def createActions(self):
        self.openAct = QtWidgets.QAction("打开(&O)...", self, shortcut="Ctrl+O",
                triggered=self.open)
        self.printAct = QtWidgets.QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.printPreview)
        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)
        self.zoomInAct = QtWidgets.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QtWidgets.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QtWidgets.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QtWidgets.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)
        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QtWidgets.QAction("About &Qt", self,
                triggered=QtWidgets.qApp.aboutQt)
        self.decodeAct = QtWidgets.QAction("解码验证(&V)", self,
                shortcut="Ctrl+V", enabled=False, triggered=self.decode)          
        self.encodeAct = QtWidgets.QAction("增加水印(&E)", self,
                shortcut="Ctrl+E", enabled=False, triggered=self.encode)                      
        self.encOptAct = QtWidgets.QAction("加水印选项(&E)", self,
                shortcut="Ctrl+E", enabled=False, triggered=self.encOpt)   
        self.decOptAct = QtWidgets.QAction("解水印选项(&E)", self,
                shortcut="Ctrl+E", enabled=False, triggered=self.decOpt)  

    def createMenus(self):
        self.fileMenu = QtWidgets.QMenu("文件(&F)", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.viewMenu = QtWidgets.QMenu("查看(&V)", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)
        self.anaMenu = QtWidgets.QMenu("分析(&A)", self)
        self.anaMenu.addAction(self.decodeAct)
        self.anaMenu.addAction(self.encodeAct)
        self.anaMenu.addAction(self.decOptAct)
        self.anaMenu.addAction(self.encOptAct)
        self.helpMenu = QtWidgets.QMenu("帮助(&H)", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.anaMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)
        
    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.encodeAct.setEnabled(not self.encodeAct.isChecked())
        self.decodeAct.setEnabled(True)  
        self.encOptAct.setEnabled(True)
        self.decOptAct.setEnabled(True)      
    
    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
    
    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

class VrfWindow(QtWidgets.QWidget):
     sig_vrf=pyqtSignal(str, int) #修改4：子窗口建立信号传递的是（str）数据

     @pyqtSlot()
     def __init__(self):
         super(VrfWindow, self).__init__()
         self.sig_vrf.connect(self.fun)
         self.resize(400, 300)
         self.setWindowTitle("解码结果报告")
         # Label
         self.txte = QTextEdit(self)
         self.txte.setGeometry(0, 0, 400, 300)
         self.txte.setText('水印内容')
         self.txte.setAlignment(Qt.AlignCenter)
         self.txte.setStyleSheet('font-size:20px')
     def fun(self, fn, len):
         try:
            bwm1 = WaterMark(password_img=1, password_wm=1)
            if bwm1.wm_bit == None:
                len_wm = len 
            else:
                len_wm = len(bwm1.wm_bit)
            wm_extract = bwm1.extract(fn, wm_shape=len_wm, mode='str')
            print("encoded text: ", wm_extract)
            self.txte.setText(wm_extract)
         except:
            self.txte.setText('无法获取水印内容')
            QtWidgets.QMessageBox.information(self, "解码水印失败",
                        "无法解码水印文件 %s,水印长度：%d." % (fn, len)) 
            self.close()  
            



class DecOptWindow(QtWidgets.QWidget):
     dec_len = 512
     sig_opt=pyqtSignal(str, int) #修改4：子窗口建立信号传递的是（str）数据
     def __init__(self):
         super(DecOptWindow, self).__init__()
         self.resize(400, 300)
         self.setWindowTitle("解码水印选项:设置水印长度")
         # Label
         self.txte = QLineEdit(self)
         self.txte.setGeometry(0, 0, 400, 300)
         self.txte.setText(str(self.dec_len))
         self.txte.setAlignment(Qt.AlignCenter)
         self.txte.setStyleSheet('font-size:40px')

     @pyqtSlot()
     def closeEvent(self, event):
         self.dec_len = int(self.txte.text())
         self.sig_opt.emit("", self.dec_len)#修改5：窗口传递具体的信号

         

class EncOptWindow(QtWidgets.QWidget):
     plain = "水印默认内容建议少加一些"
     def __init__(self):
         super(EncOptWindow, self).__init__()
         self.resize(400, 300)
         self.setWindowTitle("水印选项:设置水印内容")
         # Label
         self.txte = QTextEdit(self)
         self.txte.setGeometry(0, 0, 400, 300)
         self.txte.setText(self.plain)
         self.txte.setAlignment(Qt.AlignLeft)
         self.txte.setStyleSheet('font-size:20px')

     def closeEvent(self, event):
         self.plain = self.txte.toPlainText()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())