import tkinter as tk
from tkinter import ttk
import threading

class Post(ttk.Frame):
	def __init__(self, video_maker):
		super().__init__()

		self.program_state = tk.StringVar()
		self.program_state.set("Waiting for input...")

		self.video_maker = video_maker

		self.drive = tk.BooleanVar()
		self.drive.set(False)

		self.url = tk.StringVar()

		url_frame = tk.LabelFrame(self, text="Url", padx=10, pady=10)
		url_entry = tk.Entry(url_frame, font="TkFixedFont", textvariable=self.url)
		url_entry.pack(fill="x")
		url_frame.pack(fill="both")
		
		radiobutton_frame = tk.Frame(self)
		local_radiobutton = tk.Radiobutton(radiobutton_frame, text="Save locally", variable=self.drive, value=False)
		local_radiobutton.grid(row=0, column=0, padx=10, pady=10)
		drive_radiobutton = tk.Radiobutton(radiobutton_frame, text="Save on Google Drive", variable=self.drive, value=True)
		drive_radiobutton.grid(row=0, column=1, padx=10, pady=10)
		radiobutton_frame.pack()

		generate_button = tk.Button(self, text="Generate Post Video", command=self.start_thread)
		generate_button.pack()

		state_label = tk.Label(self, textvariable=self.program_state)
		state_label.pack()

	def start_thread(self):
		thread = threading.Thread(target=self.generate_video)
		thread.start()
		self.program_state.set("Generating...")

	def generate_video(self):
		try:
			self.video_maker.make_post_video(self.url.get(), self.drive.get())
			self.program_state.set("Done!")
		except:
			self.video_maker.delete_files()
			self.program_state.set("Error!")