import os
import sys
import subprocess
import logging
import time
import paramiko
import pxssh
import configparser

from autotest.client import test, utils
from autotest.client.shared import error, utils_memory


class rf_temperature_sensor(test.test):

    """
    Autotest module for power test.

    @author: vkancharla@fb.com 
    """
    version = 2
    preserve_srcdir = True

    def initialize(self):
        """
        Verifies if we have gcc to compile disktest.
        """
        logging.info('INSIDE INIT FUNCTION')
    def build(self, srcdir):
        """
        Compiles disktest.
        """
        logging.info('INSIDE BUILD')

    def run_once(self, test_path='', rasp_ip=None, user=None, relay_num=None, on_off=None):
        """
        Runs one iteration of disktest.

        :param disks: List of directories (usually mountpoints) to be passed
                to the test.
        :param gigabytes: Disk space that will be used for the test to run.
        :param chunk_mb: Size of the portion of the disk used to run the test.
                Cannot be larger than the total amount of free RAM.
        """
        logging.info('TEST CASE XX - AP Test - Manufacturing - RF Temperature Sensor Test')   

        oc_config = configparser.ConfigParser()
        oc_config.read(test_path.split('autotest')[0] + 'autotest/config/oc_config.ini')
        iperfsrv_user = oc_config.get('iperfsrv', 'user')
        iperfsrv_passwd = oc_config.get('iperfsrv', 'passwd')
        iperfsrv_ip = oc_config.get('iperfsrv', 'ip')
        oc_user = oc_config.get('oc', 'user')
        oc_passwd = oc_config.get('oc', 'passwd')
        oc_ip = oc_config.get('oc', 'ip')

        # Poll process for new output until finished
        s = pxssh.pxssh(timeout=500, maxread=2000000)
        s.login(oc_ip,oc_user,oc_passwd,auto_prompt_reset=False)
        logging.info('CONFIGURING UART LINK....')
        s.sendline('/home/oc/host/ocmw/ocmw_usb')
        time.sleep(5)


        logging.info('COLLECTING RF sensor temperature ....')
        rf_temp = subprocess.check_output('/home/oc/host/ocmw/occmd get status rf.ch1_sensor.temperature', shell=True) 
        time.sleep(5)
        logging.info('rf sensor temperature is : %s',rf_temp)

        rfch1_temp = 0

        if 'rf.ch1_sensor.temperature' in rf_temp:
            if isinstance(rf_temp.split(' = ')[1], int):
                rfch1_temp = int(rf_temp.split(' = ')[1])
            logging.info('RF SENSOR TEMPERATURE IS %s',rfch1_temp)  

        if (rfch1_temp > 0):
            logging.info('TEMPERATURE SENSOR ON RF SENSOR IS WORKING FINE')
        else:
            logging.info('TEMPERATURE SENSOR ON RF SENSOR IS NOT WORKING FINE')
            raise ValueError('WRONG DATA') 

        s.close()


