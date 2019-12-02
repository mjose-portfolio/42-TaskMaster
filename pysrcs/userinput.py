"""File dedicated to user input handling"""

import output
import sys
import termios
import logging

import curses
import errors

def ask_for_confirmation(programList, time, error, mode):
	"""Asks for confirmation of current setup"""
	logging.info(f'Asking the user if he wants to continue')
	if time != None:
		output.display_summary(programList, time)
	else:
		errors.error_log(error)
	confirmation = input().lower()
	while confirmation != 'y' and confirmation != "yes":
		if confirmation == 'n' or confirmation == "no":
			print(output.bcolors.FAIL, "\n/!\\ Aborting execution /!\\",
			output.bcolors.ENDC)
			logging.info(f'User input {confirmation}, exit Taskmaster with RC=0.')
			if mode == 0:
				sys.exit(0)
			else:
				return 1
		logging.info(f'User input invalid:"{confirmation}". Re-asking')
		print("Please answer with yes/y or no/n")
		confirmation = input().lower()
	logging.info(f'User input "{confirmation}".')

def ask_for_reload_confirmation():
	"""Asks for confirmation of reload action"""
	logging.info(f'Asking the user if he wants to continue the reload process')
	confirmation = input("\nWould you really like to reload the config file (y/n)? Some processes could be killed...\n").lower()
	while confirmation != 'y' and confirmation != "yes":
		if confirmation == 'n' or confirmation == "no":
			print(output.bcolors.FAIL, "\n/!\\ Reload didn't take effect /!\\",
			output.bcolors.ENDC)
			logging.info(f'User input {confirmation}, reload not processed.')
			return 0
		logging.info(f'User input invalid:"{confirmation}". Re-asking')
		print("Please answer with yes/y or no/n")
		confirmation = input().lower()
	logging.info(f'User input "{confirmation}".')
	return 1

def ask_for_exit_kill_confirmation():
	"""Asks for confirmation of killing all remaining jobs at exit action"""
	logging.info(f'Asking the user if he wants to kill all remaining jobs')
	confirmation = input("\nYou are about to exit Taskmaster, would you like to kill all remaining jobs (yes/no/cancel)?\n").lower()
	while confirmation != 'y' and confirmation != "yes" and confirmation != 'n' and confirmation != "no" and confirmation != 'c' and confirmation != "cancel":
		logging.info(f'User input invalid:"{confirmation}". Re-asking')
		print("Please answer with yes/y, no/n or cancel/c")
		confirmation = input().lower()
	logging.info(f'User input "{confirmation}".')
	return confirmation
