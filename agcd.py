#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Approximate Greatest Common Divisor Class
    Based on the paper "AGCD: a robust periodicity analysis method based on approximate greatest common divisor"
"""

__author__ = "Paolo Di Prodi"
__copyright__ = "Copyright 2018, Paolo Di Prodi"
__license__ = "Apache"
__version__ = "2.0"
__email__ = "paolo [AT] logstotal [dot] com"
__status__ = "Production"

import math
import itertools
import random

class AGCDException(Exception):
    pass

class AGCD(object):

    def __init__(self):

        self.occur = {}

    def make_noise_interval(self):

        r_int = math.floor(self.r)

        if r_int <= 1 :
            return [0]
        else:
            interval = [i for i in range(0,r_int)]

            return interval

    def period_histogram(self,time_events,is_sorted = False, dupes = True):

        typecheck = all(isinstance(x, int) for x in time_events)

        if typecheck:
            if dupes:
                sorted_events = list(set(time_events))
            else:
                sorted_events = time_events

            if len(sorted_events) == 0:
                raise AGCDException("There are no events to parse")
            elif len(sorted_events) == 1:
                raise AGCDException("Unable to infer period from one sample")

            if is_sorted == False:
                sorted_events = sorted(sorted_events)

            diff_time = [sorted_events[n] - sorted_events[n - 1] for n in range(1, len(sorted_events))]

            self.dim = len(diff_time)

            self.tmin = min(diff_time)

            self.r = math.sqrt(self.tmin)
            self.r_int = self.make_noise_interval()

            D = [sorted_events[n] - sorted_events[0] for n in range(1, len(sorted_events))]

            D_pairs = itertools.combinations(D, 2)

            for d in D_pairs:

                for ri in self.r_int:
                    for rj in self.r_int:

                        g = math.gcd(d[0] + ri, d[1] + rj)

                        if g >= self.tmin:
                            if g in self.occur:
                                self.occur[g] += 1
                            else:
                                self.occur[g] = 1

        else:
            raise AGCDException("Only integers time events supported")

    def entropy_histogram(self,base=2):
        '''
        Compute the entropy of the histogram
        :return: float
        '''

        total = 0.0

        norm = sum(list(self.occur.values()))

        vals = [v / norm for v in list(self.occur.values())]

        for v in vals:
            total += (v * math.log(v,base))

        return -1.0 * total

    def period_max(self):

        max_g = max(self.occur, key=lambda k: self.occur[k])

        return max_g

    def print_histogram(self):

        sorted_keys = sorted(self.occur, key=self.occur.get, reverse=True)

        for key in sorted_keys:
            print("g {0} count {1}".format(key,self.occur[key]))


