from yt_dlp import YoutubeDL
import os
import shutil
from gradio_client import Client, handle_file
import httpx

class Downloader:
    def __init__(self):
        self.gradio_link = "" 
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}], "outtmpl":"%(title)s.%(ext)s", "format":"bestaudio", "progress_hooks":[self.name_hook]})
        self.subs_dir = os.path.abspath("C:/Users/bob/Downloads/subtitles") #put your own output directory here, with forward slashes
        self.vid_link = "" 
        self.vid_title = ""
        self.vid_ext = ""

    def name_hook(self, data):
        self.vid_title, self.vid_ext = os.path.splitext(data["info_dict"]["_filename"])

    def set_link(self, link):
        self.vid_link = link

    def generate_subs(self, filename):
        #Get the link by running this: https://colab.research.google.com/drive/1pJ7aQOT432yJzVCEdapajTkW093x0iea?usp=sharing
        client = Client(self.gradio_link)
        client.httpx_kwargs["timeout"] = httpx.Timeout(50)
        result = client.predict(
        media_file=handle_file(os.path.normpath(os.path.join(os.path.dirname(__file__), filename + "." + self.vid_ext))),
        source_lang="Japanese",
        target_lang="Japanese",
        align=True,
        api_name="/subtitle_maker",
        )
        print(result)

        output_path = os.path.normpath(result)
        final_dir = self.subs_dir + "/" + filename + ".srt"
        shutil.move(output_path, final_dir)
        os.remove(filename + "." + self.vid_ext)
        print("Subtitle file saved to " + final_dir.replace("\\","/"))
        client.close()

    def main(self):
        info_dict = self.yt.extract_info(self.vid_link, download=True)
        self.vid_ext = info_dict["requested_downloads"][0]["ext"]
        self.generate_subs(self.vid_title)
        
d = Downloader()

d.gradio_link = input("Enter the current gradio link: ")

while True:
    link = input("Enter a Youtube link: ")
    d.set_link(link)
    d.main()