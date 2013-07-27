import logging

def logger_factory(name, filename='default'):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	if filename == 'default':
		filename = name + '.log'
	file_handler = logging.FileHandler(filename)
	format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
	file_handler.setFormatter(format)
	logger.addHandler(file_handler)
	return logger