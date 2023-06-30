from PySide6.QtWidgets import QStackedWidget,QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QToolBar
from PySide6.QtGui import QAction,QIcon
import sys
from KeyboardDecrypt import KeyboardDecryptWindow
from MouseDecrypt import MouseDecryptWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("键盘流量&鼠标流量 GUI by mumuzi")
        self.keyboardDecryptWindow = KeyboardDecryptWindow(self)
        self.keyboardDecryptWindow.file_dropped.connect(self.set_file)
        self.mouseDecryptWindow = MouseDecryptWindow()
        self.mouseDecryptWindow.file_dropped.connect(self.set_file)

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.addWidget(self.keyboardDecryptWindow)
        self.stackedWidget.addWidget(self.mouseDecryptWindow)

        self.typeToolBar = QToolBar(self)
        self.keyboardAction = QAction('键盘流量解密', self)
        self.mouseAction = QAction('鼠标流量解密', self)
        self.keyboardAction.triggered.connect(lambda: self.switch_window(0))
        self.mouseAction.triggered.connect(lambda: self.switch_window(1))
        self.typeToolBar.addAction(self.keyboardAction)
        self.typeToolBar.addAction(self.mouseAction)
        self.addToolBar(self.typeToolBar)

        # 文件选择功能

        self.fileToolBar = QToolBar(self)
        self.select_file_label = QLabel("选择或拖拽文件")
        self.fileToolBar.addWidget(self.select_file_label)
        self.file_name = QLineEdit()
        self.file_name.setReadOnly(True)
        self.fileToolBar.addWidget(self.file_name)
        self.select_file_button = QAction("浏览文件", self)
        self.select_file_button.triggered.connect(self.select_file)
        self.fileToolBar.addAction(self.select_file_button)
        self.addToolBar(self.fileToolBar)

        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)

        self.setWindowIcon(QIcon('./img/myico.ico'))
        self.setStyleSheet("""
            MainWindow {background-image: url(img/mybg.jpg)}
            QPushButton {background-color: transparent}
            QTextEdit {background-color: rgba(255, 255, 255, 200)}
            QLineEdit {background-color: rgba(255, 255, 255, 200)}
        """)

        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

        # 设置窗口大小
        self.resize(600, 450)

    def switch_window(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def select_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Wireshark pcapng (*.ntar *.ntar.* *.pcapng.gz *.pcapng.zst *.pcapng.lz4 *.pcapng);;tcpdump pcap (*.dmp.* *.dmp *.cap.* *.cap *.pcap.* *.pcap);;other (*.*)", options=options)
        if fileName:
            self.file_name.setText(fileName)  # 更新file_name文本框的文本
            self.keyboardDecryptWindow.set_file(fileName)
            self.mouseDecryptWindow.set_file(fileName)

    def set_file(self, file_name):
        self.file_name.setText(file_name)
        self.keyboardDecryptWindow.set_file(file_name)
        self.mouseDecryptWindow.set_file(file_name)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
