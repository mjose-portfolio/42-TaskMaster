"""General error output and handling file"""
import sys
import output
import logging

def permission_config_error():
	print(output.bcolors.FAIL + "Permission denied when loading the configuration file, exiting gracefully...", output.bcolors.ENDC, file=sys.stderr)
	sys.exit(1)

def parse_error():
	logging.error(f'There was a fatal error while parsing the config file, exiting gracefully...')
	print(output.bcolors.FAIL + "There was a fatal error while parsing the config file, exiting gracefully...", output.bcolors.ENDC, file=sys.stderr)
	sys.exit(1)

def error_execution(str):
	logging.error(f'There was an error starting command: {str}')
	print(output.bcolors.FAIL + "There was an error starting command:", str,
	", not executing any instance of this command", output.bcolors.ENDC, file=sys.stderr)

def error_reload_config():
	logging.error(f'There was an error reloading the config file, staying on old config')
	print(output.bcolors.FAIL + "There was an error reloading the config file" +
	", staying on old config", output.bcolors.ENDC, file=sys.stderr)

def error_ammount_cmds(mode, str):
	"""error for when a command has less than 1 instance in config file"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("command -> " + str + " has less than one desired instance"
	+ "in the config file", file=sys.stderr)
	if mode == 0:
		logging.error(f'Command {str} has less than one desired instance'
		+ f' in the config file, exit TaskMaster. RC=1')
		sys.exit(1)
	logging.error(f'Command {str} has less than one desired instance'
	+ f' in the config file')
	return 1

def error_config(mode, command, param):
	"""Base error function for config file errors"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("command -> ", end='', file=sys.stderr)
	print(command, end=' ', file=sys.stderr)
	print("has ", end='', file=sys.stderr)
	print(param, end=' ', file=sys.stderr)
	print("not set correctly in the config file", file=sys.stderr)
	if mode == 0:
		logging.error(f'Command {command} has {param} not seted'
		+ f' correctly in the config file, exit TaskMaster. RC=1')
		sys.exit(1)
	logging.error(f'Command {command} has {param} not seted'
	+ f' correctly in the config file')
	return (1)

def error_json(exc, mode, e):
	"""error function for when json file doesn't load"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print(exc, file=sys.stderr)
	print("bad formatting or error loading json file", file=sys.stderr)
	logging.error(f'Json file {sys.argv[1]} can\'t be load: {e}, exit TaskMaster RC=1')
	if mode == 0:
		sys.exit(1)
	return None

def error_repeated_names(mode):
	"""error function for when there's repeated program names"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("Repeated command names!", file=sys.stderr)
	if mode == 0:
		logging.error(f'Invalid program names have been detected. Exit TaskMaster RC=1')
		sys.exit(1)
	logging.error(f'Invalid program names have been detected.')
	return (1)

def error_instances(mode, totalinstances):
	"""error function for when the yaml file contains too many instances"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("Too many instances of some program in config file (fork bomb)", file=sys.stderr)
	if mode == 0:
		logging.error(f'{totalinstances} instances have been found, the limit is 400, exit TaskMaster. RC=1')
		sys.exit(1)
	logging.error(f'{totalinstances} instances have been found, the limit is 400')
	return (1)

def error_names(mode, totalinstances):
	"""error function for when there's repeated names"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("Too many programs with the same name (max 1)", file=sys.stderr)
	if mode == 0:
		logging.error(f'There were multiple programs with the same name. RC=1')
		sys.exit(1)
	logging.error(f'There were multiple programs with the same name. RC=1')
	return (1)

def error_config_len(mode, len_param):
	"""error function for when the json file doesn't contain all the fields"""
	print('\n' + "taskmaster : ", end='', file=sys.stderr)
	print("Not all parameters are present in the config file!", file=sys.stderr)
	if mode == 0:
		logging.error(f'Parameters found {len_param}, expected 15, exit TaskMaster. RC=1')
		sys.exit(1)
	logging.error(f'Parameters found {len_param}, expected 15.')
	return (1)

def error_check_params():
	"""Initial error checking"""
	logging.info('Checking valid params...')
	if len(sys.argv) != 2:
		print("taskmaster : ", end='', file=sys.stderr)
		print("usage: main.py config_file", file=sys.stderr)
		logging.error(f'Invalid params found: arguments found {len(sys.argv)}, expected 2.')
		logging.info(f'Exit TaskMaster RC=1')
		sys.exit(1)
	logging.info('Params checked: VALID')

def error_log(error):
	print(f'Detected error "{error}" opening the log file.\n'
			+ f'Do you want to continue? y/n'
			+ f' (if you continue, it will not be written in the log).', file=sys.stderr)
