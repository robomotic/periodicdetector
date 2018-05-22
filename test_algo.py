#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Approximate Greatest Common Divisor Unit Test
    Based on: AGCD: a robust periodicity analysis method based on approximate greatest common divisor
"""

__author__ = "Paolo Di Prodi"
__copyright__ = "Copyright 2018, Logstotal"
__license__ = "Apache"
__version__ = "2.0"
__email__ = "paolo [AT] logstotal [dot] com"
__status__ = "Production"

import unittest
import math
import itertools
import random
from agcd import AGCD


def frange(start, stop, step=1.0):
    while start < stop:
        yield start
        start += step

class TestPeriodic(unittest.TestCase):
    '''
    Unit Test of the main class
    '''


    def test_simple(self):
        '''
        Very simple and short period
        :return:
        '''
        time_events = [0,2,4,6,8,10]

        agcd = AGCD()

        agcd.period_histogram(time_events)

        self.assertEqual(len(time_events), agcd.dim+1)

        period = agcd.period_max()

        self.assertEqual(2,period)


    def test_large(self):
        '''
        Add offset to series
        :return:
        '''

        time_events = [2000,4000,6000,8000,10000]

        agcd = AGCD()

        agcd.period_histogram(time_events)

        period = agcd.period_max()

        print("Maximum period found p = %d " % period)

        self.assertEqual(2000,period)


    def test_approx(self):
        '''
        Introduce some noise in the period
        :return:
        '''
        time_events = [1,19,41,65,81,99]

        agcd = AGCD()

        agcd.period_histogram(time_events)

        period = agcd.period_max()

        print("Maximum period found p = %d " % period)

        self.assertEqual(20,period)

    def test_missing(self):
        '''
        Introduce missing events in the series
        :return:
        '''
        time_events = [1,19,65,81,99,142]

        agcd = AGCD()

        agcd.period_histogram(time_events)

        period = agcd.period_max()

        print("Maximum period found p = %d " % period)

        self.assertEqual(period,20)

    def series_generator(self,total,p,offset,noise_mag,noise_p,missing):
        missing_idx = []

        for x in range(missing):
            missing_idx.append(random.randint(0, total-1))

        events = [ ]
        missing_count = 0
        for i in range(offset,total):

            #check if period needs to be skipped
            if i not in missing_idx:
                if random.random() > noise_p:
                    if random.randint(0,1) == 1:
                        events.append(p * i + noise_mag)
                    else:
                        events.append(p * i - noise_mag)
                else:
                    events.append(p*i)
            else:
                missing_count+=1

        return events


    def test_complete(self):
        '''
        More exaustive test with random noise and random missing entries
        :return:
        '''

        # fix random generator
        random.seed(5)

        # define the sequence length
        total = 100
        # define the period
        period = 10

        # first event time
        offset = random.randint(1,2)

        # define the noise range +-1
        noise_mag = 0
        # define the noise probability
        noise_prob = 0.0

        for missing in range(0,math.ceil(total/4)):
            print("Test with {0} events of which {1} missing".format(total,missing))
            events = self.series_generator(total,period,offset,noise_mag,noise_prob,missing)

            agcd = AGCD()

            agcd.period_histogram(events)

            period_estimate = agcd.period_max()

            print("Maximum period found p = %d " % period)

            self.assertEqual(period, period_estimate)


        for noise_mag in range(0,2):
            for noise_prob in frange(0.0,0.4,0.1):

                print("Test with {0} events with noise mag {1} and frequency {2:.2f}".format(total,noise_mag,noise_prob))
                events = self.series_generator(total,period,offset,noise_mag,noise_prob,missing)

                agcd = AGCD()

                agcd.period_histogram(events)

                entropy = agcd.entropy_histogram()
                period_estimate = agcd.period_max()

                print("Maximum period found p = {0} ".format( period) )
                print("Binary entropy = {0:.2f}".format(entropy))

                self.assertEqual(period, period_estimate)


    def series_random_generator(self,total,offset,max_value):

        rangeOfNumbers = range(offset, (max_value + 1))

        randomNumList = random.sample(rangeOfNumbers, total)

        randomNumList.sort()

        return randomNumList

    def test_entropy(self):
        '''
        Check if random numbers produces a flat histogram = low entropy
        :return:
        '''

        # fix random generator
        random.seed(5)

        # generates all the numbers in a sequence
        events = self.series_random_generator(10,0,10)

        self.assertListEqual(events,list(range(0,10)))

        agcd = AGCD()

        agcd.period_histogram(events)

        entropy = agcd.entropy_histogram()
        period_estimate = agcd.period_max()

        print("Maximum period found p = {0} ".format(period_estimate))
        print("Binary entropy = {0:.2f}".format(entropy))

        agcd.print_histogram()

        self.assertAlmostEqual(1.15,entropy,places=2)

        events = self.series_random_generator(10, 0, 100)

        agcd = AGCD()

        agcd.period_histogram(events)

        entropy = agcd.entropy_histogram()
        period_estimate = agcd.period_max()

        print("Maximum period found p = {0} ".format(period_estimate))
        print("Binary entropy = {0:.2f}".format(entropy))

        agcd.print_histogram()

        self.assertGreater(1.9,entropy)

if __name__ == '__main__':
    unittest.main()
