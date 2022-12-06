import os
import moviepy.editor as mpy
import re
from PIL import Image

class VideoCompiler:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def get_video_files(self, directory):
		paths = os.listdir(directory)
		clips = []
		for path in paths:
			clips.append(mpy.VideoFileClip(f"{directory}/{path}"))

		return clips

	def resize_videos(self, clips):
		for i in range(len(clips)):
			resized = clips[i].resize((self.width, self.height))
			# Apparantly if you use clip.filename the video just corrupts?
			# Like what the fuck
			resized.write_videofile(f"./temp_files/resized_footage/{i}.mp4")
			resized.close()

	def compile_videos(self, clips):
		final = mpy.concatenate_videoclips(clips)
		final.write_videofile("./temp_files/final/final.mp4")
		final.close()

	def compile_reddit_video(self):
		audio_paths = os.listdir("./temp_files/audio_clips")
		
		# Ensures that the files are listed like
		# 1.mp3, 2.mp3 etc and not
		# 1.mp3, 10.mp3 etc
		audio_paths.sort(key=lambda f: int(re.sub('\D', '', f)))

		audio_clips = []
		title_audio = mpy.AudioFileClip("./temp_files/title_clips/title.mp3")
		for path in audio_paths:
			audio_clips.append(mpy.AudioFileClip(f"./temp_files/audio_clips/{path}"))

		image_paths = os.listdir("./temp_files/images")
		
		# Ensures that the files are listed like
		# 1.png, 2.png etc and not
		# 1.png, 10.png etc
		image_paths.sort(key=lambda f: int(re.sub('\D', '', f)))

		images = []
		title_image = mpy.ImageClip("./temp_files/title_clips/title.png", duration=title_audio.duration)
		for i in range(len(image_paths)):
			images.append(mpy.ImageClip(f"./temp_files/images/{i}.png", duration=audio_clips[i].duration))

		title_image = title_image.set_audio(title_audio)
		for i in range(len(images)):
			images[i] = images[i].set_audio(audio_clips[i])
		
		images.insert(0, title_image)

		final = mpy.concatenate_videoclips(images)
		final.write_videofile("./temp_files/final/final.mp4", fps=24)
		final.close()

		print("Rendered video.")

	def resize_images(self, input_directory, output_directory):
		image_paths = os.listdir(input_directory)
		for path in image_paths:
			image = Image.open(f"{input_directory}/{path}")
			x, y = image.size

			new_x = 0
			new_y = 0

			x_multiplier = self.width / x
			y_multiplier = self.height / y

			if y_multiplier < x_multiplier:
				new_x = int(x * y_multiplier)
				new_y = int(y * y_multiplier)
			else:
				new_x = int(x * x_multiplier)
				new_y = int(y * x_multiplier)

			resized = image.resize((new_x, new_y))

			image_with_edges = Image.new("RGB", (self.width, self.height), (0, 0, 0))

			x_position = int(self.width / 2 - new_x / 2)
			y_position = int(self.height / 2 - new_y / 2)

			image_with_edges.paste(resized, (x_position, y_position))
			image_with_edges.save(f"{output_directory}/{os.path.splitext(path)[0]}.png", "PNG")

	def compile_image_compilation(self, time_per_image, music_path):
		images = []
		
		image_paths = os.listdir("./temp_files/resized_footage")
		image_paths.sort(key=lambda f: int(re.sub('\D', '', f)))
		for i in range(len(image_paths)):
			images.append(mpy.ImageClip(f"./temp_files/resized_footage/{i}.png", duration=time_per_image))

		final = mpy.concatenate_videoclips(images)

		music_clip = mpy.AudioFileClip(music_path)
		music_clip = music_clip.set_duration(final.duration)

		final = final.set_audio(music_clip)
		
		final.write_videofile("./temp_files/final/final.mp4", fps=24)
		final.close()