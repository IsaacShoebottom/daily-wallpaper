import datetime
import os
import sys
import requests
import importlib
import logging
import slugify
import settings


def main():
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	config = settings.load_settings()
	logging.debug(f"Config: {config}")

	session = requests.Session()
	session.headers.update({
		"User-Agent": config['general']['user_agent']
	})

	# Convenience variables, could be inlined
	provider_name = config['general']['provider']
	provider_settings = config[config['general']['provider']]
	download_location = os.path.abspath(os.path.expanduser(config['general']['location']))

	# Load the provider module
	provider = importlib.import_module(f"providers.{config['general']['provider']}")

	# Create an instance of the provider
	provider_obj = getattr(provider, provider_name.title())(provider_settings, session)
	# Get the image URL and title
	image_url, image_title = provider_obj.get_image_info()
	logging.debug(f"Image URL: {image_url}")

	# Download the image
	image = session.get(image_url).content

	if not os.path.exists(download_location):
		os.mkdir(download_location)
	if not os.path.exists(f"{download_location}/{provider_name.title()}"):
		os.mkdir(f"{download_location}/{provider_name.title()}")

	date = datetime.datetime.now().strftime("%Y-%m-%d")
	image_title = slugify.slugify(image_title)
	with open(f"{download_location}/{provider_name.title()}/{date} [{image_title}].jpg", "wb") as file:
		file.write(image)

if __name__ == "__main__":
	main()