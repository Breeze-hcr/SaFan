import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QSettings, QStandardPaths
from browser_window import BrowserWindow


def main():
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("SaFan Browser")
    app.setApplicationVersion("2.0.0")

    # 设置应用样式
    apply_styles(app)

    # 创建主窗口
    browser = BrowserWindow()
    browser.show()

    sys.exit(app.exec_())


def apply_styles(app):
    """应用自定义样式表"""
    style_path = os.path.join(os.path.dirname(__file__), "resources", "styles", "dark_theme.qss")
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except:
        # 使用内置的备用样式
        app.setStyleSheet("""
            QMainWindow {
                background-color: #2D2D30;
            }
            QTabWidget::pane {
                border: none;
                background: #252526;
            }
            QTabBar::tab {
                background: #333337;
                color: #CCCCCC;
                padding: 8px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #1E1E1E;
                border-bottom: 2px solid #007ACC;
            }
            QLineEdit {
                background: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #007ACC;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QToolBar {
                background: #333337;
                border: none;
                padding: 5px;
            }
            QToolButton {
                background: transparent;
                border-radius: 4px;
                padding: 5px;
            }
            QToolButton:hover {
                background: #3C3C3C;
            }
            QStatusBar {
                background: #252526;
                color: #A0A0A0;
            }
        """)


if __name__ == "__main__":
    main()