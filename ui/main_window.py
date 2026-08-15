from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
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

    def _create_ui(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("ChapterSplit")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = title.font()
        font.setPointSize(24)
        font.setBold(True)
        title.setFont(font)

        subtitle = QLabel(
            "Smart YouTube Chapter Downloader"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()