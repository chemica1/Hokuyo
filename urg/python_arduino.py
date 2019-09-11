from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
import serial
import time
import signal
import threading

DMAX = 2500

class Hokuyo():
    def __init__(self):
        self.ser = serial.Serial(port='COM3', baudrate=9600,timeout=0)
        self.line = []  # 라인 단위로 데이터 가져올 리스트 변수
        self.exitThread = False  # 쓰레드 종료용 변수

    def handler(self, signum, frame):
        exitThread = True

    # 데이터 처리할 함수
    def parsing_data(self, data):
        # 리스트 구조로 들어 왔기 때문에
        # 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)
        print(tmp)

    def readThread(self, ser):
        # 쓰레드 종료될때까지 계속 돌림
        while not self.exitThread:
            # 데이터가 있있다면
            for c in ser.read():
                # line 변수에 차곡차곡 추가하여 넣는다.
                self.line.append(chr(c))
                if c == 124:  # 아스키코드 | 임 라인의 끝을 만나면..
                    # 데이터 처리 함수로 호출
                    self.parsing_data(self.line)
                    ser.write(b'1234|')
                    # line 변수 초기화
                    del self.line[:]

    def update(self, laser, plot, text):
        timestamp, scan = laser.get_filtered_dist(start=530, end=550, dmax=10000)
        a = scan.T
        b = a[1]
        b.sort()
        print(b[0])
        plot.set_data(*scan.T)
        text.set_text('t: %d' % timestamp)
        plt.draw()
        plt.pause(0.001)

    def run(self):
        plt.ion()
        laser = HokuyoLX()
        ax = plt.subplot(111, projection='polar')
        plot = ax.plot([], [], '.')[0]
        text = plt.text(0, 1, '', transform=ax.transAxes)
        ax.set_rmax(DMAX)
        ax.grid(True)
        plt.show()

        thread1 = threading.Thread(target=self.readThread, args=(self.ser,))
        # 시작!
        thread1.start()

        while plt.get_fignums():
            self.update(laser, plot, text)
        laser.close()


if __name__ == '__main__':
    hokuyo = Hokuyo()
    hokuyo.run()
