from PIL import Image
import os.path

class ThumbnailMaker:
	def __init__(self, clips, directory):
		self.directory = directory
		self.clips = clips

	def get_vertical_images(self):
		self.clips[0].save_frame(f"{self.directory}/image1.png", 0)
		self.clips[1].save_frame(f"{self.directory}/image2.png", 0)
		self.clips[2].save_frame(f"{self.directory}/image3.png", 0)

	def make_vertical_thumbnail(self, subreddit):
		image1 = Image.open(f"{self.directory}/image1.png")
		image1 = image1.resize((426, 720), Image.NEAREST)
		image2 = Image.open(f"{self.directory}/image2.png")
		image2 = image2.resize((426, 720), Image.NEAREST)
		image3 = Image.open(f"{self.directory}/image3.png")
		image3 = image3.resize((426, 720), Image.NEAREST)

		if os.path.isfile(f"./overlays/{subreddit}.png"):
			overlay = Image.open(f"./overlays/{subreddit}.png")

		thumbnail = Image.new("RGB", (1280, 720), (0, 0, 0))
		thumbnail.paste(image1, (0, 0))
		thumbnail.paste(image2, (426, 0))
		thumbnail.paste(image3, (852, 0))
		
		if os.path.isfile(f"./overlays/{subreddit}.png"):
			thumbnail.paste(overlay, (0, 0), overlay)
		
		thumbnail.save("./temp_files/final/thumbnail.png", "PNG")

		image1.close()
		image2.close()
		image3.close()
		if os.path.isfile(f"./overlays/{subreddit}.png"):
			overlay.close()
		thumbnail.close()

		print("Made thumbnail.")