import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setApplicationName("ChapterSplit")
    app.setApplicationDisplayName("ChapterSplit")
    app.setOrganizationName("HaniHere")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())