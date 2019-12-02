"""General module for signal handling"""

import signal
import logging

import menuloop

def reset_signal_handlers_process():
	"""Ignores all signals for taskmaster except SIGCHLD"""
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	signal.signal(signal.SIGQUIT, signal.SIG_DFL)
	signal.signal(signal.SIGTSTP, signal.SIG_DFL)
	signal.signal(signal.SIGCONT, signal.SIG_DFL)
	signal.signal(signal.SIGTTIN, signal.SIG_DFL)
	signal.signal(signal.SIGTTOU, signal.SIG_DFL)
	signal.signal(signal.SIGCHLD, signal.SIG_DFL)
	signal.signal(signal.SIGHUP, signal.SIG_DFL)
	signal.signal(signal.SIGWINCH, signal.SIG_DFL)
	signal.signal(signal.SIGHUP, signal.SIG_DFL)
	logging.info(f'Signal handlers reset.')

def set_signal_handlers_taskmaster():
	"""Ignores all signals for taskmaster except SIGCHLD"""
	logging.info(f'Setting signal handlers...')
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	signal.signal(signal.SIGQUIT, signal.SIG_IGN)
	signal.signal(signal.SIGTSTP, signal.SIG_IGN)
	signal.signal(signal.SIGCONT, signal.SIG_IGN)
	signal.signal(signal.SIGTTIN, signal.SIG_IGN)
	signal.signal(signal.SIGTTOU, signal.SIG_IGN)
	signal.signal(signal.SIGCHLD, signal.SIG_DFL)
	logging.info(f'Signal handlers set.')

