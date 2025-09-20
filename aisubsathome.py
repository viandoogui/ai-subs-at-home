from yt_dlp import YoutubeDL
import os
import shutil

class Downloader:
    def __init__(self):
        self.token = "" #make a hugging face account, generate an access token, then paste it here
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}],"outtmpl":"%(title)s.%(ext)s", "format":"bestaudio"})
        self.video_link = "" 
        self.subs_dir = os.path.abspath("C:/Users/bob/Downloads/subtitles/") #put your own output directory here, with forward slashes

    def set_link(self, link):
        self.video_link = link

    def generate_subs(self, filename):
        from gradio_client import Client, handle_file
        #each free hf user can use 3 free minutes of ZeroGPU a day with this space
        #the site tells you 4, but 1 is blocked out at runtime by default, since computing may or may not finish
        #as long as you stay under 3 out of 4 minutes of the day (check!), it should work fine
        client = Client("viandoogui/kotoba-japanese-srt", hf_token=self.token)
        result = client.predict(
                audio=handle_file(os.path.normpath(os.path.join(os.path.dirname(__file__), filename + ".opus"))),
                task="transcribe",
                api_name="/test"
        )
        print(result)
        output_path = os.path.normpath(result[1])
        shutil.move(output_path, self.subs_dir + "/" + filename + ".srt")
        os.remove(filename + ".opus")

    def main(self):
        info = self.yt.extract_info(self.video_link)
        filename = info["title"]
        self.generate_subs(filename)

d = Downloader()

while True:
    link = input("Enter a Youtube link: ")
    d.set_link(link)
    d.main()