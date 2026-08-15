from core.downloader import Downloader

downloader = Downloader(r"C:\Users\haniy\Music\YouTube Jukebox")

url = input("Paste YouTube URL: ")

success = downloader.download(url)

if success:
    print("\n✅ Download completed successfully.")
else:
    print("\n❌ Download failed.")