import sys
from PySide2.QtWidgets import QApplication
from browser_window import BrowserWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SaFan Browser")
    app.setApplicationVersion("1.0.0")

    browser = BrowserWindow()
    browser.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()