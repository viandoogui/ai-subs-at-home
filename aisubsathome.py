from yt_dlp import YoutubeDL
import os
import shutil
from gradio_client import Client, handle_file
import httpx

class Downloader:
    def __init__(self):
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}], "outtmpl":"%(title)s.%(ext)s", "format":"bestaudio", "progress_hooks":[self.name_hook]})
        self.subs_dir = os.path.abspath("C:/Users/bob/Downloads/subtitles") #put your own output directory here, with forward slashes
        self.gradio_link = "" 
        self.video_link = "" 
        self.curr_title = ""
        self.prev_title = ""
        self.title_list = []
        self.ext_list = []

    def name_hook(self, data):
        self.prev_title = self.curr_title
        self.curr_title, _ = os.path.splitext(data["info_dict"]["_filename"])
        if self.prev_title != self.curr_title:
            self.title_list.append(self.curr_title)

    def set_link(self, link):
        self.video_link = link

    def generate_subs(self, filename, vid_ext, subdir):
        #Get the gradio link by running this: https://colab.research.google.com/drive/1pJ7aQOT432yJzVCEdapajTkW093x0iea?usp=sharing
        client = Client(self.gradio_link)
        client.httpx_kwargs["timeout"] = httpx.Timeout(50000)
        result = client.predict(
        media_file=handle_file(os.path.normpath(os.path.join(os.path.dirname(__file__), filename + "." + vid_ext))),
        source_lang="Japanese",
        target_lang="Japanese",
        align=True,
        api_name="/subtitle_maker",
        )
        print(result)

        output_path = os.path.normpath(result)
        if subdir == None:
            final_dir = self.subs_dir + "/" + filename + ".srt"
        else:
            final_dir = self.subs_dir + "/" + subdir + "/" + filename + ".srt"
        shutil.move(output_path, final_dir)
        os.remove(filename + "." + vid_ext)
        print("Subtitle file saved to " + final_dir.replace("\\","/"))
        client.close()

    def main(self):
        info_dict = self.yt.extract_info(self.video_link, download=True)

        if info_dict.get("entries") == None:
            self.vid_ext = info_dict["requested_downloads"][0]["ext"]
            self.generate_subs(self.curr_title, self.vid_ext, None)
        else:
            playlist_title = info_dict["title"]
            os.mkdir(os.path.join(self.subs_dir, playlist_title))
            playlist_length = len(info_dict["entries"])
            for video in info_dict["entries"]:
                self.ext_list.append(video["requested_downloads"][0]["ext"])
            for i in range(len(self.title_list)):
                print(f"Playlist Progress: {i+1} of {playlist_length} videos")
                self.generate_subs(self.title_list[i], self.ext_list[i], playlist_title)

        self.title_list.clear()
        self.ext_list.clear()
        self.prev_title = ""
        self.curr_title = ""
        
d = Downloader()

d.gradio_link = input("Input the current gradio link: ")

while True:
    link = input("Input a Youtube video or playlist link: ")
    d.set_link(link)
    d.main()