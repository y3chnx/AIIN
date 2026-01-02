import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QTabWidget, QLabel, QStatusBar,
    QToolButton, QWidget, QVBoxLayout,
    QProgressBar, QMenu, QWidgetAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
import threading
import time
sys.path.append(os.path.dirname(__file__))

def start_flask_server():
    try:
        print("🔹 Starting Flask server...")
        from ai_engine import start_ai_engine
        start_ai_engine()
    except Exception as e:
        print(f"❌ Flask server start failed: {e}")
        import traceback
        traceback.print_exc()

flask_thread = threading.Thread(
    target=start_flask_server,
    daemon=True
)
flask_thread.start()

print("⏳ Waiting for Flask server to start...")
time.sleep(3)

import socket
for i in range(10):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 5137))
        sock.close()
        if result == 0:
            print("✅ Flask server ready!")
            break
    except:
        pass
    time.sleep(0.5)
else:
    print("⚠️ Flask server check failed, proceeding...")

class DownloadItem(QWidget):
    def __init__(self, download):
        super().__init__()
        self.download = download

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        self.label = QLabel(download.downloadFileName())
        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        download.downloadProgress.connect(self.update_progress)
        download.finished.connect(self.finished)

    def update_progress(self, received, total):
        if total > 0:
            self.progress.setValue(int(received / total * 100))

    def finished(self):
        self.progress.setValue(100)
        self.label.setText(self.label.text() + " ✔")
        self.progress.mousePressEvent = lambda e: QDesktopServices.openUrl(
            QUrl.fromLocalFile(os.path.dirname(self.download.path()))
        )

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loading = False
        self.fullscreen_browser = None

        self.setWindowTitle("AIIN")
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet("""
        QMainWindow { background-color: #202124; }
        QToolBar { background: #2b2d31; border: none; padding: 6px; }
        QLineEdit {
            background: #202124;
            color: #e8eaed;
            border-radius: 20px;
            padding: 8px 14px;
            border: 1px solid #5f6368;
            min-width: 520px;
            font-size: 14px;
        }
        QLineEdit:focus { border: 1px solid #8ab4f8; }
        QTabBar::tab {
            background: #2b2d31;
            color: #9aa0a6;
            padding: 8px 14px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar::tab:selected {
            background: #202124;
            color: #e8eaed;
        }
        QTabBar::tab:hover { background: #3c4043; }
        QStatusBar {
            background: #2b2d31;
            color: #e8eaed;
        }
        """)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.back_btn = self.make_button("◀", lambda: self.current_browser().back())
        self.forward_btn = self.make_button("▶", lambda: self.current_browser().forward())
        self.reload_btn = self.make_button("⟳", self.reload_or_stop)

        self.toolbar.addWidget(self.back_btn)
        self.toolbar.addWidget(self.forward_btn)
        self.toolbar.addWidget(self.reload_btn)

        self.security_icon = QLabel("🔒")
        self.security_icon.setFixedSize(44, 44)
        self.security_icon.setAlignment(Qt.AlignCenter)
        self.security_icon.setStyleSheet("font-size:18px;")
        self.toolbar.addWidget(self.security_icon)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter address")
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

        self.download_btn = self.make_button("⬇", None)
        self.download_btn.setPopupMode(QToolButton.InstantPopup)
        self.download_menu = QMenu()
        self.download_btn.setMenu(self.download_menu)
        self.toolbar.addWidget(self.download_btn)

        self.new_tab_btn = self.make_button("+", self.add_tab)
        self.toolbar.addWidget(self.new_tab_btn)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        self.add_tab()

    def make_button(self, text, callback):
        btn = QToolButton()
        btn.setText(text)
        btn.setFixedSize(48, 48)
        btn.setStyleSheet("""
            QToolButton {
                font-size: 22px;
                border-radius: 12px;
                color: #e8eaed;
            }
            QToolButton:hover { background: #3c4043; }
        """)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def add_tab(self, qurl=None):
        browser = QWebEngineView()

        browser.page().fullScreenRequested.connect(self.handle_fullscreen)

        browser.setUrl(
            qurl if isinstance(qurl, QUrl)
            else QUrl("http://127.0.0.1:5137/new.html")
        )

        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda q, b=browser: self.on_url_changed(b, q))
        browser.loadStarted.connect(self.on_load_started)
        browser.loadFinished.connect(self.on_load_finished)
        browser.titleChanged.connect(lambda t, b=browser: self.set_tab_title(b, t))
        browser.iconChanged.connect(lambda i, b=browser: self.set_tab_icon(b, i))

    def current_browser(self):
        return self.tabs.currentWidget()

    def update_url_bar(self):
        browser = self.current_browser()
        if browser:
            self.on_url_changed(browser, browser.url())

    def on_url_changed(self, browser, qurl):
        if browser != self.current_browser():
            return

        url_str = qurl.toString()
        
        if url_str.startswith("http://127.0.0.1:5137/new"):
            self.url_bar.clear()
            self.security_icon.setText("🛌")
            return

        self.url_bar.setText(url_str)
        self.security_icon.setText("🔒" if qurl.scheme() == "https" else "⚠️")

    def on_load_started(self):
        self.loading = True
        self.reload_btn.setText("⏹")

    def on_load_finished(self):
        self.loading = False
        self.reload_btn.setText("⟳")

    def reload_or_stop(self):
        browser = self.current_browser()
        if self.loading:
            browser.stop()
        else:
            browser.reload()

    def handle_fullscreen(self, request):
        request.accept()
        browser = self.sender().view()

        if request.toggleOn():
            self.fullscreen_browser = browser
            self.toolbar.hide()
            self.tabs.hide()
            browser.setParent(None)
            self.setCentralWidget(browser)
            self.showFullScreen()
        else:
            self.showNormal()
            self.toolbar.show()
            self.tabs.show()
            self.setCentralWidget(self.tabs)
            self.fullscreen_browser = None

    def handle_download(self, download):
        path = os.path.join(
            os.path.expanduser("~/Downloads"),
            download.downloadFileName()
        )
        download.setPath(path)
        download.accept()

        item = DownloadItem(download)
        action = QWidgetAction(self.download_menu)
        action.setDefaultWidget(item)
        self.download_menu.addAction(action)

    def set_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1 and title:
            self.tabs.setTabText(index, title)

    def set_tab_icon(self, browser, icon):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabIcon(index, icon)

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://", "file://")):
            url = "https://" + url
        self.current_browser().setUrl(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())