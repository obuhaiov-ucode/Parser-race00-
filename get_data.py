import yaml
import json

def get_data(path = None, extension = None):
	if isinstance(path, str):
		if not extension:
			extension = path.split(".")[-1]
		try:
			with open(path, "r") as fd:
				if extension == "json":
					return json.load(fd)
				elif extension == "yaml":
					return yaml.safe_load(fd)
		except:
			return None
	return None