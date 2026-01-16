from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename
import os
import shutil
from gradio_client import Client, handle_file
import httpx

class Downloader:
    def __init__(self):
        #put your own output directory here, with forward slashes
        self.subs_dir = os.path.abspath("C:/Users/bob/Downloads/subtitles")
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}], "outtmpl":"%(title)s.%(ext)s", "format":"bestaudio", "paths":{"home":self.subs_dir}, "ignoreerrors":True})
        self.gradio_link = "" 
        self.video_link = "" 
        self.title_list = []
        self.ext_list = []
        self.existing = set()

    def generate_subs(self, filename, vid_ext, subdir):
        #Get the gradio link by running this: https://colab.research.google.com/drive/1pJ7aQOT432yJzVCEdapajTkW093x0iea?usp=sharing
        client = Client(self.gradio_link)
        client.httpx_kwargs["timeout"] = httpx.Timeout(50000)
        success = False

        while success == False:
            try:
                print("Current video: " + filename)
                result = client.predict(
                media_file=handle_file(os.path.normpath(os.path.join(self.subs_dir, filename + "." + vid_ext))),
                source_lang="Japanese",
                target_lang="Japanese",
                align=True,
                api_name="/subtitle_maker",
                )
            except:
                choice = input("Gradio connection failed. Try again? (y/n) ").lower()
                while choice != "y" or choice != "yes" or choice != "n" or choice != "no":
                    if choice == "y" or choice == "yes":
                        client.close()
                        client = Client(self.gradio_link)
                        client.httpx_kwargs["timeout"] = httpx.Timeout(50000)
                        break
                    elif choice == "n" or choice == "no":
                        print("Skipping current video...")
                        return
                    else:
                        choice = input("Invalid input, try again! ")
            else:
                output_path = os.path.normpath(result)
                if subdir == None:
                    final_dir = self.subs_dir + "/" + filename + ".srt"
                else:
                    final_dir = self.subs_dir + "/" + subdir + "/" + filename + ".srt"

                shutil.move(output_path, final_dir)
                print("Subtitle file saved to " + final_dir.replace("\\","/"))
                client.close()
                success = True

    def main(self):
        info_dict = self.yt.extract_info(self.video_link, download=True)

        if info_dict.get("entries") == None: #link is a single video
            curr_title, _ = os.path.splitext(os.path.basename(info_dict["requested_downloads"][0]["_filename"]))
            curr_title = sanitize_filename(curr_title)
            vid_ext = info_dict["requested_downloads"][0]["ext"]
            self.generate_subs(curr_title, vid_ext, None)
            os.remove(self.subs_dir + "/" + curr_title + "." + vid_ext)
        else: #link is a playlist
            playlist_title = sanitize_filename(info_dict["title"])
            os.mkdir(os.path.join(self.subs_dir, playlist_title))

            for video in info_dict["entries"]:
                if video != None: #video is not private
                    curr_title, _ = os.path.splitext(os.path.basename(video["requested_downloads"][0]["_filename"]))
                    self.title_list.append(sanitize_filename(curr_title))
                    self.ext_list.append(video["requested_downloads"][0]["ext"])

            playlist_length = len(self.title_list)

            for i in range(playlist_length):
                print(f"Playlist Progress: {i+1} of {playlist_length} videos")
                if self.title_list[i] not in self.existing:
                    self.generate_subs(self.title_list[i], self.ext_list[i], playlist_title)
                    self.existing.add(self.title_list[i])
                else:
                    print("Video is a duplicate, skipping...")

            for i in range(len(self.title_list)):
                if os.path.isfile(self.subs_dir + "/" + self.title_list[i] + "." + self.ext_list[i]):
                    os.remove(self.subs_dir + "/" + self.title_list[i] + "." + self.ext_list[i])

        self.title_list.clear()
        self.ext_list.clear()
        self.existing.clear()
        
d = Downloader()

d.gradio_link = input("Input the current gradio link: ")

while True:
    link = input("Input a Youtube video or playlist link: ")
    d.video_link = link
    d.main()