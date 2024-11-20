import logging
import requests
from requests import session

from providers.provider import Provider

class bing(Provider):
	name = "Bing"
	url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
	idx = 0
	number = 2**31-1

	def __init__(self, settings, session):
		super().__init__(settings, session)
		self.size = settings.get("size")
		self.country = settings.get("country")
		self.market = settings.get("market")

	def get_image_url(self):
		query = f"https://www.bing.com/HPImageArchive.aspx?format=js&idx={self.idx}&n={self.number}&mkt={self.market}"
		logging.debug(f"Query: {query}")

		response = self.session.get(query).json()
		logging.debug(f"Response: {response}")

		image_url = response["images"][0]["urlbase"]
		logging.debug(f"Image URL: {image_url}")

		image_url = f"https://www.bing.com{image_url}_{self.size}.jpg"
		return image_url

