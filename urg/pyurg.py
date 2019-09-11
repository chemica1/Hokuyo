from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
import serial

DMAX = 2500

class Hokuyo():
    distance = 0

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
        self.laser = HokuyoLX()
        ax = plt.subplot(111, projection='polar')
        plot = ax.plot([], [], '.')[0]
        text = plt.text(0, 1, '', transform=ax.transAxes)
        ax.set_rmax(DMAX)
        ax.grid(True)
        plt.show()
        while plt.get_fignums():
            self.update(self.laser, plot, text)
        self.laser.close()

if __name__ == '__main__':
    hokuyo = Hokuyo()
    hokuyo.run()
