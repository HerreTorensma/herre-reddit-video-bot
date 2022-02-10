import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from backend.config_manager import ConfigManager

class Settings(ttk.Frame):
	def __init__(self):
		super().__init__()

		self.video_location = ""
		self.thumbnail_location = ""

		video_frame = tk.LabelFrame(self, text="Video save location")

		self.video_entry = tk.Entry(video_frame)
		self.video_entry.pack(expand=1, fill="x", side="left", padx=10, pady=10)

		video_button = tk.Button(video_frame, text="Browse...", command=self.select_video_folder)
		video_button.pack(side="right", padx=10, pady=10)
		video_frame.pack(fill="x")

		thumbnail_frame = tk.LabelFrame(self, text="Thumbnail save location")
		
		self.thumbnail_entry = tk.Entry(thumbnail_frame)
		self.thumbnail_entry.pack(expand=1, fill="x", side="left", padx=10, pady=10)
		
		thumbnail_button = tk.Button(thumbnail_frame, text="Browse...", command=self.select_thumbnail_folder)
		thumbnail_button.pack(side="right", padx=10, pady=10)
		thumbnail_frame.pack(fill="x")

		drive_video_frame = tk.LabelFrame(self, text="Google Drive Video Folder ID")
		self.drive_video_entry = tk.Entry(drive_video_frame)
		self.drive_video_entry.pack(fill="x", padx=10, pady=10)
		drive_video_frame.pack(fill="x")
		
		drive_thumbnail_frame = tk.LabelFrame(self, text="Google Drive Thumbnail Folder ID")
		self.drive_thumbnail_entry = tk.Entry(drive_thumbnail_frame)
		self.drive_thumbnail_entry.pack(fill="x", padx=10, pady=10)
		drive_thumbnail_frame.pack(fill="x")

		save_button = tk.Button(self, text="Save Settings", command=self.save_settings)
		save_button.pack(padx=10, pady=10)

		self.config_manager = ConfigManager("./config.ini")
		self.config_manager.read_config()
		self.load_config()

	def load_config(self):
		self.video_location = self.config_manager.config["general"]["video_save_location"]
		self.video_entry.delete(0, "end")
		self.video_entry.insert(0, self.video_location)

		self.thumbnail_location = self.config_manager.config["general"]["thumbnail_save_location"]
		self.thumbnail_entry.delete(0, "end")
		self.thumbnail_entry.insert(0, self.thumbnail_location)

		self.drive_video_entry.insert(0, self.config_manager.config["google_drive"]["video_folder_id"])
		self.drive_thumbnail_entry.insert(0, self.config_manager.config["google_drive"]["thumbnail_folder_id"])

	def save_settings(self):
		self.video_location = self.video_entry.get()
		self.thumbnail_location = self.thumbnail_entry.get()

		self.config_manager.config["general"]["video_save_location"] = self.video_location
		self.config_manager.config["general"]["thumbnail_save_location"] = self.thumbnail_location

		self.config_manager.config["google_drive"]["video_folder_id"] = self.drive_video_entry.get()
		self.config_manager.config["google_drive"]["thumbnail_folder_id"] = self.drive_thumbnail_entry.get()

		self.config_manager.write_config()
	
	def select_video_folder(self):
		self.video_location = filedialog.askdirectory()
		self.video_entry.delete(0, "end")
		self.video_entry.insert(0, self.video_location)

	def select_thumbnail_folder(self):
		self.thumbnail_location = filedialog.askdirectory()
		self.thumbnail_entry.delete(0, "end")
		self.thumbnail_entry.insert(0, self.thumbnail_location)