#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Approximate Greatest Common Divisor Unit Test for Web logs

    Malware botnet data from: https://mcfp.weebly.com/analysis
"""

__author__ = "Paolo Di Prodi"
__copyright__ = "Copyright 2018, Paolo Di Prodi"
__license__ = "Apache"
__version__ = "2.0"
__email__ = "paolo [AT] logstotal [dot] com"
__status__ = "Production"

import unittest
import math
import itertools
import random
from agcd import AGCD
import os,sys
import requests
import shutil
from scapy.all import *


def download_file(url):
    local_filename = url.split('/')[-1]

    if os.path.exists(local_filename):
        return local_filename

    r = requests.get(url, stream=True,verify=False)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return local_filename


class TestMalware(unittest.TestCase):
    '''
    Unit Test of the main class
    '''
    PCAP_FILE = None
    WEBLOG_FILE = None

    def toobig_test_1_pull_pcap(self):
        '''
        Very simple and short period
        :return:
        '''


        url = r'https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-89-1/2014-09-15_capture-win2.pcap'

        TestMalware.PCAP_FILE = download_file(url)

        self.assertTrue(os.path.exists(TestMalware.PCAP_FILE))

    def toobig_test_2_open_pcap(self):


        # rdpcap comes from scapy and loads in our pcap file
        pcap_log = rdpcap(TestMalware.PCAP_FILE)

        # Let's check the summary
        summary = pcap_log.summary()

        print(summary)

        self.assertTrue(pcap_log!=None)

    def test_1_pull_weblog(self):
        url = r'https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-89-1/2014-09-15_capture-win2.weblogng'

        TestMalware.WEBLOG_FILE = download_file(url)

        self.assertTrue(os.path.exists(TestMalware.WEBLOG_FILE))


if __name__ == '__main__':
    unittest.main()
