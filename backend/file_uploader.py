import shutil
from pathlib import Path
from datetime import datetime
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class FileUploader:
	def __init__(self):
		pass

	def copy_to_folder(self, file, new_folder, new_name, extension):
		if new_name == "":
			new_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + extension

		Path(new_folder).mkdir(parents=True, exist_ok=True)
		
		shutil.copy(file, new_folder + "/" + new_name)

		print("Copied to folder.")

	def upload_to_google_drive(self, file_path, title, id):
		gauth = GoogleAuth()
		drive = GoogleDrive(gauth)

		gfile = drive.CreateFile({"title": title, "parents": [{"id": id}]})
		gfile.SetContentFile(file_path)
		gfile.Upload()

		print("Uploaded to Google Drive.")