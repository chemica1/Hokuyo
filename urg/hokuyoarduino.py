from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
import serial
import time
from threading import Thread, Timer, Event
import os
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

class hokuyoArduino():

    def __init__(self):
        COMNUM = self.file_to_list('COM')
        hokuyoArg = self.file_to_list('Hokuyo')
        self.hokuyoStart = int(hokuyoArg[0])
        self.hokuyoEnd = int(hokuyoArg[1])
        self.hokuyoDMAX = int(hokuyoArg[2])
        self.guiDMAX = int(hokuyoArg[3])

        self.ser = serial.Serial(port=f'{COMNUM[0]}', baudrate=9600, timeout=0)
        self.laser = HokuyoLX()
        self.DistEvent = Event()
        self.GuiEvent = Event()

        self.dstList = []

    def stopTimer(self, count):
        count += 1
        print(count)
        timer = Timer(1, self.stopTimer, args=[count])
        timer.start()
        if count == 5:
            print('stop')
            timer.cancel()

    def dstListUpdate(self):
        while True:
            if self.DistEvent.isSet(): #event가 set상태면 dist 업뎃
                timestamp, scan = self.laser.get_filtered_dist(start=self.hokuyoStart, end=self.hokuyoEnd, dmax=self.hokuyoDMAX)
                a = scan.T
                b = a[1]
                b.sort()
                print(b[0])
                self.dstList.append(b[0])

    def HokuyoGuiUpdate(self):
        plt.ion()
        ax = plt.subplot(111, projection='polar')
        plot = ax.plot([], [], '.')[0]
        text = plt.text(0, 1, '', transform=ax.transAxes)
        ax.set_rmax(self.guiDMAX)
        ax.grid(True)
        plt.show()
        while_tmp = 1
        while while_tmp:
            if not self.GuiEvent.isSet(): #event가 clear상태면 gui 업뎃
                timestamp, scan = self.laser.get_filtered_dist(start=self.hokuyoStart, end=self.hokuyoEnd, dmax=self.hokuyoDMAX)
                plot.set_data(*scan.T)
                text.set_text('t: %d' % timestamp)
                plt.draw()
                plt.pause(0.001)
            plt.pause(0.001)
            a = plt.get_fignums()
            while_tmp = a[0]

    def arduinoThread(self, ser):
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
                    tmp = self.parsing_data(line)
                    print(tmp)
                    if 'a' in tmp:
                        print("거리측정 시작합니다@@@@@@@@@@@@@@@@@@@")
                        self.GuiEvent.set()
                        self.DistEvent.set()
                        time.sleep(5)
                        self.GuiEvent.clear()
                        self.DistEvent.clear()
                        time.sleep(1)
                        self.pc2arduino()

                    del line[:]
                    #ser.write(b'1234|')
                    # line 변수 초기화

    def pc2arduino(self):
        self.dstList.sort()
        print(f'전송합니다 {self.dstList[0]}')
        a = int(self.dstList[0])
        self.ser.write(f'{a}|'.encode())
        del self.dstList[:]

    def parsing_data(self, data):
        # 리스트 구조로 들어 왔기 때문에
        # 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)
        return tmp

    def file_to_list(self, file):
        tempList = []
        dir_path = os.getcwd()
        with open(f'{dir_path}\\txt\\{file}.txt', 'r', encoding='UTF8') as fp:
            while (1):
                line = fp.readline()
                try:
                    escape = line.index('\n')
                except:
                    escape = len(line)
                if line:
                    tempList.append(line[0:escape])
                else:
                    break
        return tempList

    def run(self):
        arduinoThread = Thread(target=self.arduinoThread, args=(self.ser,))
        HokuyoGuiUpdate = Thread(target=self.HokuyoGuiUpdate)
        dstListUpdate = Thread(target=self.dstListUpdate)

        arduinoThread.start()
        HokuyoGuiUpdate.start()
        dstListUpdate.start()


if __name__ == '__main__':
    a = hokuyoArduino()
    a.run()
