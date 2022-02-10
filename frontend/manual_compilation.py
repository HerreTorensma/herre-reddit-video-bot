import tkinter as tk
from tkinter import ttk
import threading

class ManualCompilation(ttk.Frame):
	def __init__(self, video_maker):
		super().__init__()

		self.program_state = tk.StringVar()
		self.program_state.set("Waiting for input...")

		self.video_maker = video_maker

		self.drive = tk.BooleanVar()
		self.drive.set(False)

		self.width = tk.IntVar()
		self.height = tk.IntVar()

		self.subreddit = tk.StringVar()
		self.subreddit.set("")

		dimensions_frame = ttk.LabelFrame(self, text="Dimensions")

		width_entry = tk.Entry(dimensions_frame, width=8, textvariable=self.width)
		width_entry.delete(0, "end")
		width_entry.insert(0, 1280)
		width_entry.grid(row=0, column=1)

		x_label = tk.Label(dimensions_frame, text="x")
		x_label.grid(row=0, column=2)

		height_entry = tk.Entry(dimensions_frame, width=8, textvariable=self.height)
		height_entry.delete(0, "end")
		height_entry.insert(0, 720)
		height_entry.grid(row=0, column=3)
		
		dimensions_frame.pack(padx=10, pady=10)

		subreddit_frame = ttk.LabelFrame(self, text="Subreddit")
		subreddit_entry = ttk.Entry(subreddit_frame, textvariable=self.subreddit)
		subreddit_entry.pack()
		subreddit_frame.pack(padx=10, pady=10)

		urls_frame = tk.LabelFrame(self, text="Urls", padx=10, pady=10)
		self.urls_box = tk.Text(urls_frame, width=75, height=10)
		self.urls_box.pack(fill="x", expand=1)
		urls_frame.pack(fill="both")

		radiobutton_frame = tk.Frame(self)
		local_radiobutton = tk.Radiobutton(radiobutton_frame, text="Save locally", variable=self.drive, value=False)
		local_radiobutton.grid(row=0, column=0, padx=10, pady=10)
		drive_radiobutton = tk.Radiobutton(radiobutton_frame, text="Save on Google Drive", variable=self.drive, value=True)
		drive_radiobutton.grid(row=0, column=1, padx=10, pady=10)
		radiobutton_frame.pack()
		
		generate_button = tk.Button(self, text="Generate Compilation", command=self.start_thread)
		generate_button.pack()

		state_label = tk.Label(self, textvariable=self.program_state)
		state_label.pack()

	def start_thread(self):
		thread = threading.Thread(target=self.generate_video)
		thread.start()
		self.program_state.set("Generating...")

	def generate_video(self):
		urls_string = self.urls_box.get("1.0", "end")
		urls = urls_string.split("\n")
		urls = list(filter(None, urls))

		try:
			self.video_maker.make_compilation(video_links=urls, width=self.width.get(), height=self.height.get(), subreddit=self.subreddit.get(), listing="", limit="", timeframe="", drive=self.drive.get())
			self.program_state.set("Done!")
		except:
			self.video_maker.delete_files()
			self.program_state.set("Error!")