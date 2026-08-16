from pathlib import Path
import subprocess


class Downloader:
    def __init__(self, output_folder: str):
        self.output_folder = Path(output_folder)

    def download(
    self,
    url: str,
    progress_callback=None,
    log_callback=None,
):
        if log_callback:
         log_callback("Preparing download...")

        if progress_callback:
            progress_callback(5)

        if not url.strip():
            return False, "Please enter a YouTube URL."

        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True, exist_ok=True)

        command = [
            "yt-dlp",
            "--extractor-args",
            "youtube:player_client=android",
            "-x",
            "--audio-format",
            "mp3",
            "--split-chapters",
            "-o",
            "%(title)s/%(section_number)03d - %(section_title)s.%(ext)s",
            url,
        ]

        try:
            if log_callback:
                log_callback("Downloading and splitting...")
            result = subprocess.run(
    command,
    cwd=self.output_folder,
)
            if progress_callback:
                progress_callback(100)

            if log_callback:
                if result.returncode == 0:
                    log_callback("Finished successfully.")
                else:
                    log_callback("Download failed.")

            if result.returncode == 0:
                return True, "Download completed successfully."

            return False, "Download failed."

        except FileNotFoundError:
            return False, "yt-dlp was not found."

        except Exception as e:
            return False, str(e)
        