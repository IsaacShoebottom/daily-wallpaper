import datetime
import logging
import requests
import re
from providers.provider import Provider

# https://api.wikimedia.org/wiki/Feed_API/Reference/Featured_content

class wikimedia(Provider):
	name = "Wikimedia"
	url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/"


	def __init__(self, settings, session):
		super().__init__(settings, session)

	def get_image_url(self):
		today = datetime.datetime.now()
		date = today.strftime('%Y/%m/%d')
		logging.debug(f"Date: {date}")
		url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/' + date
		logging.debug(f"URL: {url}")

		response = self.session.get(url).json()
		logging.debug(f"Response: {response}")

		image = response['image']['image']['source']
		logging.debug(f"Image: {image}")
		image_url = image

		return image_url

