import time
import os
import click
from tqdm import tqdm
from colorama import Fore, Style
import platform
import subprocess


def get_notify_command():
    """Returns the appropriate notification command based on the platform"""
    if platform.system() == 'Darwin':  # macOS
        return 'osascript -e \'display notification "Break is over!" with title "Pomodoro Timer"\''
    elif platform.system() == 'Linux':  # Linux
        return 'notify-send "Pomodoro Timer" "Break is over!"'
    else:  # Windows
        return ''


def check_capabilities():
    """Determines if sound and notification are supported on the platform"""
    can_play_sound = False
    can_notify = False
    if platform.system() == 'Darwin':  # macOS
        can_play_sound = True
        can_notify = True
    elif platform.system() == 'Linux':  # Linux
        try:
            subprocess.call(['aplay', '--version'])
            can_play_sound = True
        except:
            pass

        try:
            subprocess.call(['notify-send', '--version'])
            can_notify = True
        except:
            pass

    else:  # Windows
        try:
            import winsound
            can_play_sound = True
        except:
            pass

    return can_play_sound, can_notify


def play_sound():
    """Plays a sound to indicate the end of a work session"""
    if platform.system() == 'Darwin':
        os.system('afplay /System/Library/Sounds/Ping.aiff')
    elif platform.system() == 'Linux':
        os.system('aplay /usr/share/sounds/speech-dispatcher/test.wav')
    else:  # Windows
        # winsound.PlaySound("*", winsound.SND_ALIAS)
        pass


@click.command()
@click.option('--work', '-w', default=25, type=int, help='Work time in minutes (default: 25)')
@click.option('--rest', '-b', default=5, type=int, help='Break time in minutes (default: 5)')
@click.option('--notify', '-n', is_flag=True, help='Enable desktop notifications (default: False)')
def pomodoro(work, rest, notify):
    # convert minutes to seconds
    work_time = work * 60
    break_time = rest * 60

    # Determine if sound and notification are supported
    can_play_sound, can_notify = check_capabilities()
    notify_command = get_notify_command()

    while True:
        # work session
        print(f'{Fore.GREEN}{Style.BRIGHT}Work for {work} minutes!{Style.RESET_ALL}')
        with tqdm(total=work_time, desc='Work', unit='s', bar_format='{l_bar}{bar}|') as pbar:
            for i in range(work_time, 0, -1):
                pbar.update()
                time.sleep(1)
            # play sound
            if can_play_sound:
                play_sound()
            if notify and notify_command:
                os.system(notify_command)

        # break session
        print(f'{Fore.RED}{Style.BRIGHT}Break for {rest} minutes!{Style.RESET_ALL}')
        with tqdm(total=break_time, desc='Break', unit='s', bar_format='{l_bar}{bar}|') as pbar:
            for i in range(break_time, 0, -1):
                pbar.update()
                time.sleep(1)
            # notify
            if can_notify and notify and notify_command:
                os.system(notify_command)


if __name__ == '__main__':
    pomodoro()
