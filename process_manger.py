import os

import psutil
import qdarkstyle
# from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QListWidget, QAbstractItemView, QLineEdit, QPushButton, QVBoxLayout, \
    QApplication, QListWidgetItem


class ProcessManager(QWidget):
    def __init__(self):
        super(ProcessManager, self).__init__()

        self.processes = []
        self.selected_process = None

        self.process_list = QListWidget()
        self.process_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.process_list.itemSelectionChanged.connect(self.update_selected_process)

        self.port_filter = QLineEdit()
        self.port_filter.setPlaceholderText("筛选 by Port")
        self.port_filter.textChanged.connect(self.filter_processes)

        self.process_filter = QLineEdit()
        self.process_filter.setPlaceholderText("筛选 by Process Name")
        self.process_filter.textChanged.connect(self.filter_processes)

        self.kill_button = QPushButton("杀死进程")
        self.kill_button.clicked.connect(self.kill_selected_process)
        self.kill_button.setEnabled(False)

        self.refresh_button = QPushButton("刷新进程列表")
        self.refresh_button.clicked.connect(self.refresh_processes)

        layout = QVBoxLayout()
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.process_list)
        layout.addWidget(self.port_filter)
        layout.addWidget(self.process_filter)
        layout.addWidget(self.kill_button)

        self.setLayout(layout)
        # self.Icon = QIcon("./icon.ico")
        self.setWindowTitle("进程管理")
        self.setWindowIcon(self.Icon)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))

        self.refresh_processes()

    def refresh_processes(self):
        self.processes.clear()
        self.process_list.clear()

        for process in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                process_info = process.as_dict(attrs=['pid', 'name', 'connections'])
                self.processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.filter_processes()

    def filter_processes(self):
        port_filter_text = self.port_filter.text().strip()
        process_filter_text = self.process_filter.text().strip()

        filtered_processes = []

        for process in self.processes:
            if port_filter_text and not any(str(port_filter_text) in str(c.laddr.port) for c in process['connections']):
                continue
            if process_filter_text and process['name'].lower().find(process_filter_text.lower()) == -1:
                continue

            filtered_processes.append(process)

        self.process_list.clear()

        for process in filtered_processes:
            # item = QListWidgetItem("{} (PID: {}) ({})".format(process['name'], process['pid'], process['connections']))
            item = QListWidgetItem(
                f"{process['name']} (PID: {process['pid']}) Port:{'/'.join([d.laddr.port.__str__() for d in process['connections']])}")
            self.process_list.addItem(item)

        self.selected_process = None
        self.kill_button.setEnabled(False)
        # 使用CMD命令查找占用该端口的进程
        command_find = f"netstat -ano | findstr :{port_filter_text or process_filter_text}"
        print(command_find)

    def update_selected_process(self):
        items = self.process_list.selectedItems()

        if not items:
            self.selected_process = None
            self.kill_button.setEnabled(False)
            return

        item = items[0]
        for process in self.processes:
            if f"{process['name']} (PID: {process['pid']}) Port:{'/'.join([d.laddr.port.__str__() for d in process['connections']])}" == item.text():
                self.selected_process = process
                self.kill_button.setEnabled(True)
                break

    def kill_selected_process(self):

        if not self.selected_process:
            return

        try:
            # 使用CMD命令结束该进程及其子进程
            command_kill = f"taskkill /f /t /pid {self.selected_process['pid']}"
            print(command_kill)
            output_kill = os.popen(command_kill).read()
            # process = psutil.Process(self.selected_process['pid'])
            # process.kill()
            print(f"kill {self.selected_process['pid']} {output_kill}")
        except Exception as e:
            print(e)

        self.refresh_processes()


if __name__ == "__main__":
    app = QApplication([])
    window = ProcessManager()
    window.show()
    app.exec_()
