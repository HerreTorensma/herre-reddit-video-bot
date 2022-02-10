import tkinter as tk
from tkinter import ttk
import threading

class AutomaticCompilation(ttk.Frame):
	def __init__(self, video_maker):
		super().__init__()

		self.program_state = tk.StringVar()
		self.program_state.set("Waiting for input...")
		
		self.video_maker = video_maker

		self.timeframe = tk.StringVar(self)
		self.timeframe.set("day")

		self.listing = tk.StringVar(self)
		self.listing.set("top")

		self.drive = tk.IntVar(self)
		self.drive.set(False)

		self.width = tk.IntVar(self)
		self.height = tk.IntVar(self)
		self.subreddit = tk.StringVar(self)
		self.limit = tk.StringVar(self)

		options_frame = tk.LabelFrame(self, text="Options")
		options_frame.columnconfigure(0, minsize=250)
		options_frame.columnconfigure(1, minsize=250)

		dimensions_label = tk.Label(options_frame, text="Dimensions")
		dimensions_label.grid(row=0, column=0)

		dimensions_frame = ttk.Frame(options_frame)

		self.width_entry = tk.Entry(dimensions_frame, width=9, textvariable=self.width)
		self.width_entry.grid(row=0, column=1)

		x_label = tk.Label(dimensions_frame, text="x")
		x_label.grid(row=0, column=2)

		self.height_entry = tk.Entry(dimensions_frame, width=9, textvariable=self.height)
		self.height_entry.grid(row=0, column=3)
		
		dimensions_frame.grid(row=0, column=1)

		subreddit_label = tk.Label(options_frame, text="Subreddit")
		subreddit_label.grid(row=1, column=0)
		subreddit_entry = tk.Entry(options_frame, width=20, textvariable=self.subreddit)
		subreddit_entry.grid(row=1, column=1)

		limit_label = tk.Label(options_frame, text="Amount of clips")
		limit_label.grid(row=2, column=0)
		limit_entry = tk.Entry(options_frame, textvariable=self.limit)
		limit_entry.grid(row=2, column=1)
		
		listing_label = tk.Label(options_frame, text="Listing")
		listing_label.grid(row=3, column=0)
		listing_dropdown = tk.OptionMenu(options_frame, self.listing, "hot", "new", "rising", "controversial", "top")
		listing_dropdown.config(width=14)
		listing_dropdown.grid(row=3, column=1)
		
		timeframe_label = tk.Label(options_frame, text="Timeframe")
		timeframe_label.grid(row=4, column=0)
		timeframe_dropdown = tk.OptionMenu(options_frame, self.timeframe, "hour", "day", "week", "month", "year", "all")
		timeframe_dropdown.config(width=14)
		timeframe_dropdown.grid(row=4, column=1)

		options_frame.pack(ipadx=10, ipady=10)

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
		try:
			self.video_maker.make_compilation(video_links=[], width=self.width.get(), height=self.height.get(), subreddit=self.subreddit.get(), listing=self.listing.get(), limit=self.limit.get(), timeframe=self.timeframe.get(), drive=self.drive.get())
			self.program_state.set("Done!")
		except:
			self.video_maker.delete_files()
			self.program_state.set("Error!")