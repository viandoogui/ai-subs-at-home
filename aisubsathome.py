from yt_dlp import YoutubeDL

class Downloader:
    def __init__(self):
        self.token = ""
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}]})

    def main(self):
        self.yt.download(['https://www.youtube.com/watch?v=DnbKwHEQ1mA'])
        print(self.yt.prepare_filename(self.yt.extract_info("https://www.youtube.com/watch?v=DnbKwHEQ1mA")))

d = Downloader()
d.main()