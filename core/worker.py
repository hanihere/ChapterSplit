from PySide6.QtCore import QObject, Signal


class DownloadWorker(QObject):
    finished = Signal(bool)
    progress = Signal(int)
    log = Signal(str)

    def __init__(self, downloader, url):
        super().__init__()
        self.downloader = downloader
        self.url = url

    def run(self):
        self.log.emit("Starting download...")

        success = self.downloader.download(
            self.url,
            progress_callback=self.progress.emit,
            log_callback=self.log.emit,
        )

        self.finished.emit(success)