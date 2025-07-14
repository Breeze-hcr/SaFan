from PySide2.QtWidgets import (QMainWindow, QToolBar, QLineEdit,
                               QAction, QTabWidget, QWidget, QVBoxLayout,
                               QPushButton)
from PySide2.QtGui import QIcon
from PySide2.QtCore import QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SaFan Browser")
        self.resize(1024, 768)

        # 创建主部件和布局
        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        # 添加初始标签页
        self.add_new_tab(QUrl("https://www.google.com"), "主页")

        self.setCentralWidget(self.browser_tabs)

        # 创建导航栏
        self.create_navigation_bar()

        # 添加新标签页按钮
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.browser_tabs.setCornerWidget(new_tab_btn, Qt.TopRightCorner)

    def create_navigation_bar(self):
        """创建导航工具栏"""
        nav_toolbar = QToolBar("导航栏")
        self.addToolBar(nav_toolbar)

        # 后退按钮
        back_btn = QAction(QIcon.fromTheme("go-previous"), "后退", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav_toolbar.addAction(back_btn)

        # 前进按钮
        forward_btn = QAction(QIcon.fromTheme("go-next"), "前进", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav_toolbar.addAction(forward_btn)

        # 刷新按钮
        refresh_btn = QAction(QIcon.fromTheme("view-refresh"), "刷新", self)
        refresh_btn.triggered.connect(lambda: self.current_browser().reload())
        nav_toolbar.addAction(refresh_btn)

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        # 主页按钮
        home_btn = QAction(QIcon.fromTheme("go-home"), "主页", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(home_btn)

    def current_browser(self):
        """获取当前标签页的浏览器部件"""
        return self.browser_tabs.currentWidget()

    def add_new_tab(self, qurl=None, label="新标签页"):
        """添加新标签页"""
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # 连接信号
        browser.urlChanged.connect(self.update_urlbar)
        browser.loadFinished.connect(self.update_title)

        # 添加标签页
        index = self.browser_tabs.addTab(browser, label)
        self.browser_tabs.setCurrentIndex(index)

    def close_tab(self, index):
        """关闭标签页"""
        if self.browser_tabs.count() < 2:
            return

        widget = self.browser_tabs.widget(index)
        widget.deleteLater()
        self.browser_tabs.removeTab(index)

    def navigate_home(self):
        """导航到主页"""
        self.current_browser().setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        """导航到地址栏中的URL"""
        url_text = self.url_bar.text()

        if not url_text.startswith(("http://", "https://")):
            url_text = "http://" + url_text

        self.current_browser().setUrl(QUrl(url_text))

    def update_urlbar(self, q):
        """更新地址栏"""
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self):
        """更新标签页标题"""
        title = self.current_browser().page().title()
        index = self.browser_tabs.currentIndex()
        self.browser_tabs.setTabText(index, title[:15] + "..." if len(title) > 15 else title)
        self.setWindowTitle(f"{title} - SaFan Browser")