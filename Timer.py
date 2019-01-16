from datetime import datetime

import sublime
import sublime_plugin
import time
import threading
import webbrowser


def show_message():
    sublime.message_dialog("You've already worked 40 minutes! It's time to break! Do not forget to set timer again!")
    webbrowser.open("youtube.com")

def show():
    while True:
        time.sleep(10)
        update_seconds()
        if sublime.timer_time is not None:
            sublime.timer_time = datetime.now()
        if sublime.timer_seconds > 18: #2400
            sublime.really = 1
            sublime.run_command("timer_stop")
            return

def update_seconds():
    if sublime.timer_time is not None:
        td = datetime.now() - sublime.timer_time
        sublime.timer_seconds += (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def show_time():
    has_run = hasattr(sublime, 'timer_seconds')
    if has_run is False or (has_run and sublime.timer_seconds == 0):
        sublime.status_message('timer is not running')
        return

    seconds = sublime.timer_seconds

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    output = []
    if hours >= 2:
        output.append('%i hours' % hours)
    elif hours == 1:
        output.append('1 hour')

    if minutes >= 2:
        output.append('%i minutes' % minutes)
    elif minutes == 1:
        output.append('1 minute')

    if seconds >= 2:
        output.append('%i seconds' % seconds)
    elif seconds == 1:
        output.append('1 second')

    sublime.status_message(' '.join(output))


class TimerStartCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        if not hasattr(sublime, 'timer_seconds'):
            sublime.timer_seconds = 0
        sublime.timer_time = datetime.now()
        if threading.activeCount() > 0:
            sublime.thread1 = threading.Thread(target=show)
            sublime.thread1.start()   


class TimerPauseCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        update_seconds()

        show_time()

        sublime.timer_time = None



class TimerStopCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        update_seconds()

        show_time()

        sublime.timer_seconds = 0
        sublime.timer_time = None
        if sublime.really == 1:
            sublime.really = 0
            show_message()



class TimerCurrentCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        update_seconds()

        show_time()

        if sublime.timer_time is not None:
            sublime.timer_time = datetime.now()