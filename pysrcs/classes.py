"""File to store all class related functions"""
import logging

class Program:
	"""base class for all programs to be executed"""

	def __init__(self, config):
		"""assigns config for a program to his object"""
		self.config = config
		self.pidList = []
		self.name = config[0]
		self.cmd = config[1]
		self.cmdammount = config[2]
		self.autostart = config[3]
		self.autorestart = config[4]
		self.starttime = config[5]
		self.stoptime = config[6]
		self.restartretries = config[7]
		self.quitsig = config[8]
		self.exitcodes = config[9]
		self.workingdir = config[10]
		self.umask = config[11]
		self.stdout = config[12]
		self.stderr = config[13]
		self.env = config[14]
		self.started = False
		if self.autostart != 1:
			self.state = "Not started"
		else:
			self.state = "Starting"
		self.selected = 0

	def update_state(self):
		"""function that updates state after X time has run"""
		self.state = "Started"

def init_classes(configList):
	"""initialises program classes with their corresponding config"""
	logging.info(f'Initializing programs list')
	programList = []
	for config in configList:
		newClass = Program(config)
		programList.append(newClass)
	logging.info(f'Programs list initilized')
	return programList
