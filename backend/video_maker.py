from backend.scraper import Scraper
from backend.content_downloader import ContentDownloader
from backend.video_compiler import VideoCompiler
from backend.thumbnail_maker import ThumbnailMaker
from backend.text_to_speech import TextToSpeech
from backend.image_maker import ImageMaker
from backend.text_formatter import TextFormatter
from backend.file_uploader import FileUploader
from backend.config_manager import ConfigManager

import os
import re

class VideoMaker:
	def __init__(self):
		pass

	def delete_files(self):
		footage = os.listdir("./temp_files/footage")
		resized_footage = os.listdir("./temp_files/resized_footage")
		images = os.listdir("./temp_files/images")
		audio_clips = os.listdir("./temp_files/audio_clips")
		final = os.listdir("./temp_files/final")

		for clip in footage:
			os.remove(f"./temp_files/footage/{clip}")
		
		for clip in resized_footage:
			os.remove(f"./temp_files/resized_footage/{clip}")

		for image in images:
			os.remove(f"./temp_files/images/{image}")
		
		for clip in audio_clips:
			os.remove(f"./temp_files/audio_clips/{clip}")

		if os.path.isfile("./temp_files/title_clips/title.mp3"):
			os.remove("./temp_files/title_clips/title.mp3")
		
		if os.path.isfile("./temp_files/title_clips/title.png"):
			os.remove("./temp_files/title_clips/title.png")
		
		for file in final:
			os.remove(f"./temp_files/final/{file}")

		print("Files tidied up.")

	def make_compilation(self, video_links, width, height, subreddit, listing, limit, timeframe, drive):
		scraper = Scraper()
		if video_links == []:
			page = scraper.get_subreddit_json(subreddit, listing, limit, timeframe)
			urls = scraper.get_video_urls_from_subreddit(page)
		else:
			urls = []
			for link in video_links:
				page = scraper.get_post_json(link + ".json")
				urls.append(scraper.get_video_url_from_post(page))

		video_downloader = ContentDownloader("./temp_files/footage", urls)
		video_downloader.download_videos()

		video_compiler = VideoCompiler(width, height)
		raw_clips = video_compiler.get_video_files("./temp_files/footage")
		video_compiler.resize_videos(raw_clips)

		clips = video_compiler.get_video_files("./temp_files/resized_footage")
		video_compiler.compile_videos(clips)

		if subreddit != "" and len(clips) >= 3:
			thumbnail_maker = ThumbnailMaker(clips, "./temp_files/images")
			images = thumbnail_maker.get_vertical_images()
			thumbnail_maker.make_vertical_thumbnail(subreddit)

		for clip in raw_clips:
			clip.close()

		for clip in clips:
			clip.close()

		config_manager = ConfigManager("./config.ini")
		config = config_manager.read_config()

		file_uploader = FileUploader()
		if drive == True:
			file_uploader.upload_to_google_drive("./temp_files/final/final.mp4", "compilation", config["google_drive"]["video_folder_id"])
			if os.path.isfile("./temp_files/final/thumbnail.png"):
				file_uploader.upload_to_google_drive("./temp_files/final/thumbnail.png", "compilation", config["google_drive"]["thumbnail_folder_id"])
		else:
			video_folder = config["general"]["video_save_location"]
			if video_folder == "default":
				video_folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/videos")
			
			thumbnail_folder = config["general"]["thumbnail_save_location"]
			if thumbnail_folder == "default":
				thumbnail_folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/thumbnails")
			
			file_uploader.copy_to_folder("./temp_files/final/final.mp4", video_folder, "", ".mp4")
			if os.path.isfile("./temp_files/final/thumbnail.png"):
				file_uploader.copy_to_folder("./temp_files/final/thumbnail.png", thumbnail_folder, "", ".png")

		self.delete_files()

	def make_comment_video(self, url, amount, drive):
		url = url + ".json"

		scraper = Scraper()
		page = scraper.get_post_json(url)
		post_data = scraper.get_post_data(page)
		comments = scraper.get_comments_from_post(page, amount)

		text_formatter = TextFormatter()
		comment_lines, formatted_comments = text_formatter.format_content(comments, 50, 32)

		for i in range(len(formatted_comments)):
			formatted_comments[i]["body"] = text_formatter.convert_html_to_unicode(formatted_comments[i]["body"])

		sentences = []
		for content in formatted_comments:
			sentences.append(text_formatter.split_into_sentences(content["body"]))

		sentences = text_formatter.filter_sentences(sentences)

		text_to_speech = TextToSpeech()
		text_to_speech.save_audio(post_data["title"], "./temp_files/title_clips/title.mp3")
		
		audio_counter = 0
		for i in range(len(sentences)):
			for j in range(len(sentences[i])):
				text_to_speech.save_audio(sentences[i][j], f"./temp_files/audio_clips/{audio_counter}.mp3")
				audio_counter += 1
		
		text_to_speech.stop_engine()

		image_maker = ImageMaker()
		image_maker.make_title_image(post_data, "./temp_files/title_clips/title.png")

		image_counter = 0
		for i in range(len(sentences)):
			frame_text = ""
			for j in range(len(sentences[i])):
				frame_text += sentences[i][j] + " "
				lines = text_formatter.split_into_paragraphs(frame_text, 50)
				
				while lines[0] == "\n":
					lines.remove("\n")

				image_maker.make_vertical_content_image(formatted_comments[i], lines, f"./temp_files/images/{image_counter}.png")
				image_counter += 1

		video_compiler = VideoCompiler(1080, 1920)
		video_compiler.compile_reddit_video()

		config_manager = ConfigManager("./config.ini")
		config = config_manager.read_config()
		
		file_uploader = FileUploader()
		if drive == True:
			file_uploader.upload_to_google_drive("./temp_files/final/final.mp4", post_data["title"], config["google_drive"]["video_folder_id"])
		else:
			folder = config["general"]["video_save_location"]
			if folder == "default":
				folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/videos")
			file_uploader.copy_to_folder("./temp_files/final/final.mp4", folder, re.sub(r'[\\/*?:"<>|]', "", post_data["title"] + ".mp4"), None)
		
		self.delete_files()

	def make_post_video(self, url, drive):
		url = url + ".json"

		scraper = Scraper()
		page = scraper.get_post_json(url)
		post_data = scraper.get_post_data(page)
		
		text_formatter = TextFormatter()
		content_lines, formatted_content = text_formatter.format_content([post_data], 50, 32)

		for i in range(len(formatted_content)):
			formatted_content[i]["body"] = text_formatter.convert_html_to_unicode(formatted_content[i]["body"])

		sentences = []
		for content in formatted_content:
			sentences.append(text_formatter.split_into_sentences(content["body"]))

		sentences = text_formatter.filter_sentences(sentences)

		text_to_speech = TextToSpeech()
		text_to_speech.save_audio(post_data["title"], "./temp_files/title_clips/title.mp3")
		
		audio_counter = 0
		for i in range(len(sentences)):
			for j in range(len(sentences[i])):
				text_to_speech.save_audio(sentences[i][j], f"./temp_files/audio_clips/{audio_counter}.mp3")

				audio_counter += 1
		
		text_to_speech.stop_engine()
		
		image_maker = ImageMaker()
		image_maker.make_title_image(post_data, "./temp_files/title_clips/title.png")

		image_counter = 0
		for i in range(len(sentences)):
			frame_text = ""
			for j in range(len(sentences[i])):
				frame_text += sentences[i][j] + " "
				lines = text_formatter.split_into_paragraphs(frame_text, 50)

				while lines[0] == "\n":
					lines.remove("\n")

				image_maker.make_vertical_content_image(formatted_content[i], lines, f"./temp_files/images/{image_counter}.png")
				image_counter += 1

		video_compiler = VideoCompiler(1080, 1920)
		video_compiler.compile_reddit_video()

		config_manager = ConfigManager("./config.ini")
		config = config_manager.read_config()

		file_uploader = FileUploader()
		if drive == True:
			file_uploader.upload_to_google_drive("./temp_files/final/final.mp4", post_data["title"], config["google_drive"]["video_folder_id"])
		else:
			folder = config["general"]["video_save_location"]
			if folder == "default":
				folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/videos")
			file_uploader.copy_to_folder("./temp_files/final/final.mp4", folder, re.sub(r'[\\/*?:"<>|]', "", post_data["title"] + ".mp4"), None)
		
		self.delete_files()

	def make_multiple_comments_videos(self, subreddit, listing, amount_of_posts, timeframe, amount_of_comments, drive):
		scraper = Scraper()
		page = scraper.get_subreddit_json(subreddit, listing, amount_of_posts, timeframe)
		urls = scraper.get_post_urls_from_subreddit(page)
		for url in urls:
			self.make_comment_video(url + ".json", amount_of_comments, drive)

	def make_multiple_post_videos(self, subreddit, listing, amount, timeframe, drive):
		scraper = Scraper()
		page = scraper.get_subreddit_json(subreddit, listing, amount, timeframe)
		urls = scraper.get_post_urls_from_subreddit(page)
		for url in urls:
			self.make_post_video(url + ".json", drive)

	def make_image_compilation(self, width, height, subreddit, listing, amount, timeframe, drive, music_path, time_per_image):
		scraper = Scraper()
		page = scraper.get_subreddit_json(subreddit, listing, amount, timeframe)
		urls = scraper.get_images_urls_from_subreddit(page)
		
		content_downloader = ContentDownloader("./temp_files/images", urls)
		content_downloader.download_images()

		video_compiler = VideoCompiler(width, height)
		video_compiler.resize_images("./temp_files/images", "./temp_files/resized_footage")
		
		video_compiler.compile_image_compilation(time_per_image, music_path)

		config_manager = ConfigManager("./config.ini")
		config = config_manager.read_config()

		file_uploader = FileUploader()
		if drive == True:
			file_uploader.upload_to_google_drive("./temp_files/final/final.mp4", "compilation", config["google_drive"]["video_folder_id"])
			if os.path.isfile("./temp_files/final/thumbnail.png"):
				file_uploader.upload_to_google_drive("./temp_files/final/thumbnail.png", "compilation", config["google_drive"]["thumbnail_folder_id"])
		else:
			video_folder = config["general"]["video_save_location"]
			if video_folder == "default":
				video_folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/videos")
			
			thumbnail_folder = config["general"]["thumbnail_save_location"]
			if thumbnail_folder == "default":
				thumbnail_folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/thumbnails")
			
			file_uploader.copy_to_folder("./temp_files/final/final.mp4", video_folder, "", ".mp4")
			if os.path.isfile("./temp_files/final/thumbnail.png"):
				file_uploader.copy_to_folder("./temp_files/final/thumbnail.png", thumbnail_folder, "", ".png")

		self.delete_files()

	def make_transparant_post_video(self, url, drive):
		url = url + ".json"

		scraper = Scraper()
		page = scraper.get_post_json(url)
		post_data = scraper.get_post_data(page)
		
		text_formatter = TextFormatter()
		content_lines, formatted_content = text_formatter.format_content([post_data], 50, 32)

		for i in range(len(formatted_content)):
			formatted_content[i]["body"] = text_formatter.convert_html_to_unicode(formatted_content[i]["body"])

		sentences = []
		for content in formatted_content:
			sentences.append(text_formatter.split_into_sentences(content["body"]))

		sentences = text_formatter.filter_sentences(sentences)

		text_to_speech = TextToSpeech()
		text_to_speech.save_audio(post_data["title"], "./temp_files/title_clips/title.mp3")
		
		audio_counter = 0
		for i in range(len(sentences)):
			for j in range(len(sentences[i])):
				text_to_speech.save_audio(sentences[i][j], f"./temp_files/audio_clips/{audio_counter}.mp3")

				audio_counter += 1
		
		text_to_speech.stop_engine()
		
		image_maker = ImageMaker()
		image_maker.make_title_image(post_data, "./temp_files/title_clips/title.png")

		image_counter = 0
		for i in range(len(sentences)):
			frame_text = ""
			for j in range(len(sentences[i])):
				frame_text += sentences[i][j] + " "
				lines = text_formatter.split_into_paragraphs(frame_text, 50)

				while lines[0] == "\n":
					lines.remove("\n")

				image_maker.make_transparant_content_image(formatted_content[i], lines, f"./temp_files/images/{image_counter}.png")
				image_counter += 1

		video_compiler = VideoCompiler(1080, 1920)
		video_compiler.compile_reddit_video()

		config_manager = ConfigManager("./config.ini")
		config = config_manager.read_config()

		file_uploader = FileUploader()
		if drive == True:
			file_uploader.upload_to_google_drive("./temp_files/final/final.mp4", post_data["title"], config["google_drive"]["video_folder_id"])
		else:
			folder = config["general"]["video_save_location"]
			if folder == "default":
				folder = os.path.expanduser("~/Videos/Herre's Reddit Video Bot/videos")
			file_uploader.copy_to_folder("./temp_files/final/final.mp4", folder, re.sub(r'[\\/*?:"<>|]', "", post_data["title"] + ".mp4"), None)
		
		self.delete_files()
