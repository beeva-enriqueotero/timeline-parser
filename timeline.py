import re

import wikipedia
import datefinder

MIN_LENGTH = 100


class Timeline:
	def __init__(self, query=None, lang="en"):
		self.name = ""
		self.text = ""
		self.images = []
		self.hits = []

		if not query:
			return

		if lang in wikipedia.languages():
			wikipedia.set_lang(lang)

		results = wikipedia.search(query)
		if results:
			best_result = results[0]
			page = wikipedia.page(best_result)
			self.name = page.title
			self.text = page.content
			self.clean_text()
			self.generate()

			for img in page.images:
				if re.search(query, img, re.IGNORECASE):
					self.images.append(img)

	def clean_text(self, minlength=MIN_LENGTH):
		if not self.text:
			return False

		lines = []
		chars = 0
		for line in self.text.splitlines():
			if line.startswith("=") or not line:
				continue
			lines.append(line)
			chars += len(line)

		content = ""
		for line in lines:
			if len(line) > minlength:
				content += line

		self.text = content

	def generate(self):
		if not self.text:
			return False

		dates = list(datefinder.find_dates(self.text, index=True, source=True))
		limits = dates[0:2]

		results = []
		for d in dates:
			initial, final = d[2]
			while 1:
				initial -= 1
				char = self.text[initial]
				if char == ".":
					initial += 1
					break

			while 1:
				final += 1
				char = self.text[final]
				if char == ".":
					final += 1
					break

			date = d[0]
			if limits[0][0] <= date <= limits[1][0]:
				hit = self.text[initial:final]
				hits = map(lambda x: x["hit"], results)

				if hit not in hits:
					results.append({
						'date': date,
						'hit': hit
					})

		self.hits = sorted(results, key=lambda date: date["date"])
		delattr(self, "text")
