"""File for general tooling"""
import sys
import json
import os
import signal
import logging

import errors

configFile = None

def delete_instances(program, nb):
    """kills nb instances of desired job"""
    if nb > 0 and program.state != "Finished" and program.state != "Stopped" and program.state != "Not started":
        for pid in program.pidList:
            if nb == 0:
                return
            if pid[1] != "Finished" and pid[1] != "Stopped":
                os.kill(pid[0].pid, signal.SIGKILL)
            nb -= 1
    logging.info(f'All instances of {program.name} were killed')

def kill_job(program):
    """kills selected job"""
    if program.state != "Finished" and program.state != "Stopped" and program.state != "Not started":
        for pid in program.pidList:
            if pid[1] != "Finished" and pid[1] != "Stopped":
                os.kill(pid[0].pid, signal.SIGKILL)
    logging.info(f'Job: {program.name} was killed')

def kill_jobs(programList):
    """kills remaining processes on exit"""
    for program in programList:
        if program.state != "Finished" and program.state != "Stopped" and program.state != "Not started":
            for pid in program.pidList:
                if pid[1] != "Finished" and pid[1] != "Stopped":
                    os.kill(pid[0].pid, signal.SIGKILL)
    logging.info(f'All jobs were killed on exit')

def verify_config(mode, configList):
    """Verifies that the parsed yaml file doesn't contain any errors and has
    all required parameters
    """
    i = 0
    totalinstances = 0
    logging.info(f'Checking configuration...')
    while i < len(configList):
        j = i + 1
        totalinstances += configList[i][2]
        while j < len(configList):
            if configList[i][0] == configList[j][0]:
                return errors.error_repeated_names(mode)
            j += 1
        i += 1
    if totalinstances >= 400:
       return errors.error_instances(mode, totalinstances)
    logging.info(f'{totalinstances} instances have been found')
    for config in configList:
        if len(config) != 15:
            return errors.error_config_len(mode, len(config))
        elif isinstance(config[0], str) != True:
            return errors.error_config(mode, config[0], "name")
        elif isinstance(config[1], str) != True:
            return errors.error_config(mode, config[0], "cmd")
        elif isinstance(config[2], int) != True or config[2] < 1:
            return errors.error_config(mode, config[0], "cmdammount")
        elif config[2] < 1:
            return errors.error_ammount_cmds(mode, config[0])
        elif isinstance(config[3], bool) != True or (config[3] != True and config[3] != False):
            return errors.error_config(mode, config[0], "autostart")
        elif isinstance(config[4], str) != True or (config[4] != "never" and config[4] != "always"
        and config[4] != "unexpected"):
            return errors.error_config(mode, config[0], "autorestart")
        elif config[5] < 0 or isinstance(config[5], int) != True:
            return errors.error_config(mode, config[0],
            "starttime/stoptime/restartretries")
        elif config[6] < 0 or isinstance(config[6], int) != True:
            return errors.error_config(mode, config[0],
            "starttime/stoptime/restartretries")
        elif config[7] < 0 or isinstance(config[7], int) != True:
            return errors.error_config(mode, config[0],
            "starttime/stoptime/restartretries")
        elif (isinstance(config[8], str) != True or (config[8] != "TERM" and
        config[8] != "QUIT" and config[8] != "INT" and config[8] != "KILL"
        and config[8] != "TSTP" and config[8] != "STOP" )):
            return errors.error_config(mode, config[0], "quitsig")
        elif config[9] != "None" and isinstance(config[9], list) != True:
            return errors.error_config(mode, config[0], "exitcodes")
        elif isinstance(config[10], str) != True or os.path.isdir(config[10]) == False:
            return errors.error_config(mode, config[0], "workingdir")
        elif isinstance(config[11], str) != True and isinstance(config[11], int) != True:
            return errors.error_config(mode, config[0], "umask")
        elif isinstance(config[12], str) != True:
            return errors.error_config(mode, config[0], "stdout")
        elif isinstance(config[13], str) != True:
            return errors.error_config(mode, config[0], "stdin")
        elif config[14] != "None" and isinstance(config[14], list) != True:
            return errors.error_config(mode, config[0], "env")
        if config[10][len(config[10]) - 1] != '/':
            config[10] += '/'
        if isinstance(config[14], list):
            for e in config[14]:
                if e.count('=') != 1:
                    return errors.error_config(mode, config[0], "env")
        if isinstance(config[9], list):
            for e in config[9]:
                if isinstance(e, int) == False:
                    return errors.error_config(mode, config[0], "exitcodes")
        logging.info(f'Config verified succesfully: {config[0]}')

def parse_json_file():
    """parses the json config file and returns it to the main function"""
    try:
        logging.info(f'Opening config file... {sys.argv[1]}')
        configList = None
        global configFile
        if configFile == None:
            file = sys.argv[1]
            configFile = os.getcwd() + "/" + sys.argv[1]
        else:
            file = configFile
        with open(file, 'r') as stream:
            logging.info(f'Config file {sys.argv[1]} open.')
            logging.info(f'Loading config file... {sys.argv[1]}')
            configload = json.load(stream)
            for data in configload:
                if data != "programs":
                    break
                configList = []
                for program in configload[data]:
                    config = []
                    config.append(program)
                    for param in configload[data][program]:
                        config.append(configload[data][program][param])
                    configList.append(config)
            logging.info(f'Config file {sys.argv[1]} loaded.')
    except Exception as e:
        return errors.error_json(f"Json file: {e}", 1, e)
    return configList
