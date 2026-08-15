from pathlib import Path
import subprocess


class Downloader:
    def __init__(self, output_folder: str):
        self.output_folder = Path(output_folder)

    def download(self, url: str):
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
            str(self.output_folder / "%(title)s/%(section_number)03d - %(section_title)s.%(ext)s"),
            url,
        ]

        result = subprocess.run(command)

        return result.returncode == 0