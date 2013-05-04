#!/usr/bin/env python3
"""
    Spampot Runner Application
    Copyright (C) 2013 William A. Kennington III

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import smtp
import os
import configparser
import argparse
import logging, logging.handlers

def serve(log, config):
    log.debug('Opening Server')
    addr = config['Global'].get('addr', '0.0.0.0')
    port = config['Global'].get('port', 25)
    host = config['Global'].get('host', 'localhost')
    server = smtp.SMTP(host=host, port=port, addr=addr)
    server.run()
    exit(0)

def daemonize(log, config):
    log.debug('Forking Daemon')

    # Perform the first fork
    try: 
        pid = os.fork() 
        if pid > 0:
            exit(0) 
        log.debug('First Fork to pid %d' % pid)
    except OSError as e:
        log.error('Failed to fork daemon process')
        exit(1)

    # Decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    # Perform the second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            exit(0) 
        log.debug('Second Fork to pid %d' % pid)
    except OSError as e:
        log.error('Failed to fork daemon process')
        exit(1) 

    # Begin Execution
    serve(log, config) 

def normal(log, config):
    serve(log, config)

def run():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Spawn the spampot server')
    parser.add_argument('--conf', '-c', dest='conf', metavar='c', type=str, default='spampot.conf', help='Configuration file to read')
    parser.add_argument('--daemon', '-d', metavar='d', dest='daemon', type=bool, default=None, help='False to serve in current process or True to spawn workers')
    parser.add_argument('--log-level', '-L', metavar='L', dest='log_level', type=str, default=None, help='Level of Logging to display')
    parser.add_argument('--log', '-l', dest='logs', metavar='file', type=str, default=None, nargs='+', help='The logfile[s] to write into')
    args = parser.parse_args()

    # Read the default configuration file
    config = configparser.ConfigParser()
    config.read(args.conf)
    if not ('Global' in config.sections()):
        print('Configuration file is missing the "Global" section')
        exit(1)

    # Merge config with command line arguments
    logs = args.logs if args.logs else config['Global'].get('log', 'syslog').split(' ')
    log_level = args.log_level if args.log_level else config['Global'].get('log_level', 'INFO').upper()
    daemon = args.daemon if args.daemon == None else config['Global'].get('daemon', True)

    # Setup the logger
    logger = logging.getLogger('Global')
    logger.setLevel(log_level)
    for log in [log for log in logs if daemon and log != '-']:
        if log == 'syslog':
            logger.addHandler(logging.handlers.SysLogHandler())
        if log == '-':
            logger.addHandler(logging.handlers.StreamHandler(sys.stdout))
        else:
            logger.addHandler(logging.handlers.RotatingFileHandler(log))

    # Perform the requested service
    daemonize(logger, config) if daemon else normal(logger, config)

    exit(0)

if  __name__ == '__main__':
    run()
