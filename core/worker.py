from PySide6.QtCore import QObject, Signal


class DownloadWorker(QObject):
    finished = Signal(bool, str)
    log = Signal(str)

    def __init__(self, downloader, url):
        super().__init__()
        self.downloader = downloader
        self.url = url

    def run(self):
        success, message = self.downloader.download(
            self.url,
            log_callback=self.log.emit,
        )

        print("EMITTING:", success, message)
        self.finished.emit(success, message)
        print("EMITTED")