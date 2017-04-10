# -*- coding: utf-8 -*-

import re
import wikipedia

from random import randint
from datetime import datetime
from datefinder import Datefinder

MIN_LENGTH = 100
MAX_LENGTH = 250


class Parser:
	def __init__(self, query=None, lang="en"):
		self.name 		= ""
		self.text		= ""
		self.dates 		= []
		self.images 	= []
		self.picture 	= ""
		self.hits 		= []

		if not query:
			return

		self.query = query

		if lang in wikipedia.languages():
			wikipedia.set_lang(lang)

	def suggestions(self):
		return list(wikipedia.search(self.query, results=10))

	def results(self, max_length=MAX_LENGTH):
		results = wikipedia.search(self.query)

		if results:
			best_result = results[0]
			page = wikipedia.page(best_result, preload=True)

			self.name = page.title
			self.text = page.content
			self.clean_text()
			self.generate()

			for img in page.images:
				if re.search(self.query, img, re.IGNORECASE):
					self.images.append(img)

			if len(self.images):
				picture = randint(0, len(self.images) - 1)
				self.picture = self.images[picture]

		result = self.__dict__.copy()
		result["hits"] = []
		for hit in self.hits:
			result["hits"].append(hit)

		return result

	def clean_text(self):
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
			content += line

		self.text = content

	def generate(self, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
		if not self.text:
			return False

		datefinder = Datefinder(self.text)

		dates 	= datefinder.results()
		limits 	= dates[0:2]
		self.dates = sorted(limits, key=lambda date: date["datetime"])

		hits =[]
		results = []
		for d in dates:
			initial, final = d["start"], d["end"]
			while 1:
				initial -= 1
				char = self.text[initial]
				if char == ".":
					initial += 1
					break

			while 1:
				final += 1
				if final < len(self.text):
					char = self.text[final]
					if char == ".":
						final += 1
						break
				else:
					break

			date 	= d["datetime"]
			format	= d["format"]
			if self.dates[0]["datetime"] <= date <= self.dates[1]["datetime"]:
				hit = self.text[initial:final]
				if max_length > len(hit) > min_length and hit not in hits:
					hits.append(hit)
					results.append({
						'datetime': date,
						'date': datetime.strftime(date, format),
						'content': hit
					})

		self.hits = sorted(results, key=lambda date: date["datetime"])
		delattr(self, "text")
