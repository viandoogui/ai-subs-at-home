from yt_dlp import YoutubeDL
import os
import shutil
from gradio_client import Client, handle_file

class Downloader:
    def __init__(self):
        self.gradio_link = "" 
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}], "outtmpl":"%(title)s.%(ext)s", "format":"bestaudio", "progress_hooks":[self.name_hook]})
        self.subs_dir = os.path.abspath("C:/Users/bob/Downloads/subtitles/") #put your own output directory here, with forward slashes
        self.vid_link = "" 
        self.vid_title = ""

    def name_hook(self, data):
        self.vid_title, ext = os.path.splitext(data["info_dict"]["_filename"])

    def set_link(self, link):
        self.vid_link = link

    def generate_subs(self, filename):
        #Get the link by running this: https://colab.research.google.com/drive/18K_U1uCSHtiFTKNyoZDjBUwa9tT15xpn?usp=sharing
        client = Client(self.gradio_link)
        result = client.predict(
        media_file=handle_file(os.path.normpath(os.path.join(os.path.dirname(__file__), filename + ".opus"))),
        source_lang="Japanese",
        target_lang="Japanese",
        align=True,
        api_name="/subtitle_maker"
        )
        print(result)

        output_path = os.path.normpath(result)
        shutil.move(output_path, self.subs_dir + "/" + filename + ".srt")
        os.remove(filename + ".opus")
        client.close()

    def main(self):
        try:
            self.yt.download(self.vid_link)
        except:
            print("Download failed, try again or update yt-dlp using 'pip install yt-dlp --upgrade'")
            return None
        self.generate_subs(self.vid_title)
        
d = Downloader()

d.gradio_link = input("Enter the current gradio link: ")

while True:
    link = input("Enter a Youtube link: ")
    d.set_link(link)
    d.main()