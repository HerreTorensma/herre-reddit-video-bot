import youtube_dl

class VideoDownloader:
	def __init__(self, directory, urls):
		self.directory = directory
		self.urls = urls

	def download_videos(self):
		ydl = youtube_dl.YoutubeDL({"outtmpl": f"{self.directory}/%(id)s.%(ext)s"})

		with ydl:
			for url in self.urls:
				ydl.download([url])

		print("Downloaded videos.")