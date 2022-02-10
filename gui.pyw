import tkinter as tk
from tkinter import ttk
import sys
import os

# Make the GUI look good on 4k
if sys.platform == "win32":
	from ctypes import windll
	windll.shcore.SetProcessDpiAwareness(1)

from frontend.settings import Settings
from frontend.manual_compilation import ManualCompilation
from frontend.automatic_compilation import AutomaticCompilation
from frontend.post import Post
from frontend.comments import Comments
from frontend.multiple_posts import MultiplePosts
from frontend.multiple_comments import MultipleComments

from frontend.text_redirector import TextRedirector

from backend.video_maker import VideoMaker

class GUI:
	def __init__(self, master):
		master.title("Herre's Reddit Video Bot")
		master.geometry("1024x768")

		self.output_box_frame = ttk.LabelFrame(text="Output", padding=[10, 10])
		self.output_box = tk.Text(self.output_box_frame, height=8)
		self.output_box.configure(state="disabled")
		self.output_box.pack(fill="x")

		sys.stdout = TextRedirector(self.output_box, "stdout")
		sys.stderr = TextRedirector(self.output_box, "stderr")

		self.notebook = ttk.Notebook(master, padding=[10, 10])

		video_maker = VideoMaker()

		manual_compilation_tab = ManualCompilation(video_maker)
		automatic_compilation_tab = AutomaticCompilation(video_maker)
		post_tab = Post(video_maker)
		comments_tab = Comments(video_maker)
		multiple_posts_tab = MultiplePosts(video_maker)
		multiple_comments_tab = MultipleComments(video_maker)
		settings_tab = Settings()

		self.notebook.add(manual_compilation_tab, text="Manual Compilation")
		self.notebook.add(automatic_compilation_tab, text="Automatic Compilation")
		self.notebook.add(post_tab, text="Post")
		self.notebook.add(comments_tab, text="Comments")
		self.notebook.add(multiple_posts_tab, text="Automatic Posts")
		self.notebook.add(multiple_comments_tab, text="Automatic Comments")
		self.notebook.add(settings_tab, text="Settings")

		self.notebook.pack(expand=1, fill="both")

		self.output_box_frame.pack(fill="both")

if __name__ == "__main__":
	root = tk.Tk()
	gui = GUI(root)
	root.mainloop()