from datetime import datetime

import sublime
import sublime_plugin


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