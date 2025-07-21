from PySide2.QtWidgets import (QMainWindow, QToolBar, QLineEdit, QAction, QMenu, QStatusBar,
                               QFileDialog, QMessageBox, QLabel)
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import QUrl, QSize
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineProfile, QWebEngineDownloadItem
from tab_widget import TabWidget
from bookmarks import BookmarkManager
from SaFan.history import HistoryManager
import os


class BrowserWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SaFan Browser")
        self.resize(1280, 800)

        # 创建主部件
        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)

        # 连接信号
        self.tab_widget.url_changed.connect(self.update_url_bar)
        self.tab_widget.title_changed.connect(self.update_title)
        self.tab_widget.load_progress.connect(self.update_progress)

        # 初始化管理器
        self.bookmark_manager = BookmarkManager()
        self.history_manager = HistoryManager()

        # 创建UI
        self.create_actions()
        self.create_toolbar()
        self.create_status_bar()

        # 添加初始标签页 - 必须在创建工具栏之后
        self.tab_widget.add_new_tab(QUrl("https://www.baidu.com"), "主页")

        # 设置下载处理器
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download_request)

    def create_actions(self):
        """创建菜单动作"""
        # 文件菜单
        self.new_tab_action = QAction(QIcon("resources/icons/new_tab.png"), "新建标签页", self)
        self.new_tab_action.setShortcut(QKeySequence.AddTab)
        self.new_tab_action.triggered.connect(self.tab_widget.add_new_tab)

        self.new_window_action = QAction(QIcon("resources/icons/new_window.png"), "新建窗口", self)
        self.new_window_action.setShortcut("Ctrl+N")
        self.new_window_action.triggered.connect(self.new_window)

        self.private_mode_action = QAction(QIcon("resources/icons/private.png"), "隐私浏览", self)
        self.private_mode_action.setShortcut("Ctrl+Shift+P")
        self.private_mode_action.triggered.connect(self.toggle_private_mode)

        self.close_action = QAction("关闭", self)
        self.close_action.setShortcut("Ctrl+W")
        self.close_action.triggered.connect(self.close)

        # 编辑菜单
        self.cut_action = QAction(QIcon("resources/icons/cut.png"), "剪切", self)
        self.cut_action.setShortcut(QKeySequence.Cut)

        self.copy_action = QAction(QIcon("resources/icons/copy.png"), "复制", self)
        self.copy_action.setShortcut(QKeySequence.Copy)

        self.paste_action = QAction(QIcon("resources/icons/paste.png"), "粘贴", self)
        self.paste_action.setShortcut(QKeySequence.Paste)

        # 视图菜单
        self.zoom_in_action = QAction(QIcon("resources/icons/zoom_in.png"), "放大", self)
        self.zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        self.zoom_out_action = QAction(QIcon("resources/icons/zoom_out.png"), "缩小", self)
        self.zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        self.zoom_out_action.triggered.connect(self.zoom_out)

        self.reset_zoom_action = QAction("重置缩放", self)
        self.reset_zoom_action.setShortcut("Ctrl+0")
        self.reset_zoom_action.triggered.connect(self.reset_zoom)

        # 书签菜单
        self.bookmark_page_action = QAction(QIcon("resources/icons/bookmark.png"), "添加书签", self)
        self.bookmark_page_action.setShortcut("Ctrl+D")
        self.bookmark_page_action.triggered.connect(self.bookmark_current_page)

        self.show_bookmarks_action = QAction(QIcon("resources/icons/bookmarks.png"), "书签管理器", self)
        self.show_bookmarks_action.setShortcut("Ctrl+Shift+B")
        self.show_bookmarks_action.triggered.connect(self.show_bookmarks_manager)

        # 工具菜单
        self.downloads_action = QAction(QIcon("resources/icons/downloads.png"), "下载内容", self)
        self.downloads_action.setShortcut("Ctrl+J")
        self.downloads_action.triggered.connect(self.show_downloads_manager)

        self.history_action = QAction(QIcon("resources/icons/history.png"), "历史记录", self)
        self.history_action.setShortcut("Ctrl+H")
        self.history_action.triggered.connect(self.show_history_manager)

        self.developer_tools_action = QAction(QIcon("resources/icons/dev_tools.png"), "开发者工具", self)
        self.developer_tools_action.setShortcut("F12")
        self.developer_tools_action.triggered.connect(self.toggle_developer_tools)

    def create_toolbar(self):
        """创建导航工具栏"""
        nav_toolbar = QToolBar("导航栏")
        nav_toolbar.setIconSize(QSize(20, 20))
        nav_toolbar.setMovable(False)
        self.addToolBar(nav_toolbar)

        # 后退按钮
        self.back_btn = QAction(QIcon("resources/icons/back.png"), "后退", self)
        self.back_btn.setShortcut(QKeySequence.Back)
        self.back_btn.triggered.connect(self.back)
        nav_toolbar.addAction(self.back_btn)

        # 前进按钮
        self.forward_btn = QAction(QIcon("resources/icons/forward.png"), "前进", self)
        self.forward_btn.setShortcut(QKeySequence.Forward)
        self.forward_btn.triggered.connect(self.forward)
        nav_toolbar.addAction(self.forward_btn)

        # 刷新按钮
        self.refresh_btn = QAction(QIcon("resources/icons/refresh.png"), "刷新", self)
        self.refresh_btn.setShortcut(QKeySequence.Refresh)
        self.refresh_btn.triggered.connect(self.reload)
        nav_toolbar.addAction(self.refresh_btn)

        # 停止按钮
        self.stop_btn = QAction(QIcon("resources/icons/stop.png"), "停止", self)
        self.stop_btn.triggered.connect(self.stop)
        nav_toolbar.addAction(self.stop_btn)

        # 主页按钮
        self.home_btn = QAction(QIcon("resources/icons/home.png"), "主页", self)
        self.home_btn.triggered.connect(self.navigate_home)
        nav_toolbar.addAction(self.home_btn)

        nav_toolbar.addSeparator()

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索内容")
        self.url_bar.setMinimumWidth(400)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_toolbar.addWidget(self.url_bar)

        nav_toolbar.addSeparator()

        # 书签按钮
        self.bookmark_btn = QAction(QIcon("resources/icons/bookmark.png"), "书签", self)
        self.bookmark_btn.triggered.connect(self.bookmark_current_page)
        nav_toolbar.addAction(self.bookmark_btn)

        # 下载按钮
        self.downloads_btn = QAction(QIcon("resources/icons/downloads.png"), "下载", self)
        self.downloads_btn.triggered.connect(self.show_downloads_manager)
        nav_toolbar.addAction(self.downloads_btn)

        # 菜单按钮
        self.menu_btn = QAction(QIcon("resources/icons/menu.png"), "菜单", self)
        self.menu_btn.triggered.connect(self.show_app_menu)
        nav_toolbar.addAction(self.menu_btn)

    def create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        self.progress_label = QLabel("就绪")
        status_bar.addWidget(self.progress_label)

        self.secure_label = QLabel()
        status_bar.addPermanentWidget(self.secure_label)

    # 导航相关方法
    def back(self):
        """后退"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.back()

    def forward(self):
        """前进"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.forward()

    def reload(self):
        """刷新"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.reload()

    def stop(self):
        """停止加载"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.stop()

    def navigate_to_url(self):
        """导航到地址栏中的URL"""
        url_text = self.url_bar.text().strip()

        if not url_text:
            return

        browser = self.tab_widget.current_browser()
        if not browser:
            return

        # 尝试处理为URL
        if "." in url_text and " " not in url_text:
            if not url_text.startswith(("http://", "https://")):
                url_text = "https://" + url_text
            browser.setUrl(QUrl(url_text))
        else:
            # 作为搜索查询
            search_url = f"https://www.baidu.com/baidu?ie=utf-8&wd={url_text.replace(' ', '+')}"
            browser.setUrl(QUrl(search_url))

    def navigate_home(self):
        """导航到主页"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.setUrl(QUrl("https://www.baidu.com"))

    def update_url_bar(self, url):
        """更新地址栏"""
        if self.tab_widget.current_browser() == self.sender():
            self.url_bar.setText(url.toString())
            self.url_bar.setCursorPosition(0)

            # 更新安全状态
            if url.scheme() == "https":
                self.secure_label.setText("安全连接 🔒")
            else:
                self.secure_label.setText("不安全连接")

    def update_title(self, title):
        """更新窗口标题"""
        if self.tab_widget.current_browser() == self.sender():
            self.setWindowTitle(f"{title} - SaFan Browser")

    def update_progress(self, progress):
        """更新加载进度"""
        if progress < 100:
            self.progress_label.setText(f"加载中... {progress}%")
        else:
            self.progress_label.setText("就绪")

    def bookmark_current_page(self):
        """添加当前页面到书签"""
        browser = self.tab_widget.current_browser()
        if not browser:
            return

        current_url = browser.url().toString()
        current_title = browser.title()

        self.bookmark_manager.add_bookmark(current_title, current_url)
        QMessageBox.information(self, "书签已添加", f"已添加 '{current_title}' 到书签")

    def show_bookmarks_manager(self):
        """显示书签管理器"""
        self.bookmark_manager.show()

    def show_history_manager(self):
        """显示历史记录管理器"""
        self.history_manager.show()

    def show_downloads_manager(self):
        """显示下载管理器"""
        self.download_manager.show()

    def toggle_developer_tools(self):
        """切换开发者工具"""
        browser = self.tab_widget.current_browser()
        if not browser:
            return

        if browser.page().devToolsPage():
            browser.page().setDevToolsPage(None)
        else:
            browser.page().setDevToolsPage(QWebEnginePage())

    def handle_download_request(self, download: QWebEngineDownloadItem):
        """处理下载请求"""
        # 获取下载目录
        download_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

        # 构建默认保存路径
        default_path = os.path.join(download_dir, download.suggestedFileName())

        # 弹出保存对话框
        path, _ = QFileDialog.getSaveFileName(
            self, "保存文件",
            default_path
        )

        if path:
            download.setPath(path)
            download.accept()
            self.download_manager.add_download(download)

    def zoom_in(self):
        """放大页面"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)

    def zoom_out(self):
        """缩小页面"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.setZoomFactor(max(0.1, browser.zoomFactor() - 0.1))

    def reset_zoom(self):
        """重置缩放"""
        browser = self.tab_widget.current_browser()
        if browser:
            browser.setZoomFactor(1.0)

    def toggle_private_mode(self):
        """切换隐私浏览模式"""
        # 在实际应用中，这里会创建一个新的隐私窗口
        QMessageBox.information(self, "隐私浏览", "隐私浏览模式已启用。在此模式下，不会保存浏览历史、Cookie 或搜索记录。")

    def new_window(self):
        """创建新窗口"""
        new_browser = BrowserWindow()
        new_browser.show()

    def show_app_menu(self):
        """显示应用菜单"""
        menu = QMenu(self)

        # 文件菜单
        file_menu = menu.addMenu("文件")
        file_menu.addAction(self.new_tab_action)
        file_menu.addAction(self.new_window_action)
        file_menu.addAction(self.private_mode_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_action)

        # 编辑菜单
        edit_menu = menu.addMenu("编辑")
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)

        # 视图菜单
        view_menu = menu.addMenu("视图")
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.reset_zoom_action)

        # 书签菜单
        bookmarks_menu = menu.addMenu("书签")
        bookmarks_menu.addAction(self.bookmark_page_action)
        bookmarks_menu.addAction(self.show_bookmarks_action)

        # 工具菜单
        tools_menu = menu.addMenu("工具")
        tools_menu.addAction(self.downloads_action)
        tools_menu.addAction(self.history_action)
        tools_menu.addAction(self.developer_tools_action)

        # 显示菜单
        menu.exec_(self.sender().parent().mapToGlobal(self.sender().geometry().bottomLeft()))