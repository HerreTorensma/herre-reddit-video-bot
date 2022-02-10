import pyttsx3

class TextToSpeech:
	def __init__(self):
		self.engine = pyttsx3.init()
		self.voices = self.engine.getProperty("voices")
		self.engine.setProperty("voice", self.voices[1].id)

	def save_audio(self, text, filename):
		self.engine.save_to_file(text, filename)
		self.engine.runAndWait()
		print("Saved audio clip.")

	def stop_engine(self):
		self.engine.stop()