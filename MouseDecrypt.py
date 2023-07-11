from PySide6.QtWidgets import QSizePolicy,QComboBox,QStackedWidget,QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QRadioButton, QButtonGroup, QTabWidget, QMenuBar, QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
import sys,os,time,datetime
from MouseExtract import extract_data
import matplotlib.pyplot as plt

class MouseDecryptWindow(QWidget):
    file_name = Signal(str)  # 文件名信号
    file_dropped = Signal(str)

    def __init__(self):
        super(MouseDecryptWindow, self).__init__()

        self.layout = QVBoxLayout(self)

        # 选择执行的类型
        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("选择执行类型：")
        self.type_layout.addWidget(self.type_label)
        self.button_group_type = QButtonGroup(self)
        self.select_type1 = QRadioButton("capdata")
        self.select_type2 = QRadioButton("usbhid")
        self.button_group_type.addButton(self.select_type1)
        self.button_group_type.addButton(self.select_type2)
        self.type_layout.addWidget(self.select_type1)
        self.type_layout.addWidget(self.select_type2)
        self.layout.addLayout(self.type_layout)

        # 选择想要查看的鼠标按键
        self.button_layout = QHBoxLayout()
        self.button_label = QLabel("选择想要查看的鼠标按键：")
        self.button_layout.addWidget(self.button_label)
        self.button_group_button = QButtonGroup(self)
        self.select_button1 = QRadioButton("左键")
        self.select_button2 = QRadioButton("右键")
        self.select_button3 = QRadioButton("无按键")
        self.select_button4 = QRadioButton("所有")
        self.button_group_button.addButton(self.select_button1)
        self.button_group_button.addButton(self.select_button2)
        self.button_group_button.addButton(self.select_button3)
        self.button_group_button.addButton(self.select_button4)
        self.button_layout.addWidget(self.select_button1)
        self.button_layout.addWidget(self.select_button2)
        self.button_layout.addWidget(self.select_button3)
        self.button_layout.addWidget(self.select_button4)
        self.layout.addLayout(self.button_layout)

        # 执行按钮
        self.button_layout = QHBoxLayout()
        stylesheet = load_stylesheet("./css/style.css")

        self.run_button = QPushButton("保存并打开图片")
        self.run_button.clicked.connect(self.run_command)
        self.run_button.setFixedSize(120, 40)  # 设置固定大小
        self.button_layout.addWidget(self.run_button)
        self.run_button.setStyleSheet(stylesheet)

        # 保存图片按钮
        self.save_button = QPushButton("仅保存图片")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setFixedSize(120, 40)  # 设置固定大小
        self.button_layout.addWidget(self.save_button)
        self.save_button.setStyleSheet(stylesheet)

        self.all_button = QPushButton("一键保存全部")
        self.all_button.clicked.connect(self.all_command)
        self.all_button.setFixedSize(120, 40)  # 设置固定大小
        self.button_layout.addWidget(self.all_button)
        self.all_button.setStyleSheet(stylesheet)

        self.layout.addLayout(self.button_layout)

        # 输出窗口
        self.output = QTextEdit()
        self.layout.addWidget(self.output)
        self.output.setReadOnly(True)

        self.setLayout(self.layout)

        # 文件名变量
        self.file = ''

        # 接收文件名信号
        self.file_name.connect(self.set_file)

        self.setAcceptDrops(True)

    def set_file(self, file):
        self.file = file

    def dragEnterEvent(self, event):
        # accept the drag only if it contains files
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # get the file URLs (a list of QUrls)
        urls = event.mimeData().urls()

        # assuming only one file is dropped, get the first URL
        url = urls[0]

        # get the file path (a string)
        filePath = url.toLocalFile()

        # 发送文件名信号
        self.file_dropped.emit(filePath)

    def save_image(self):
        self.run_command(from_save_button=True)

    def run_command(self,from_save_button=False):
        self.output.clear()

        # 输出当前时间
        current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.output.append(f"{current_time}")

        # 获取当前选中的执行类型和鼠标按键
        checked_button_type = self.button_group_type.checkedButton()
        checked_button_key = self.button_group_button.checkedButton()

        # 检查是否选择了执行类型和鼠标按键以及文件
        if checked_button_type:
            _type = checked_button_type.text()
        else:
            _type = None

        if checked_button_key:
            key = checked_button_key.text()
        else:
            key = None

        if not self.file:
            self.output.append("错误：没有选择文件。")
            return

        if not _type:
            self.output.append("错误：没有选择执行类型。")
            return

        if not key:
            self.output.append("错误：没有选择鼠标按键。")
            return

        self.output.append(f"执行的类型： {_type}")
        self.output.append(f"选择的鼠标按键： {key}")
        self.output.append("正在执行，若文件较大可能会出现无响应情况，请稍后……")

        QApplication.processEvents()

        try:
            result = extract_data(_type, key, self.file)
        except Exception as e:
            self.output.append(f"执行出错：{e}")
        else:
            self.output.append("执行成功。")
            self.output.append("已将转换后的坐标写入result.txt，如有需要可自行利用")
            self.output.append(f"已将图片保存至当前环境运行目录下的output_files文件夹中的{_type}_{key}.png")
            time.sleep(0.5)
            if not os.path.exists('output_files'):
                os.mkdir('output_files')
            result.savefig(f"./output_files/{_type}_{key}.png")
            if not from_save_button:
                os.system(f"./output_files/{_type}_{key}.png")

    def all_command(self):
        self.output.clear()

        # 输出当前时间
        current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.output.append(f"{current_time}")

        if not self.file:
            self.output.append("错误：没有选择文件。")
            return

        self.output.append("正在执行，若文件较大可能会出现无响应情况，请稍后……")
        QApplication.processEvents()
        for _type in ['capdata','usbhid']:
            for key in ['左键','右键','无按键','所有']:
                try:
                    result = extract_data(_type, key, self.file)
                except Exception as e:
                    self.output.append(f"执行出错：{e}")
                else:
                    self.output.append("执行成功。")
                    self.output.append(f"已将图片保存至当前环境运行目录下的output_files文件夹中的{_type}_{key}.png")
                    QApplication.processEvents()
                    time.sleep(0.1)
                    if not os.path.exists('output_files'):
                        os.mkdir('output_files')
                    result.savefig(f"./output_files/{_type}_{key}.png")


def load_stylesheet(filename):
    with open(filename, "r") as f:
        return f.read()
