# master
import base64
import json
import socket as sock
import time     # for test only
#from matplotlib import pyplot
from multiprocessing import Process

from obspy import *
import numpy as np
import zmq

import logging

logging.basicConfig(format='%(levelname)s %(asctime)s %(funcName)s %(filename)s:%(lineno)d '
                           '%(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


from detector.header_util import unpack_ch_header, prep_name, pack_ch_header, chunk_stream
from detector.test.filter_exp import bandpass_zi
# from detector.test.signal_generator import SignalGenerator


class StaLtaTriggerCore:

    def __init__(self, nsta, nlta):
        self.nsta = nsta
        self.nlta = nlta
        #print('nlta:' + str(nlta))
        self.lta = np.require(np.zeros(nlta), dtype='float32')
        self.sta = np.require(np.zeros(nsta), dtype='float32')
        self.buf = self.lta.copy()

    def trigger(self, data):
        if data.size > self.nsta:
            res1 = self.trigger(data[:self.nsta])
            res2 = self.trigger(data[self.nsta:])
            return np.append(res1, res2)
        self.buf = self.buf[-self.nlta:]
        self.sta = self.sta[-self.nsta:]
        self.lta = self.lta[-self.nlta:]
        self.buf = np.append(self.buf, data ** 2)
        cum_sum = np.cumsum(self.buf[-data.size:])
        next_sta = self.sta[-1] + (cum_sum - np.cumsum(self.buf[-self.nsta-data.size:-self.nsta])) / nsta
        next_lta = self.lta[-1] + (cum_sum - np.cumsum(self.buf[-self.nlta-data.size:-self.nlta])) / nlta
        self.sta = np.append(self.sta, next_sta)
        self.lta = np.append(self.lta, next_lta)
        logger.debug('\nsta:' + str(self.sta[-data.size:])) # + '\nlta:' + str(self.lta[-data.size:]))
        return self.sta[-data.size:] / self.lta[-data.size:]


nsta = 5
nlta = 10
data = np.arange(20)
slTrigger = StaLtaTriggerCore(nsta, nlta)
slTrigger.trigger(data)

