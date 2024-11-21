import os.path
import tomlkit

local_path = os.path.abspath("config.toml")
user_path = os.path.expanduser("~/.config/daily-wallpaper/config.toml")

def default_settings():
	general = tomlkit.table()
	general.add("location", "~/Pictures/Wallpapers")
	general["location"].comment("Download location")
	general.add("provider", ["bing", "unsplash", "wikimedia"])
	general["provider"].comment("Which wallpaper provider to use, in order of preference (do no include if you don't want to download the file)")
	general.add("include_title", True)
	general.value.item("include_title").comment("Include image title in filename")
	general.add("set_wallpaper", False)
	general.value.item("set_wallpaper").comment("Set wallpaper after download")
	general.add("log", False)
	general.value.item("log").comment("Log to file, located in the download location")
	general.add("log_level", "INFO")
	general["log_level"].comment("Log level, possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL")
	general.add("overwrite", False)
	general.value.item("overwrite").comment("Overwrite existing files")
	general.add("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0")
	general["user_agent"].comment("User-Agent to use for requests, change to avoid being blocked or to comply with ToS")
	general.add(tomlkit.nl())

	daemon = tomlkit.table()
	daemon.add("daemon", False)
	daemon.value.item("daemon").comment("Run as daemon (continuously in the background)")
	daemon.add("interval", 86400)
	daemon["interval"].comment("Interval in seconds (24 hours)")
	daemon.add("cron", "0 0 * * *")
	daemon["cron"].comment("Cron expression, overrides interval")
	daemon.add(tomlkit.nl())

	bing = tomlkit.table()
	bing.add("size", "UHD")
	bing["size"].comment('Image size, possible values: "UHD", "1920x1080"')
	bing.add("country", "us")
	bing["country"].comment("Country, currently unused")
	bing.add("market", "en-US")
	bing["market"].comment("Market, overrides country")
	bing.add(tomlkit.nl())

	unsplash = tomlkit.table()
	unsplash.add("collection", 1459961)
	unsplash["collection"].comment("Collection ID, which gallery to use")
	unsplash.add("application_id", "")
	unsplash["application_id"].comment("Unset, currently not used, as we scrape")
	unsplash.add("access_key", "")
	unsplash["access_key"].comment("Unset, currently not used, as we scrape")
	unsplash.add("secret_key", "")
	unsplash["secret_key"].comment("Unset, currently not used, as we scrape")
	unsplash.add(tomlkit.nl())

	wikimedia = tomlkit.table()
	wikimedia.add("authorization", "")
	wikimedia["authorization"].comment("Unset, currently not used, as Wikimedia does not require it")

	defaults = tomlkit.document()
	defaults.add("general", general)
	defaults.add("daemon", daemon)
	defaults.add("bing", bing)
	defaults.add("unsplash", unsplash)
	defaults.add("wikimedia", wikimedia)

	return defaults

def load_settings():
	if os.path.exists(local_path):
		settings = tomlkit.parse(open(local_path, mode='r').read())
	elif os.path.exists(user_path):
		settings = tomlkit.parse(open(user_path, mode='b+r').read())
	else:
		settings = default_settings()
		os.makedirs(os.path.dirname(user_path), exist_ok=True)
		with open(user_path, mode='w') as file:
			tomlkit.dump(settings, file)
	return settings