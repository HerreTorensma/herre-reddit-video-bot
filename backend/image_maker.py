from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageMaker:
	def __init__(self):
		self.background_color = (26, 26, 27)
		self.author_color = (79, 188, 255)
		self.meta_color = (129, 131, 132)

	def make_title_image(self, post, filename):
		titlefont = ImageFont.truetype("./fonts/IBMPlexSans-Bold.ttf", 60)
		ibmplex = ImageFont.truetype("./fonts/IBMPlexSans-Regular.ttf", 40)
		ibmplexbold = ImageFont.truetype("./fonts/IBMPlexSans-Bold.ttf", 40)

		image = Image.open("./templates/title_template.png")
		draw = ImageDraw.Draw(image)

		draw.text((208, 80), "r/" + post["subreddit"], font=ibmplex)
		draw.text((208, 144), post["author"], font=ibmplex, fill=self.author_color)
		
		ups_width, ups_height = ibmplexbold.getsize(str(post["ups"]))
		draw.text((83 - ups_width/2, 112), str(post["ups"]), font=ibmplexbold)

		lines = textwrap.wrap(post["title"], 30)
		
		# Tallest a line of text with the ibmplexbold font gets
		height = 75
		y = 0
		for line in lines:
			draw.text((32, 256 + y), line, font=titlefont)
			y += height

		image.save(filename, "PNG")
		image.close()

		print("Title image made.")

	def make_vertical_content_image(self, content, lines, filename):
		image = Image.open("./templates/comment_template.png")

		draw = ImageDraw.Draw(image)
		notosans = ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 40)
		ibmplex = ImageFont.truetype("./fonts/IBMPlexSans-Regular.ttf", 40)

		draw.text((208, 48), content["author"], font=ibmplex, fill=self.author_color)

		author_width, author_height = ibmplex.getsize(content["author"])
		draw.text((208 + author_width + 32, 48), str(content["ups"]) + " points", font=ibmplex, fill=self.meta_color)

		# Tallest a line of text with the notosans font gets
		height = 53
		y = 0
		for line in lines:
			draw.text((32, 128 + y), line, font=notosans)
			y += height

		image.save(filename, "PNG")
		image.close()

		print("Content image made.")

	def make_transparant_content_image(self, content, lines, filename):
		image = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))

		draw = ImageDraw.Draw(image)
		notosans = ImageFont.truetype("./fonts/NotoSans-Regular.ttf", 40)

		height = 53
		y = 0
		for line in lines:
			draw.text((32, 128 + y), line, font=notosans)
			y += height

		image.save(filename, "PNG")
		image.close()