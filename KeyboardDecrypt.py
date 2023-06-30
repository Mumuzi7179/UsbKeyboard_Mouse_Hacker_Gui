from PySide6.QtWidgets import QComboBox,QStackedWidget,QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QRadioButton, QButtonGroup, QTabWidget, QMenuBar, QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
import sys,os
import datetime
from UsbKeyboardExtract import extract_data,process_data

class KeyboardDecryptWindow(QWidget):
    file_name = Signal(str)  # 文件名信号
    file_dropped = Signal(str)

    def __init__(self,parent=None):
        super(KeyboardDecryptWindow, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 选择执行的类型
        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("选择执行类型：")
        self.type_layout.addWidget(self.type_label)
        self.button_group = QButtonGroup(self)
        self.select_type1 = QRadioButton("capdata")
        self.select_type2 = QRadioButton("usbhid")

        self.button_group.addButton(self.select_type1)
        self.button_group.addButton(self.select_type2)
        self.type_layout.addWidget(self.select_type1)
        self.type_layout.addWidget(self.select_type2)
        # 确定按钮
        self.run_button = QPushButton("点击执行")
        stylesheet = load_stylesheet("./css/style.css")
        self.run_button.setStyleSheet(stylesheet)
        self.run_button.clicked.connect(self.run_command)
        self.type_layout.addWidget(self.run_button)
        self.layout.addLayout(self.type_layout)

        # 输出窗口
        self.output = QTextEdit()
        self.layout.addWidget(self.output)
        self.output.setReadOnly(True)

        self.setAcceptDrops(True)

        # 文件名变量
        self.file = ''

        # 接收文件名信号
        self.file_name.connect(self.set_file)

    def set_file(self, file):
        self.file = file

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()

        url = urls[0]

        filePath = url.toLocalFile()

        self.file_dropped.emit(filePath)



    def run_command(self):
        self.output.clear()

        current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.output.append(f"{current_time}")

        checked_button = self.button_group.checkedButton()
        if checked_button:
            type = checked_button.text()
        else:
            type = None
        if not self.file:
            self.output.append("错误：没有选择文件。")
            return
        if not type:
            self.output.append("错误：没有选择执行类型。")
            return
        self.output.append(f"执行的类型： {type}")
        try:
            result,result1 = extract_data(type, self.file)
            result2,result_delete = process_data(result1)
        except Exception as e:
            self.output.append(f"执行出错：{e}")
        else:
            self.output.append("执行成功。结果如下：")
            self.output.append(result)
            self.output.append("处理后的结果如下：")
            self.output.append(result2)
            self.output.append("删除的字符如下:")
            self.output.append(result_delete)


def load_stylesheet(filename):
    with open(filename, "r") as f:
        return f.read()