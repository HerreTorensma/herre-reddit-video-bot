import configparser

class ConfigManager:
	def __init__(self, path):
		self.path = path
		self.config = configparser.ConfigParser()

	def read_config(self):
		self.config.read(self.path)
		return self.config

	def write_config(self):
		with open(self.path, "w") as configfile:
			self.config.write(configfile)