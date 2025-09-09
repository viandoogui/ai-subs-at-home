from yt_dlp import YoutubeDL
import os
import shutil

class Downloader:
    def __init__(self):
        self.token = None
        self.yt = YoutubeDL({"postprocessors":[{"key":"FFmpegExtractAudio"}],"outtmpl":"%(title)s.%(ext)s", "format":"bestaudio"})
        self.video_link = ""
        self.subs_dir = os.path.abspath("")

    def generate_subs(self, filename):
        #you can paste the python api code from another hugging face space (using gradio) here then modify the parameters
        from gradio_client import Client, handle_file
        client = Client("viandoogui/Auto-Subtitle-Generator", hf_token=self.token)
        result = client.predict(
		media_file=handle_file(os.path.normpath(os.path.join(os.path.dirname(__file__), filename + ".opus"))),
		source_lang="Japanese",
		target_lang="Japanese",
		api_name="/subtitle_maker")
        #this will vary depending on what the output is from above
        output_path = os.path.normpath(result[0])
        shutil.move(output_path, self.subs_dir + "/" + filename + ".srt")
        os.remove(filename + ".opus")

    def main(self):
        info = self.yt.extract_info(self.video_link)
        filename = info["title"]
        self.generate_subs(filename)

d = Downloader()
d.main()