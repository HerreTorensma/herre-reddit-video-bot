import youtube_dl
import requests
from PIL import Image
import shutil

class ContentDownloader:
	def __init__(self, directory, urls):
		self.directory = directory
		self.urls = urls

	def download_videos(self):
		ydl = youtube_dl.YoutubeDL({"outtmpl": f"{self.directory}/%(id)s.%(ext)s"})

		with ydl:
			for url in self.urls:
				ydl.download([url])

		print("Downloaded videos.")

	def download_images(self):
		for i in range(len(self.urls)):
			response = requests.get(self.urls[i], stream=True)

			if response.status_code == 200:
				extension = self.urls[i].split(".")[-1]
				filename = f"{self.directory}/{i}.{extension}"
				with open(filename, "wb") as file:
					shutil.copyfileobj(response.raw, file)
