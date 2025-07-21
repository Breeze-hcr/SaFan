from PySide2.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QMessageBox
from PySide2.QtCore import Qt, QSettings, QDateTime
from PySide2.QtGui import QDesktopServices


class HistoryManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.resize(800, 500)

        # 创建布局
        layout = QVBoxLayout()

        # 历史记录列表
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.clear_btn = QPushButton("清除历史记录")
        self.clear_btn.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_btn)

        self.open_btn = QPushButton("打开")
        self.open_btn.clicked.connect(self.open_history)
        button_layout.addWidget(self.open_btn)

        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 加载历史记录
        self.load_history()

    def load_history(self):
        """从设置加载历史记录"""
        settings = QSettings("", "Browser")
        history = settings.value("history", [])

        self.history_list.clear()
        for entry in history:
            timestamp, url, title = entry
            dt = QDateTime.fromString(timestamp, Qt.ISODate)
            self.history_list.addItem(f"{dt.toString('yyyy-MM-dd hh:mm:ss')} - {title} - {url}")

    def save_history(self, history):
        """保存历史记录到设置"""
        settings = QSettings("", "Browser")
        settings.setValue("history", history)

    def add_history_entry(self, url, title):
        """添加历史记录条目"""
        settings = QSettings("", "Browser")
        history = settings.value("history", [])

        # 保留最近100条历史记录
        if len(history) >= 100:
            history = history[-99:]

        history.append((QDateTime.currentDateTime().toString(Qt.ISODate), url, title))
        settings.setValue("history", history)

    def clear_history(self):
        """清除历史记录"""
        reply = QMessageBox.question(self, "清除历史记录",
                                     "确定要清除所有浏览历史记录吗？此操作无法撤销。",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            settings = QSettings("", "Browser")
            settings.remove("history")
            self.history_list.clear()

    def open_history(self):
        """打开选中的历史记录"""
        current_item = self.history_list.currentItem()
        if not current_item:
            return

        text = current_item.text()
        parts = text.split(" - ")
        if len(parts) < 3:
            return

        url = parts[-1]
        # 通过父窗口打开历史记录
        if self.parent():
            self.parent().tab_widget.add_new_tab(QUrl(url))
        self.close()