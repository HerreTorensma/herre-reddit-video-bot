class TextRedirector:
	def __init__(self, widget, tag="stdout"):
		self.widget = widget
		self.tag = tag

	def write(self, input):
		self.widget.configure(state="normal")
		self.widget.insert("end", input, (self.tag,))
		self.widget.configure(state="disabled")

	def flush(self):
		pass