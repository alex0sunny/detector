import socket
import time

from obspy import *
from matplotlib import pyplot

from detector.misc.header_util import chunk_stream, stream_to_json
from detector.test.signal_generator import SignalGenerator


def send_signal(st, port):

    signal_generator = SignalGenerator(st)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(10)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            pyplot.ion()
            figure = pyplot.figure()
            st_vis = Stream()
            check_time = time.time()
            while True:
                st = signal_generator.get_stream()
                st_vis += st.copy()
                cur_time = time.time()
                if cur_time > check_time + 1:
                    check_time = cur_time
                    st_vis.sort().merge()
                    starttime = st_vis[0].stats.endtime - 5
                    st_vis.trim(starttime=starttime)
                    pyplot.clf()
                    st_vis.plot(fig=figure)
                    pyplot.show()
                    pyplot.pause(.01)
                sts = chunk_stream(st)
                json_datas = [stream_to_json(st).encode('utf8') for st in sts]
                for json_data in json_datas:
                    data_len = len(json_data)
                    #print('bdata size:' + str(data_len))
                    size_bytes = int(data_len).to_bytes(4, byteorder='little')
                    conn.sendall(size_bytes + json_data)
                    time.sleep(.01)
                time.sleep(.1)


st = read('D:/converter_data/example/onem.mseed')
for tr in st:
    tr.stats.station = 'ND01'

send_signal(st, 5555)
