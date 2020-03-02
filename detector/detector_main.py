import inspect
from multiprocessing import Process

from detector.filter_trigger.StaLtaTrigger import sta_lta_picker
from detector.filter_trigger.trigger_resender import resend
from detector.misc.globals import Port, CustomThread
from detector.misc.html_util import getTriggerParams
from detector.send_receive.signal_receiver import signal_receiver


import zmq
import json, os
import backend

from detector.send_receive.triggers_proxy import triggers_proxy

use_thread = False

if __name__ == '__main__':

    context = zmq.Context()
    socket_backend = context.socket(zmq.SUB)
    socket_backend.bind('tcp://*:' + str(Port.backend.value))
    socket_backend.setsockopt(zmq.SUBSCRIBE, b'AP')

    while True:

        paramsList = getTriggerParams()
        for params in paramsList:
            params.update({'station': 'ND01', 'freqmin': 100, 'freqmax': 300, 'init_level': 2, 'stop_level': 1})

        kwargs_list = [{'target': signal_receiver,
                        'kwargs': {'conn_str': 'tcp://192.168.0.189:' + str(Port.test_signal.value)}},
                       {'target': resend, 'kwargs': {'conn_str': 'tcp://*:' + str(Port.signal_resend.value),
                                                     'triggers': [1, 2], 'pem': 1, 'pet': 1}},
                       {'target': triggers_proxy, 'kwargs': {}},
                       {'target': sta_lta_picker, 'kwargs': paramsList[0]},
                       {'target': sta_lta_picker, 'kwargs': paramsList[1]},
                       {'target': sta_lta_picker, 'kwargs': paramsList[2]}]

        ps = []
        for kwargs in kwargs_list:
            if use_thread:
                p = CustomThread(**kwargs)
            else:
                p = Process(**kwargs)
            ps.append(p)
        for p in ps:
            p.start()

        socket_backend.recv()

        for p in ps:
            p.terminate()
        print('threads stopped')
        continue
    print('after break away from cycle, should exit')
