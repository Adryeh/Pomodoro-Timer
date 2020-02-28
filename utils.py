import subprocess as s


def send_announcement(title, msg):
    return s.call(['notify-send', title, msg])


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    return '%02d:%02d' % (mins, secs)
