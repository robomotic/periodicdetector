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
from agcd import AGCD,AGCDException
import os,sys
import requests
import shutil
import csv

if sys.version_info[0] < 3:
    from urlparse import urlsplit,urlunsplit
    import codecs
else:
    from urllib.parse import urlsplit,urlunsplit


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
    Unit Test for web log files
    '''

    WEBLOG_FILE = None

    def test_1_pull_weblog(self):
        url = r'https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-89-1/2014-09-15_capture-win2.weblogng'

        TestMalware.WEBLOG_FILE = download_file(url)

        self.assertTrue(os.path.exists(TestMalware.WEBLOG_FILE))

    def test_2_process_weblog(self):

        if sys.version_info[0] >= 3:
            with open(TestMalware.WEBLOG_FILE, 'r',encoding='utf-8',errors='ignore') as f:

                http_data = []
                filtered = [line.replace('\0', '') for line in f]
                reader = csv.DictReader(filtered, delimiter='\t')

                try:
                    for row in reader:

                        info = {key: row[key] for key in row.keys() if key in ['timestamp','cs-method','cs-url','s-ip','c-ip']}
                        # keep only second resolution
                        info['timestamp'] = round(float(info['timestamp']))
                        url_parse = urlsplit(info['cs-url'])

                        info['cs-url-wo-query'] = urlunsplit((url_parse[0],url_parse[1],url_parse[2],None,None))

                        if 'msg.video.qiyi.com' in row['cs-url']:
                            http_data.append(info)

                except UnicodeDecodeError as e:
                    sys.exit('file %s, line %d: %s' % (TestMalware.WEBLOG_FILE, reader.line_num, e))
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (TestMalware.WEBLOG_FILE, reader.line_num, e))

                print("Known beacon http requests %d" % len(http_data))

                # aggregate time over source IP and URL
                connection_events = {}
                for http_request in http_data:
                    key = (http_request['s-ip'],http_request['cs-url-wo-query'])

                    if key in connection_events:
                        connection_events[key]+=[http_request['timestamp']]
                    else:
                        connection_events[key] = [http_request['timestamp']]

                total_found = 0
                for (source,url) in connection_events.keys():
                    event_seconds = connection_events[(source,url)]
                    print("Beacon detection for source = {0} and url = {1}".format(source,url))

                    agcd = AGCD()

                    agcd.period_histogram(event_seconds)

                    entropy = agcd.entropy_histogram()

                    if entropy > 4.0:
                        period_estimate = agcd.period_max()

                        print("Maximum period found p = {0} ".format(period_estimate))
                        print("Binary entropy = {0:.2f}".format(entropy))
                        total_found+=1
                    else:
                        print("Entropy too high")
                print("Found in total {0} IP addresses beaconing".format(total_found))
                self.assertEqual(13,total_found)

    def test_3_process_weblog(self):

        if sys.version_info[0] >= 3:
            f = open(TestMalware.WEBLOG_FILE, 'r',encoding='utf-8',errors='ignore')

        else:
            f = codecs.open(TestMalware.WEBLOG_FILE, 'r', errors = 'ignore')

        if f:
            http_data = []
            filtered = [line.replace('\0', '') for line in f]
            reader = csv.DictReader(filtered, delimiter='\t')

            try:
                for row in reader:

                    info = {key: row[key] for key in row.keys() if key in ['timestamp','cs-method','cs-url','s-ip','c-ip']}
                    # keep only second resolution
                    info['timestamp'] = int(round(float(info['timestamp'])))
                    url_parse = urlsplit(info['cs-url'])

                    info['cs-url-wo-query'] = urlunsplit((url_parse[0],url_parse[1],url_parse[2],None,None))

                    http_data.append(info)

            except UnicodeDecodeError as e:
                sys.exit('file %s, line %d: %s' % (TestMalware.WEBLOG_FILE, reader.line_num, e))
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (TestMalware.WEBLOG_FILE, reader.line_num, e))

            # aggregate time over source IP and URL
            connection_events = {}
            for http_request in http_data:
                key = (http_request['s-ip'],http_request['cs-url-wo-query'])

                if key in connection_events:
                    connection_events[key]+=[http_request['timestamp']]
                else:
                    connection_events[key] = [http_request['timestamp']]

            total_found = 0
            for (source,url) in connection_events.keys():
                event_seconds = connection_events[(source,url)]

                if len(event_seconds)>1:
                    agcd = AGCD()

                    try:
                        agcd.period_histogram(event_seconds)

                        entropy = agcd.entropy_histogram()

                        if entropy > 4.0:
                            print("Beacon detection for source = {0} and url = {1} with {2} events".format(source, url,len(event_seconds)))

                            period_estimate = agcd.period_max()

                            print("Maximum period found p = {0} ".format(period_estimate))
                            print("Binary entropy = {0:.2f}".format(entropy))
                            total_found+=1

                    except AGCDException as e:
                        print(e)

            print("Found in total {0} IP addresses beaconing".format(total_found))
            self.assertEqual(21,total_found)


if __name__ == '__main__':
    unittest.main()
