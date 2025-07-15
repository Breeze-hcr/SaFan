from PySide2.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton
from PySide2.QtGui import QIcon
from PySide2.QtCore import QUrl, Qt, Signal
from PySide2.QtWebEngineWidgets import QWebEngineView


class TabWidget(QTabWidget):
    url_changed = Signal(QUrl)
    title_changed = Signal(str)
    load_progress = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)

        # 添加新标签页按钮
        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedSize(30, 30)
        new_tab_btn.setStyleSheet("""
            QPushButton {
                background: #007ACC;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0099FF;
            }
        """)
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.setCornerWidget(new_tab_btn, Qt.TopRightCorner)

    def add_new_tab(self, qurl=None, label="新标签页"):
        """添加新标签页"""
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # 连接信号
        browser.urlChanged.connect(lambda q: self.url_changed.emit(q))
        browser.titleChanged.connect(lambda title: self.title_changed.emit(title))
        browser.loadProgress.connect(lambda p: self.load_progress.emit(p))

        # 添加标签页
        index = self.addTab(browser, label)
        self.setCurrentIndex(index)
        return browser

    def close_tab(self, index):
        """关闭标签页"""
        if self.count() < 2:
            return

        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)

    def tab_changed(self, index):
        """标签页切换时更新地址栏和标题"""
        if index >= 0:
            browser = self.widget(index)
            if browser:
                self.url_changed.emit(browser.url())
                self.title_changed.emit(browser.title())

    def current_browser(self):
        """获取当前标签页的浏览器部件"""
        return self.currentWidget()