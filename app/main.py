import datetime
import os
import requests
import importlib
import logging
import slugify
import time
import croniter
from settings import settings

def main():
	config = settings.load_settings()
	logging.basicConfig(level=config['general']['log_level'], format="%(asctime)s [%(levelname)s] %(message)s", force=True)
	logging.debug(f"Config: {config}")

	chosen_providers = config['general']['provider']

	# Daemon mode
	if config['daemon']['daemon']:
		while True:
			for provider in chosen_providers:
				download_with_provider(provider, config)
			if config['daemon']['cron'] != "":
				now = datetime.datetime.now()
				cron = croniter.croniter(config['daemon']['cron'], now)
				next_run = cron.get_next(datetime.datetime)
				logging.info(f"Next run: {next_run}")
				time.sleep((next_run - now).total_seconds())
			else:
				time.sleep(config['daemon']['interval'])
	# Download once
	else:
		for provider in chosen_providers:
			download_with_provider(provider, config)

def download_with_provider(provider_name, config):
	session = requests.Session()
	session.headers.update({
		"User-Agent": config['general']['user_agent']
	})

	# Convenience variables, could be inlined
	provider_settings = config[provider_name] if provider_name in config else None
	download_location = os.path.abspath(os.path.expanduser(config['general']['location']))

	# Load the provider module
	provider = importlib.import_module(f"providers.{provider_name}")

	# Create an instance of the provider
	provider_obj = getattr(provider, provider_name.title())(provider_settings, session)
	# Get the image URL and title
	image_url, image_title = provider_obj.get_image_info()
	logging.debug(f"Image URL: {image_url}")

	# Variables for the file path
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	image_title = slugify.slugify(image_title)
	file_path = f"{download_location}/{provider_name.title()}/{date} [{image_title}].jpg"
	# Check if we should include the title in the filename
	if not config['general']['include_title']:
		file_path = f"{download_location}/{provider_name.title()}/{date}.jpg"
	# Create the download location if it doesn't exist
	if not os.path.exists(download_location):
		os.mkdir(download_location)
	if not os.path.exists(f"{download_location}/{provider_name.title()}"):
		os.mkdir(f"{download_location}/{provider_name.title()}")
	# Check if the file exists and if we should overwrite it
	if os.path.exists(file_path) and not config['general']['overwrite']:
		return

	# Download the image
	image = session.get(image_url).content
	with open(file_path, "wb") as file:
		file.write(image)

if __name__ == "__main__":
	main()