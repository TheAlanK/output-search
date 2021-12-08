#!/usr/bin/env python
import PySimpleGUI as sg
import subprocess
import threading
from pynput.keyboard import Listener, KeyCode

import subprocess

process = subprocess.Popen(['adb', 'logcat'],
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
exit_key = KeyCode(char='e')


class Search(threading.Thread):
    def __init__(self):
        super(Search, self).__init__()
        self.program_running = True
        self.running = False

    def stop_running(self):
        self.running = False

    def start_running(self):
        self.running = True

    def exit(self):
        self.stop_running()
        self.program_running = False

    def run(self):
        self.start_running()
        while self.program_running:
            try:
                output = process.stdout.readline()
            except:
                output = process.stdout.readline()
              
            output = output.strip()
            output = self.print_output(output)

    def print_output(self, output):
        hasKeyword = output.find('Keymaster')

        if hasKeyword != -1:
            print(output)

        return_code = process.poll()

        if return_code is not None:
            for output in process.stdout.readlines():
                print(output.strip())
                break
        return output


search_thread = Search()
search_thread.start()


def on_press(key):
    if key == exit_key:
        if search_thread.running:
            search_thread.exit()
            listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
