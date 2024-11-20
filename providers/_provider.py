from abc import abstractmethod, ABC


class Provider(ABC):
	name = None
	url = None

	def __init__(self, settings, session):
		self.settings = settings
		self.session = session

	@abstractmethod
	def get_image_info(self):
		pass