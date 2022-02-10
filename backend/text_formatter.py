import textwrap
import re
import string
import html

class TextFormatter:
	def __init__(self):
		pass

	def convert_html_to_unicode(self, text):
		return html.unescape(text)

	def split_into_paragraphs(self, text, width):
		paragraphs = text.split("\n")
		lines = []
		paragraph_lines = []
		for paragraph in paragraphs:
			paragraph_lines.append(textwrap.wrap(paragraph, width))

		for paragraph in paragraph_lines:
			for line in paragraph:
				line = line.strip()
				lines.append(line)
			lines.append("\n")

		print("Split text into paragraphs.")

		return lines

	def format_text(self, text, width, height):
		lines = self.split_into_paragraphs(text, width)

		screen_lines = []
		for i in range(0, len(lines), height):
			screen_lines.append(lines[i:i+height])

		screens = []
		for screen in screen_lines:
			screen_string = ""
			for line in screen:
				screen_string += " " + line
			screens.append(screen_string)

		print("Formatted plain text.")
		
		return screen_lines, screens

	def split_into_sentences(self, text):
		sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

		print("Split into sentences.")

		return sentences

	def format_content(self, contents, width, height):
		content_lines = []
		formatted_content = []
		for i in range(len(contents)):
			lines, text = self.format_text(contents[i]["body"], width, height)
			for j in range(len(text)):
				content_lines.append(lines[j])
				comment = {
					"author": "",
					"body": "",
					"ups": ""
				}
				comment["author"] = contents[i]["author"]
				comment["ups"] = contents[i]["ups"]
				comment["body"] = text[j]
				formatted_content.append(comment)

		print("Formatted content.")

		return content_lines, formatted_content

	def filter_sentences(self, sentences):
		for i in range(len(sentences)):
			sentences[i] = list(filter(("\n").__ne__, sentences[i]))
			sentences[i] = list(filter(("\n \n").__ne__, sentences[i]))
			sentences[i] = list(filter((" \n").__ne__, sentences[i]))

		print("Filtered sentences.")

		return sentences