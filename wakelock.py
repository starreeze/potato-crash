# coding=utf-8
from pymouse import PyMouse
from threading import Thread
import sys
from time import sleep


class MoveMouse(Thread):
    mouse = PyMouse()

    def __init__(self, interval, diff):
        Thread.__init__(self)
        self.interval = interval
        self.d = diff
        self.setDaemon(False)

    def run(self):
        self.runnable = True
        while self.runnable:
            sleep(self.interval)
            x, y = self.mouse.position()
            x += self.d
            self.mouse.move(x, y)
            self.d = -self.d

    def stop(self):
        self.runnable = False


move_mouse: MoveMouse


def set(interval, diff=1):
    global move_mouse
    move_mouse = MoveMouse(interval, diff)
    move_mouse.start()


def reset():
    move_mouse.stop()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interval = 30.0
        diff = 1
    else:
        interval = float(sys.argv[1])
        diff = int(sys.argv[2])
    set(interval, diff)
