import datetime
import logging
import time

from providers._provider import Provider

# https://api.wikimedia.org/wiki/Feed_API/Reference/Featured_content

class Wikimedia(Provider):
	name = "Wikimedia"
	url = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/"

	def __init__(self, settings, session):
		super().__init__(settings, session)

	def get_image_info(self):
		# Since wikipedia API seems to fail to provide image url, we will retry on key error until we get the image url
		try:
			today = datetime.datetime.now()
			date = today.strftime('%Y/%m/%d')
			logging.debug(f"Date: {date}")
			url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/' + date
			logging.debug(f"URL: {url}")

			response = self.session.get(url).json()
			# logging.debug(f"Response: {response}")

			image = response['image']['image']['source']
			logging.debug(f"Image: {image}")
			image_url = image

			title = response['image']['description']['text']
			return image_url, title
		except KeyError:
			logging.error("KeyError, retrying...")
			time.sleep(10) # Wait 10 seconds
			return self.get_image_info()
