"""File for general output purposes"""

import sys

class bcolors:
	CYA = '\033[36m'
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	REV	= '\033[7m'
	UNDERLINED = '\033[4m'

def display_status(programList, args):
	"""Displays program's status"""
	print('\r', end='')
	print("                                              ")
	print("\r################################")
	print(bcolors.HEADER, "STATUS\n", bcolors.ENDC)
	args = args.split(' ')
	checker = 0
	if len(args) >= 1:
		for c in args:
			if c.isalpha():
				checker = 1
				break
	if checker == 0:
		args = ""
	if len(args) > 0:
		newProgramList = []
		for name in args:
			for program in programList:
				counter = 0
				if name == program.name:
					counter += 1
					newProgramList.append(program)
					break
			if counter == 0:
				print(bcolors.FAIL + "Program: " + name + " not found!" + bcolors.ENDC)
				print(bcolors.FAIL + "Possible programs: " + bcolors.ENDC)
				for program in programList:
					print(bcolors.FAIL + program.name + bcolors.ENDC)
				return
		programList = newProgramList
	for program in programList:
		print(bcolors.UNDERLINED, program.name, bcolors.ENDC)
		print("      ", "Command ->", program.cmd)
		print("      ", "State ->", end='')
		if program.state == "Running" or program.state == "Starting":
			print(bcolors.OKGREEN, program.state, bcolors.ENDC, end='')
			if program.state == "Starting":
				print(bcolors.OKGREEN, '(' + str(program.starttime) + ' seconds)', bcolors.ENDC)
			elif program.state == "Stopped":
				print(bcolors.OKGREEN, '(' + 'SIGKILL (9)' + ')', bcolors.ENDC)
			else:
				print()
		elif program.state == "Not started" or program.state == "Stopped" or program.state == "Finished" or program.state == "Stopping" :
			print(bcolors.FAIL, program.state, bcolors.ENDC, end='')
			if program.state == "Stopping":
				print(bcolors.FAIL, '(' + str(program.stoptime) + ' seconds)', bcolors.ENDC)
			elif program.state == "Stopped":
				print(bcolors.FAIL, '(' + 'SIGKILL (9)' + ')', bcolors.ENDC)
			else:
				print()
		else:
			print(bcolors.CYA, program.state, bcolors.ENDC)
		if len(program.pidList) > 0:
			print("      ", "Instances ->", program.cmdammount)
			for pid in program.pidList:
				print("             ", pid[0].pid, "->", pid[1], end='')
				if pid[2] != None:
					if pid[1] == "Finished" or pid[1] == "Stopped" or pid[1] == "Stopping":
						print(" with exitcode ->", pid[2], end='')
						if int(pid[2]) != 0 and int(pid[2]) != 1:
							print(" (Probably Killed)")
						else:
							print()

				else:
					print('')
		print("      ", "stdout ->", "n/a")
		print("      ", "stderr ->", "n/a")
		if program.autorestart == "always":
			print("      ", "Restart ->", "always")
		elif program.autorestart == "never":
			print("      ", "Restart ->", "never")
		if program.autorestart == "unexpected":
			print("      ", "Restart ->", "on exitcodes different from -> ", end='')
			if isinstance(program.exitcodes, str):
				print(program.exitcodes, end=' ')
			else:
				for code in program.exitcodes:
					print(code, end=' ')
			print('\n', end='')
		print(f'       Start time -> {program.starttime}\n       Stop time -> {program.stoptime}')
	print("\n################################\n")

def display_special_str(str, mode, newline):
	"""Displays strings normally, underlined, or underlined + reversed"""
	if mode == 0:
		print(str, end=' ')
	elif mode == 1:
		print(bcolors.REV, str, bcolors.ENDC, end='')
	if newline == True:
		print('\n')

def display_summary(classList, time):
	"""Displays a summary of the config file and the programs that are about
	to be loaded
	"""
	print("took -> " + time[:-14] + " seconds")
	print("config file summary: \n")
	for instance in classList:
		print("Name:", bcolors.BOLD, instance.name, bcolors.ENDC)
		print("Cmd:", bcolors.BOLD, instance.cmd, bcolors.ENDC)
		print("Cmd ammount:", bcolors.BOLD, instance.cmdammount, bcolors.ENDC)
		print("Autostart:", bcolors.BOLD, instance.autostart, bcolors.ENDC)
		print("Autorestart:", bcolors.BOLD, instance.autorestart, bcolors.ENDC)
		print("Starttime:", bcolors.BOLD, instance.starttime, bcolors.ENDC)
		print("Stoptime:", bcolors.BOLD, instance.stoptime, bcolors.ENDC)
		print("Restartretries:", bcolors.BOLD, instance.restartretries,
		bcolors.ENDC)
		print("Quitsig:", bcolors.BOLD, instance.quitsig, bcolors.ENDC)
		print("Exitcodes:", bcolors.BOLD, instance.exitcodes, bcolors.ENDC)
		print("Workingdir:", bcolors.BOLD, instance.workingdir, bcolors.ENDC)
		print("Umask:", bcolors.BOLD, instance.umask, bcolors.ENDC)
		print("Stdout:", bcolors.BOLD, instance.stdout, bcolors.ENDC)
		print("Stderr:", bcolors.BOLD, instance.stderr, bcolors.ENDC)
		print("env:", bcolors.BOLD, instance.env, bcolors.ENDC)
		print('\n')
	print("#####################################################")
	print(bcolors.HEADER + "Would you really like to load this configuration"
	+ "? y/n" + bcolors.ENDC)
	print("#####################################################")

def display_progress():
	"""Displays a little progress message"""
	print(bcolors.OKGREEN + "Processing config..." + bcolors.ENDC, end=' ')
