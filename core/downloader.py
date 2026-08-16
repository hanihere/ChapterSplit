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
        if not url.strip():
            return False, "Please enter a YouTube URL."

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
            if progress_callback:
                progress_callback(5)

            if log_callback:
                log_callback("Starting yt-dlp...")

            process = subprocess.Popen(
                command,
                cwd=self.output_folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            last_status = ""

            for line in process.stdout:
                line = line.strip()

                if not line:
                    continue

                status = None

                if "[youtube]" in line:
                    status = "🔍 Analyzing video..."

                elif "[download]" in line:
                    status = "⬇ Downloading audio..."

                elif "ExtractAudio" in line:
                    status = "🎵 Converting to MP3..."

                elif "SplitChapters" in line:
                    status = "✂ Splitting chapters..."

                elif "Deleting original file" in line:
                    status = "🧹 Cleaning up..."

                if status and status != last_status:
                    last_status = status

                    if log_callback:
                        log_callback(status)

            process.wait()

            if progress_callback:
                progress_callback(100)

            if process.returncode == 0:
                return True, "Download completed successfully."

            return False, "Download failed."

        except FileNotFoundError:
            return False, "yt-dlp was not found."

        except Exception as e:
            return False, str(e)