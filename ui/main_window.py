from PySide6.QtCore import Qt, QThread
from core.worker import DownloadWorker
from core.downloader import Downloader
from utils.dialogs import select_folder
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QPlainTextEdit,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChapterSplit")
        self.resize(1000, 650)

        self._create_ui()
        self.browse_button.clicked.connect(self.choose_folder)
        self.download_button.clicked.connect(self.start_download)

    def _create_ui(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(25, 20, 25, 20)
        root.setSpacing(18)

        title = QLabel("ChapterSplit")
        font = title.font()
        font.setPointSize(24)
        font.setBold(True)
        title.setFont(font)

        subtitle = QLabel("Smart YouTube Chapter Downloader")

        root.addWidget(title)
        root.addWidget(subtitle)

        form = QFrame()
        layout = QGridLayout(form)
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(10)

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Paste YouTube URL...")

        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText("Choose output folder...")

        self.browse_button = QPushButton("Browse")

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(self.browse_button)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Logs will appear here...")

        self.download_button = QPushButton("Download")

        layout.addWidget(QLabel("YouTube URL"), 0, 0)
        layout.addWidget(self.url_edit, 1, 0)

        layout.addWidget(QLabel("Output Folder"), 2, 0)
        layout.addLayout(folder_layout, 3, 0)

        layout.addWidget(QLabel("Progress"), 4, 0)
        layout.addWidget(self.progress, 5, 0)

        layout.addWidget(QLabel("Logs"), 6, 0)
        layout.addWidget(self.log, 7, 0)

        root.addWidget(form)
        root.addStretch()

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.download_button)

        root.addLayout(button_row)

    def choose_folder(self):
        folder = select_folder(self)

        if folder:
            self.folder_edit.setText(folder)

    def start_download(self):
        url = self.url_edit.text().strip()
        folder = self.folder_edit.text().strip()

        self.log.clear()

        if not url:
            self.log.appendPlainText("Please enter a YouTube URL.")
            return

        if not folder:
            self.log.appendPlainText("Please choose an output folder.")
            return

        self.download_button.setEnabled(False)
        self.download_button.setText("Downloading...")

        self.progress.setRange(0, 0)
        self.log.clear()

        downloader = Downloader(folder)

        self.thread = QThread()
        self.worker = DownloadWorker(downloader, url)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.log.connect(self.log.appendPlainText)

        self.worker.finished.connect(self.download_finished)

        self.worker.finished.connect(self.thread.quit)

        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)

        self.thread.start()
    def download_finished(self, success, message):
        self.progress.setRange(0, 100)

        if success:
            self.progress.setValue(100)
        else:
            self.progress.setValue(0)

        self.log.appendPlainText(message)

        self.download_button.setEnabled(True)
        self.download_button.setText("Download")