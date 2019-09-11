from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
import serial
import time
import signal
from threading import Thread, Lock, Condition, Timer


DMAX = 2500

class hokuyoArduino():

    def __init__(self):
        self.ser = serial.Serial(port='COM3', baudrate=9600, timeout=0)
        self.exitThread = False  # 쓰레드 종료용 변수
        self.DMAX = 2500
        self.dstList = []
        self.cv = Condition() ## RLock이 하나 자동으로 생성된다.

    def stopUpdate_timer(self, count):
        count += 1
        print(count)
        timer = Timer(1, self.stopUpdate_timer, args=[count])
        timer.start()

        if count == 5:
            print('stop')
            timer.cancel()

    def dstListUpdate(self):
        with self.cv:
            while True:

    def HokuyoGuiUpdate(self, laser, plot, text):
        timestamp, scan = laser.get_filtered_dist(start=530, end=550, dmax=10000)
        a = scan.T
        b = a[1]
        b.sort()
        print(b[0])
        plot.set_data(*scan.T)
        text.set_text('t: %d' % timestamp)
        plt.draw()
        plt.pause(0.001)

    def handler(self, signum, frame):
        self.exitThread = True

    def initHokuyoGui(self):
        plt.ion()
        self.laser = HokuyoLX()
        ax = plt.subplot(111, projection='polar')
        plot = ax.plot([], [], '.')[0]
        text = plt.text(0, 1, '', transform=ax.transAxes)
        ax.set_rmax(DMAX)
        ax.grid(True)
        plt.show()
        while plt.get_fignums():
            self.HokuyoGuiUpdate(self.laser, plot, text)
        self.laser.close()


    def parsing_data(self, data):
        # 리스트 구조로 들어 왔기 때문에
        # 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)
        return tmp

    def readThread(self, ser):
        line = []
        # 쓰레드 종료될때까지 계속 돌림
        while True:
            # 데이터가 있있다면
            for c in ser.read():
                # line 변수에 차곡차곡 추가하여 넣는다.
                if not c == 124:  # 아스키코드 | 임 라인의 끝을 만나면..
                    line.append(chr(c))
                if c == 124:
                    # 데이터 처리 함수로 호출
                    print(self.parsing_data(line))
                    del line[:]
                    #ser.write(b'1234|')
                    # line 변수 초기화

    def run(self):