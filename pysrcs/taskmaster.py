#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import errors
import tools
import classes
import userinput
import output
import time
import signals
import menuloop
import execution
import logging

import sys
import json
import subprocess

def main():
	"""main function"""
	try:
		with open(sys.argv[1], 'r') as config:
			config_list = json.load(config)
			config.close()
			if config_list['log-active'] == True and config_list['log-file'].find('pysrcs/') == -1:
				logging.basicConfig(filename=f'{config_list["log-file"]}',
								level=logging.DEBUG,
								filemode='w',
								format='%(asctime)s %(levelname)s\t%(message)s')
			elif config_list['log-active'] == True:
				userinput.ask_for_confirmation(None, None, "log-file", 0)
	except Exception as error_log:
		if str(error_log).find("Errno 13") != -1:
			errors.permission_config_error()
		userinput.ask_for_confirmation(None, None, error_log, 0)
	errors.error_check_params()
	signals.set_signal_handlers_taskmaster()
	output.display_progress()
	start = time.time()
	configList = tools.parse_json_file()
	if configList == None:
		errors.parse_error()
	tools.verify_config(0, configList)
	programList = classes.init_classes(configList)
	end = time.time()
	userinput.ask_for_confirmation(programList,
									str(end - start),
									None, 0)
	execution.load_or_reload(programList, None)
	menuloop.setuploop(programList, configList)

if __name__ == '__main__':
	main()
