import threading

def start_timer(count):
    count+=1
    print(count)
    timer = threading.Timer(1, start_timer, args=[count])
    timer.start()

    if count == 5:
        print('stop')
        timer.cancel()

start_timer(0)