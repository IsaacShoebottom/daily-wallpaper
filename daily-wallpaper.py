import os
import sys
import tomllib
import requests
import importlib
import logging

def main():
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	session = requests.Session()
	session.headers.update({
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
	})

	# Load settings from settings.toml
	settings = tomllib.load(open("settings.toml", mode='b+r'))

	general_settings = settings.get("general")

	download_location = general_settings.get("location")
	logging.debug(f"Download location: {download_location}")

	provider_name = general_settings.get("provider")
	logging.debug(f"Provider: {provider_name}")

	provider_settings = settings.get(provider_name)

	# Load the provider module
	provider = importlib.import_module(f"providers.{provider_name}")
	logging.debug(f"Provider: {provider}")

	# Create an instance of the provider
	provider_obj = getattr(provider, provider_name)(provider_settings, session)

	# Get the image URL
	image_url = provider_obj.get_image_url()
	logging.debug(f"Image URL: {image_url}")

	# Download the image
	image = session.get(image_url).content

	# if its actually text, log it
	if image.startswith(b"<!DOCTYPE html>"):
		logging.error("Image is actually HTML")
		logging.error(image)
		sys.exit(1)

	if not os.path.exists(download_location):
		os.mkdir(download_location)
	with open(f"{download_location}/wallpaper.jpg", "wb") as file:
		file.write(image)

if __name__ == "__main__":
	main()