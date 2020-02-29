import subprocess as s
import os


def send_audio_notification(type: str):
    if type.lower() == 'piano':
        os.system('play --replay-gain off /usr/share/sounds/ubuntu/ringtones/Melody\ piano.ogg')
    elif type.lower() == 'harmonic':
        os.system('play /usr/share/sounds/ubuntu/ringtones/Harmonics.ogg ')
    elif type.lower() == 'beep':
        os.system('play -v 0.3 assets/complete.oga')
    else:
        return 'Wrong'


def send_announcement(title, msg):
    send_audio_notification('beep')
    return s.call(['notify-send', title, msg])


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    return '%02d:%02d' % (mins, secs)
