# Using official Unsplash API to get images
# curl https://api.unsplash.com/collections/1459961/photos
# But we will scrape >:)
import logging
import re
from providers._provider import Provider

class Unsplash(Provider):
	name = "Unsplash"
	url = "https://unsplash.com/collections/1459961/photo-of-the-day-(archive)"

	def __init__(self, settings, session):
		super().__init__(settings, session)

	def get_image_info(self):
		query = f"https://unsplash.com/collections/{self.settings['collection']}"
		logging.debug(f"Query: {query}")

		response = self.session.get(query).text
		# logging.debug(f"Response: {response}")

		regex = r"href=\"\/photos\/(.*?)\""
		matches = re.search(regex, response)
		logging.debug(f"Matches: {matches}")
		image_slug = matches.group(1)
		logging.debug(f"Image slug: {image_slug}")

		image_id = image_slug.split("-")[-1]
		logging.debug(f"Image ID: {image_id}")

		title = image_slug.replace("-", " ").replace(image_id, "").strip().title()

		image_url = f"https://unsplash.com/photos/{image_id}/download"
		logging.debug(f"Image URL: {image_url}")
		return image_url, title
