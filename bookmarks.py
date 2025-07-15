from PySide2.QtWidgets import QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QInputDialog, QMessageBox
from PySide2.QtCore import Qt, QSettings


class BookmarkManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("书签管理器")
        self.resize(600, 400)

        # 创建布局
        layout = QVBoxLayout()

        # 书签列表
        self.bookmark_list = QListWidget()
        layout.addWidget(self.bookmark_list)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("添加书签")
        self.add_btn.clicked.connect(self.add_bookmark)
        button_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("编辑")
        self.edit_btn.clicked.connect(self.edit_bookmark)
        button_layout.addWidget(self.edit_btn)

        self.remove_btn = QPushButton("删除")
        self.remove_btn.clicked.connect(self.remove_bookmark)
        button_layout.addWidget(self.remove_btn)

        self.open_btn = QPushButton("打开")
        self.open_btn.clicked.connect(self.open_bookmark)
        button_layout.addWidget(self.open_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 加载书签
        self.load_bookmarks()

    def load_bookmarks(self):
        """从设置加载书签"""
        settings = QSettings("SaFan", "Browser")
        bookmarks = settings.value("bookmarks", [])

        self.bookmark_list.clear()
        for title, url in bookmarks:
            self.bookmark_list.addItem(f"{title} - {url}")

    def save_bookmarks(self):
        """保存书签到设置"""
        settings = QSettings("SaFan", "Browser")
        bookmarks = []

        for i in range(self.bookmark_list.count()):
            text = self.bookmark_list.item(i).text()
            parts = text.split(" - ")
            if len(parts) >= 2:
                bookmarks.append((parts[0], parts[1]))

        settings.setValue("bookmarks", bookmarks)

    def add_bookmark(self, title="", url=""):
        """添加书签"""
        if not title or not url:
            title, ok = QInputDialog.getText(self, "添加书签", "标题:")
            if not ok or not title:
                return

            url, ok = QInputDialog.getText(self, "添加书签", "URL:")
            if not ok or not url:
                return

        self.bookmark_list.addItem(f"{title} - {url}")
        self.save_bookmarks()

    def edit_bookmark(self):
        """编辑书签"""
        current_item = self.bookmark_list.currentItem()
        if not current_item:
            return

        text = current_item.text()
        parts = text.split(" - ")
        if len(parts) < 2:
            return

        title, url = parts[0], " - ".join(parts[1:])

        new_title, ok1 = QInputDialog.getText(self, "编辑书签", "标题:", text=title)
        new_url, ok2 = QInputDialog.getText(self, "编辑书签", "URL:", text=url)

        if ok1 and ok2 and new_title and new_url:
            current_item.setText(f"{new_title} - {new_url}")
            self.save_bookmarks()

    def remove_bookmark(self):
        """删除书签"""
        current_row = self.bookmark_list.currentRow()
        if current_row >= 0:
            self.bookmark_list.takeItem(current_row)
            self.save_bookmarks()

    def open_bookmark(self):
        """打开书签"""
        current_item = self.bookmark_list.currentItem()
        if not current_item:
            return

        text = current_item.text()
        parts = text.split(" - ")
        if len(parts) < 2:
            return

        url = " - ".join(parts[1:])
        self.parent().tab_widget.add_new_tab(QUrl(url))
        self.close()