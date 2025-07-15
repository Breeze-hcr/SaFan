from PySide2.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QFileDialog
from PySide2.QtCore import Qt, QSettings, QStandardPaths, QTimer
from PySide2.QtWebEngineWidgets import QWebEngineDownloadItem
from PySide2.QtGui import QDesktopServices
import os


class DownloadManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("下载内容")
        self.resize(600, 400)

        # 创建布局
        layout = QVBoxLayout()

        # 下载列表
        self.download_list = QListWidget()
        layout.addWidget(self.download_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.open_btn = QPushButton("打开")
        self.open_btn.clicked.connect(self.open_download)
        button_layout.addWidget(self.open_btn)

        self.show_btn = QPushButton("在文件夹中显示")
        self.show_btn.clicked.connect(self.show_in_folder)
        button_layout.addWidget(self.show_btn)

        self.clear_btn = QPushButton("清除已完成")
        self.clear_btn.clicked.connect(self.clear_completed)
        button_layout.addWidget(self.clear_btn)

        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 加载下载历史
        self.load_downloads()

        # 设置定时器更新下载状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_download_status)
        self.timer.start(1000)  # 每秒更新一次

    def load_downloads(self):
        """从设置加载下载历史"""
        settings = QSettings("SaFan", "Browser")
        downloads = settings.value("downloads", [])

        self.download_list.clear()
        for path, url, state in downloads:
            self.download_list.addItem(f"{os.path.basename(path)} - {state}")
            self.download_list.item(self.download_list.count() - 1).setData(Qt.UserRole, (path, url, state))

    def save_downloads(self):
        """保存下载历史到设置"""
        settings = QSettings("SaFan", "Browser")
        downloads = []

        for i in range(self.download_list.count()):
            item = self.download_list.item(i)
            path, url, state = item.data(Qt.UserRole)
            downloads.append((path, url, state))

        settings.setValue("downloads", downloads)

    def add_download(self, download: QWebEngineDownloadItem):
        """添加下载项"""
        path = download.path()
        url = download.url().toString()

        self.download_list.addItem(f"{os.path.basename(path)} - 下载中...")
        item = self.download_list.item(self.download_list.count() - 1)
        item.setData(Qt.UserRole, (path, url, "downloading"))

        # 连接下载信号
        download.finished.connect(lambda: self.download_finished(download))
        download.downloadProgress.connect(
            lambda received, total: self.update_download_progress(item, received, total))

        # 保存下载记录
        self.save_downloads()

    def download_finished(self, download: QWebEngineDownloadItem):
        """下载完成处理"""
        for i in range(self.download_list.count()):
            item = self.download_list.item(i)
            path, url, state = item.data(Qt.UserRole)
            if path == download.path():
                item.setData(Qt.UserRole, (path, url, "completed"))
                item.setText(f"{os.path.basename(path)} - 已完成")
                self.save_downloads()
                break

    def update_download_progress(self, item, received, total):
        """更新下载进度"""
        if total > 0:
            percent = int(received * 100 / total)
            path, url, state = item.data(Qt.UserRole)
            item.setText(f"{os.path.basename(path)} - 下载中 {percent}%")

    def update_download_status(self):
        """更新下载状态（定时器触发）"""
        # 这里可以添加额外的状态更新逻辑
        pass

    def open_download(self):
        """打开下载的文件"""
        current_item = self.download_list.currentItem()
        if not current_item:
            return

        path, url, state = current_item.data(Qt.UserRole)
        if state == "completed" and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def show_in_folder(self):
        """在文件夹中显示下载的文件"""
        current_item = self.download_list.currentItem()
        if not current_item:
            return

        path, url, state = current_item.data(Qt.UserRole)
        if state == "completed" and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))

    def clear_completed(self):
        """清除已完成的下载"""
        for i in range(self.download_list.count() - 1, -1, -1):
            item = self.download_list.item(i)
            path, url, state = item.data(Qt.UserRole)
            if state == "completed":
                self.download_list.takeItem(i)

        self.save_downloads()